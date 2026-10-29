"""Minimal Slack Web API client (stdlib only)."""
import json
import os
import urllib.parse
import urllib.request

CHANNELS = {
    "chief-of-staff": "agent-chief-of-staff",
    "cirql": "agent-cirql",
    "steadfast": "agent-steadfast",
    "portfolio": "agent-portfolio",
    "handoffs": "agent-handoffs",
    "approvals": "agent-approvals",
}
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
    """Resolve channel name to ID (bot must be a member / channel visible)."""
    cursor = ""
    while True:
        p = {"types": "public_channel,private_channel", "limit": 200, "exclude_archived": "true"}
        if cursor:
            p["cursor"] = cursor
        d = api("conversations.list", p, http_post=False)
        for c in d["channels"]:
            if c["name"] == name:
                return c["id"]
        cursor = d.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            raise RuntimeError(f"Channel #{name} not found")


def post(channel: str, text: str) -> dict:
    name = normalize_channel(channel)
    return api("chat.postMessage", {"channel": channel_id(name), "text": text})
