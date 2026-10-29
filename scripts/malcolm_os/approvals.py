"""Approval evidence only. No trusted external-action executor exists yet."""
import json
import math
import os
import time

from . import slack
from .tiers import TIER_3, classify

EXPIRY_SECONDS = 72 * 3600
APPROVE = {"white_check_mark", "heavy_check_mark", "ballot_box_with_check"}
REJECT = {"x", "negative_squared_cross_mark"}
PREFIX = "[Claude] Approval request\n"


def decide(reactions, approver_id, message_ts, now=None) -> str:
    now = time.time() if now is None else now
    try:
        age = now - float(message_ts)
    except (TypeError, ValueError):
        return "invalid"
    if not approver_id or not math.isfinite(age) or age < 0:
        return "invalid"
    names = {}
    for reaction in reactions or []:
        names.setdefault(reaction["name"].split("::")[0], set()).update(reaction.get("users", []))
    if any(approver_id in names.get(n, set()) for n in REJECT):
        return "rejected"
    if age >= EXPIRY_SECONDS:
        return "expired"
    if any(approver_id in names.get(n, set()) for n in APPROVE):
        return "approved"
    return "pending"


def request(agent: str, action_type: str, summary: str, dry_run: bool = False) -> dict:
    if not agent.strip() or not action_type.strip() or not summary.strip():
        raise ValueError("Agent, action and exact scope/target summary are required")
    payload = {"version": 1, "agent": agent, "action": action_type,
               "scope": summary, "test_only": bool(dry_run)}
    text = PREFIX + json.dumps(payload, sort_keys=True) + "\nReact to approve or reject. Expires in 72 hours. Evidence only; execution disabled."
    d = slack.post("agent-approvals", text)
    return {"approval_id": d["ts"], "tier": classify(action_type), "execution_enabled": False}


def evidence(message, approver_id, action_type=None, scope=None, now=None):
    if approver_id != slack.APPROVER_ID:
        return "invalid"
    bot = os.environ.get("SLACK_BOT_USER_ID")
    if not bot or message.get("user") != bot or message.get("edited"):
        return "invalid"
    text = message.get("text", "")
    if not text.startswith(PREFIX):
        return "invalid"
    try:
        payload = json.loads(text.splitlines()[1])
    except (ValueError, IndexError):
        return "invalid"
    if not isinstance(payload, dict) or payload.get("version") != 1:
        return "invalid"
    if payload.get("test_only") is not False:
        return "test_only"
    if not all(isinstance(payload.get(k), str) and payload[k].strip() for k in ("agent", "action", "scope")):
        return "invalid"
    if action_type is not None and payload["action"] != action_type:
        return "scope_mismatch"
    if scope is not None and payload["scope"] != scope:
        return "scope_mismatch"
    return decide(message.get("reactions", []), approver_id, message.get("ts"), now)


def status(approval_id: str, approver_id: str, action_type=None, scope=None) -> str:
    cid = slack.channel_id("agent-approvals")
    d = slack.api("reactions.get", {"channel": cid, "timestamp": approval_id}, http_post=False)
    message = d.get("message", {})
    if message.get("ts") != approval_id:
        return "invalid"
    return evidence(message, approver_id, action_type, scope)


def check_all(approver_id: str, limit: int = 100) -> dict:
    cid = slack.channel_id("agent-approvals")
    d = slack.api("conversations.history", {"channel": cid, "limit": limit}, http_post=False)
    return {"requests": {m["ts"]: {"state": evidence(m, approver_id), "text": m["text"]}
                         for m in d["messages"] if m.get("text", "").startswith(PREFIX)},
            "has_more": bool(d.get("has_more")), "execution_enabled": False}


def authorize(action_type: str, approval_id, approver_id: str) -> tuple:
    """Classification is not execution authority. Fail closed for all Tier 3."""
    tier = classify(action_type)
    if tier != TIER_3:
        return True, f"{tier}: classification only; Tier 2 requires a reviewed PR"
    return False, "Tier 3 execution disabled: a trusted scope-bound single-use executor is required"
