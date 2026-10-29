"""Approval flow: requests live as Slack messages in #agent-approvals.

A checkmark reaction from SLACK_APPROVER_USER_ID approves, an X rejects.
Requests expire after 72 hours. Only the approver's reactions count.
"""
import re
import time

from . import slack
from .tiers import TIER_3, classify

EXPIRY_SECONDS = 72 * 3600
APPROVE = {"white_check_mark", "heavy_check_mark", "ballot_box_with_check"}
REJECT = {"x", "negative_squared_cross_mark"}
ID_RE = re.compile(r"APPROVAL-ID:\s*(\d+\.\d+)")


def decide(reactions, approver_id, message_ts, now=None) -> str:
    """Return approved / rejected / expired / pending. Pure function (tested)."""
    now = time.time() if now is None else now
    names = {r["name"].split("::")[0]: r.get("users", []) for r in reactions or []}
    # Rejection wins over approval if the approver used both.
    if any(approver_id in names.get(n, []) for n in REJECT):
        return "rejected"
    if any(approver_id in names.get(n, []) for n in APPROVE):
        return "approved"
    if now - float(message_ts) > EXPIRY_SECONDS:
        return "expired"
    return "pending"


def request(agent: str, action_type: str, summary: str, dry_run: bool = False) -> dict:
    tier = classify(action_type)
    text = (
        f":raising_hand: *Approval request*{' (TEST, no action will be taken)' if dry_run else ''}\n"
        f"AGENT: {agent}\nACTION: {action_type} ({tier})\nSUMMARY: {summary}\n"
        f"React :white_check_mark: to approve or :x: to reject. Expires in 72h."
    )
    d = slack.post("agent-approvals", text)
    ts = d["ts"]
    slack.api("chat.postMessage", {"channel": d["channel"], "thread_ts": ts, "text": f"APPROVAL-ID: {ts}"})
    return {"approval_id": ts, "tier": tier}


def status(approval_id: str, approver_id: str) -> str:
    cid = slack.channel_id("agent-approvals")
    d = slack.api("reactions.get", {"channel": cid, "timestamp": approval_id}, http_post=False)
    return decide(d["message"].get("reactions", []), approver_id, approval_id)


def check_all(approver_id: str, limit: int = 100) -> dict:
    cid = slack.channel_id("agent-approvals")
    d = slack.api("conversations.history", {"channel": cid, "limit": limit}, http_post=False)
    out = {}
    for m in d["messages"]:
        if "Approval request" in m.get("text", "") and "TEST" not in m["text"]:
            out[m["ts"]] = {"state": decide(m.get("reactions", []), approver_id, m["ts"]),
                            "text": m["text"]}
    return out


def authorize(action_type: str, approval_id, approver_id: str) -> tuple:
    """Code-level gate. Returns (allowed, reason)."""
    tier = classify(action_type)
    if tier != TIER_3:
        return True, f"{tier}: no approval needed (Tier 2 still requires a PR)"
    if not approval_id:
        return False, "Tier 3 action requires an approval id"
    s = status(approval_id, approver_id)
    return s == "approved", s
