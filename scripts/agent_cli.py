#!/usr/bin/env python3
"""CLI used by agents (and workflows) for Slack, approvals, and tier checks."""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from malcolm_os import approvals, slack, tiers, usage  # noqa: E402


def approver() -> str:
    v = os.environ.get("SLACK_APPROVER_USER_ID")
    if not v:
        sys.exit("SLACK_APPROVER_USER_ID is not set")
    return v


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("post"); s.add_argument("--channel", required=True); s.add_argument("--text", required=True)
    s = sub.add_parser("handoff")
    for f in ("from", "to", "task", "context", "due"):
        s.add_argument("--" + f, required=True)
    s = sub.add_parser("request-approval")
    s.add_argument("--agent", required=True); s.add_argument("--action-type", required=True)
    s.add_argument("--summary", required=True); s.add_argument("--dry-run", action="store_true")
    sub.add_parser("check-approvals")
    s = sub.add_parser("authorize"); s.add_argument("--action-type", required=True); s.add_argument("--approval-id")
    s = sub.add_parser("classify"); s.add_argument("--action-type", required=True)
    s = sub.add_parser("log-usage"); s.add_argument("--agent", required=True); s.add_argument("--file", required=True)
    a = p.parse_args(argv)

    if a.cmd == "post":
        slack.post(a.channel, a.text)
    elif a.cmd == "handoff":
        slack.post("agent-handoffs", slack.format_handoff(getattr(a, "from"), a.to, a.task, a.context, a.due))
    elif a.cmd == "request-approval":
        print(json.dumps(approvals.request(a.agent, a.action_type, a.summary, a.dry_run)))
    elif a.cmd == "check-approvals":
        print(json.dumps(approvals.check_all(approver()), indent=2))
    elif a.cmd == "authorize":
        ok, why = approvals.authorize(a.action_type, a.approval_id, approver())
        print(("ALLOWED: " if ok else "DENIED: ") + why)
        return 0 if ok else 1
    elif a.cmd == "classify":
        print(tiers.classify(a.action_type))
    elif a.cmd == "log-usage":
        print(json.dumps({"agent": a.agent, **usage.summarize(a.file)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
