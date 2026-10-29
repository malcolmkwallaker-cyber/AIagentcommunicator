"""Approximate per-run usage logging from the claude-code-action execution file."""
import json


def summarize(path: str) -> dict:
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {"note": "no execution file"}
    items = data if isinstance(data, list) else [data]
    for it in reversed(items):
        if isinstance(it, dict) and it.get("type") == "result":
            u = it.get("usage", {}) or {}
            return {
                "turns": it.get("num_turns"),
                "duration_ms": it.get("duration_ms"),
                "cost_usd_approx": it.get("total_cost_usd"),
                "input_tokens": u.get("input_tokens"),
                "output_tokens": u.get("output_tokens"),
            }
    return {"note": "no result entry"}
