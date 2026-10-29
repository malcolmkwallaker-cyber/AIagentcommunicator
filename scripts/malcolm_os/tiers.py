"""Permission tiers. Unknown actions default to Tier 3 (approval required)."""

TIER_1 = "tier1_auto"
TIER_2 = "tier2_pull_request"
TIER_3 = "tier3_approval"

TIER_1_ACTIONS = {"read_repo", "research", "write_log", "post_agent_channel"}
TIER_2_ACTIONS = {"change_code", "change_document", "open_pull_request"}
TIER_3_ACTIONS = {
    "send_email", "publish", "spend_money", "change_crm", "delete_file",
    "message_external", "create_repo", "new_project", "act_on_communication",
    "push_to_main", "merge_pull_request",
}


def classify(action_type: str) -> str:
    a = (action_type or "").strip().lower()
    if a in TIER_1_ACTIONS:
        return TIER_1
    if a in TIER_2_ACTIONS:
        return TIER_2
    return TIER_3
