"""Minimal Slack Web API client (stdlib only)."""
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request

CHANNELS = {
    "chief-of-staff": "malcolms-agents",
    "real-estate": "malcolms-agents",
    "runtheroster": "malcolms-agents",
    "website": "malcolms-agents",
    "handoffs": "malcolms-agents",
    "approvals": "agent-approvals",
}
WORKSPACE_ID = "T0BKDCYEFDZ"
COORDINATION_ID = "C0CE20ZCCNL"
APPROVER_ID = "U0BP29247TM"


def ensure_unpaused():
    if (Path(__file__).resolve().parents[2] / "PAUSE").exists():
        raise RuntimeError("PAUSE present; live operations disabled")


AGENT_CHANNELS = set(CHANNELS.values())
HANDOFF_FIELDS = ("FROM", "TO", "TASK", "CONTEXT", "DUE")


def normalize_channel(name: str) -> str:
    n = name.strip().lstrip("#")
    n = CHANNELS.get(n, n)
    if n not in AGENT_CHANNELS:
        raise ValueError(f"Channel '{name}' is not a designated agent channel")
    return n


def format_handoff(frm, to, task, context, due) -> str:
    vals = dict(zip(HANDOFF_FIELDS, (frm, to, task, context, due)))
    for k, v in vals.items():
        if not str(v).strip():
            raise ValueError(f"Handoff field {k} is required")
    return "\n".join(f"{k}: {vals[k]}" for k in HANDOFF_FIELDS)


def api(method: str, params: dict, token: str = None, http_post: bool = True) -> dict:
    ensure_unpaused()
    token = token or os.environ["SLACK_BOT_TOKEN"]
    headers = {"Authorization": "Bearer " + token}
    if http_post:
        req = urllib.request.Request(
            "https://slack.com/api/" + method,
            data=json.dumps(params).encode(),
            headers={**headers, "Content-Type": "application/json; charset=utf-8"},
        )
    else:
        req = urllib.request.Request(
            "https://slack.com/api/" + method + "?" + urllib.parse.urlencode(params),
            headers=headers,
        )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if not data.get("ok"):
        raise RuntimeError(f"Slack {method} failed: {data.get('error')}")
    return data


def channel_id(name: str) -> str:
    """Use explicit workspace-bound IDs; never resolve by channel name alone."""
    name = normalize_channel(name)
    if os.environ.get("SLACK_WORKSPACE_ID") != WORKSPACE_ID:
        raise ValueError("Expected verified MyPRE workspace")
    if os.environ.get("SLACK_APPROVER_USER_ID") != APPROVER_ID:
        raise ValueError("Expected Malcolm's MyPRE identity")
    auth = api("auth.test", {}, http_post=False)
    if auth.get("team_id") != WORKSPACE_ID or auth.get("user_id") != os.environ.get("SLACK_BOT_USER_ID"):
        raise ValueError("Slack bot identity/workspace mismatch")
    cid = COORDINATION_ID
    expected_name = "malcolms-agents"
    if name == "agent-approvals":
        cid = os.environ.get("SLACK_APPROVAL_CHANNEL_ID", "")
        expected_name = os.environ.get("SLACK_APPROVAL_CHANNEL_NAME", "")
        if not cid.startswith("C") or cid == COORDINATION_ID or not expected_name:
            raise ValueError("A distinct verified approval channel is required")
    channel = api("conversations.info", {"channel": cid}, http_post=False)["channel"]
    if (channel.get("id") != cid or channel.get("name") != expected_name
            or not channel.get("is_member") or channel.get("is_archived")
            or channel.get("is_ext_shared")):
        raise ValueError("Slack channel identity, membership or sharing mismatch")
    return cid


def post(channel: str, text: str) -> dict:
    name = normalize_channel(channel)
    return api("chat.postMessage", {"channel": channel_id(name), "text": text})

