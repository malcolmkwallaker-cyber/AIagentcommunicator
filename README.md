# AIagentcommunicator

Last updated: 2026-10-29 / Author: ChatGPT / Status: Draft correction, disabled

This repository holds a proposed Malcolm OS collaboration framework. It supports Northern Minnesota Pemberton real estate, RunTheRoster, movedwithmalcolm.com and Malcolm OS. It does not replace Drive as the source of truth or establish that bots can accept each other's Slack handoffs.

## Current roles
| Agent | Useful work | Sources |
| --- | --- | --- |
| chief-of-staff | Reconcile priorities, accepted handoffs, blockers and verified results | Malcolm OS and this repository |
| real-estate | Lead-health, listing-readiness and recruiting drafts | Authorized scoped Drive/FUB evidence, if connected |
| runtheroster | Deduplicated QA review with build and reproduction evidence | malcolmkwallaker-cyber/NFLGM |
| website | Publishing failure review and factual local content drafts | malcolmkwallaker-cyber/moved-with-malcolm |

Roles and cadence are in `agents/`. All four workflows are manual-only, with literal disabled job gates. `PAUSE` is present as a second control. No cron triggers remain. The existing 8 AM America/Chicago weekday discussion, Friday lead report, Tuesday CEO meeting and RunTheRoster QA remain the coordination points. No replacement schedules have been activated. Future recurring schedules must be deduplicated and account for Central daylight saving time.

## Repository decision
The original request named a separate `malcolm-os-agents` repository. This PR instead lives in `AIagentcommunicator`. Its root framework layout is usable for a coordination repository, but it does not satisfy the original repository-name requirement and is not a complete multi-bot transport. The named separate repository returned unavailable during review, which does not prove it does not exist. Keep this correction on PR #1. Do not rename, create, migrate or deploy a repository implicitly. Before activation, Malcolm must choose this repository as the home or approve a separate migration. Do not run two copies.

## Safety boundaries
Tier 1 is scoped reading, research, local logs and approved agent-channel coordination. Tier 2 changes require PR review. Tier 3 covers external messages, publishing, spending, CRM changes, deletion, new repos/projects and unknown actions.

Classification alone does not enforce execution. The old CLI allowed an unrelated approval ID to authorize an action and accepted approved requests indefinitely. Approval evidence is now checked for age, author, action and exact scope, with rejection precedence. Test requests never authorize real actions. The CLI still denies every Tier 3 execution because there is no trusted single-use executor. That executor needs an immutable payload, target, expiry, action binding, atomic consumption and an audit trail before it can be enabled. A reaction is not permission for arbitrary future actions.

No GitHub write token or Slack token is passed to the Claude template. It has only Read/Glob/Grep tools and remains disabled. Future PR writes require an independently enforced broker and tested default-branch protection, not a model promise or shell allowlist. Do not grant an all-repositories write token. A separate read-only token may eventually cover owned repositories; any approved writer must be limited to explicitly selected repos and non-default branches. Existing tokens, scopes, rulesets, spending limits and Slack membership have not been verified.

## Slack configuration, currently unused
Coordination uses MyPRE `#malcolms-agents`, workspace `T0BKDCYEFDZ`, channel `C0CE20ZCCNL`. `SLACK_APPROVER_USER_ID` must be Malcolm's MyPRE identity `U0BP29247TM`. The separate Real Estate workspace's `#ai-agents` is not interchangeable.

`SLACK_APPROVAL_CHANNEL_ID` must point to a distinct, verified approval channel in MyPRE. None has been verified or created in this correction. The code fails closed when configuration, workspace, name, membership or identity does not match. It accepts no discontinued project channels and does not discover channels by ambiguous name.

For a separately approved live test, a maintainer would configure `SLACK_BOT_TOKEN`, `SLACK_WORKSPACE_ID`, `SLACK_APPROVER_USER_ID`, `SLACK_BOT_USER_ID`, `SLACK_APPROVAL_CHANNEL_ID` and `SLACK_APPROVAL_CHANNEL_NAME`. Secrets never belong in source. Grant only necessary Slack posting, history and reactions read scopes for designated channels; no channel creation or broad posting scope. No live test or secret setup is performed by this PR.

## Validation
Run `python -m unittest discover tests -v`. Offline validation also runs on pull requests, with no secrets, network, Slack posts or paid calls. It intentionally runs while PAUSE is present; agent execution and Slack actions do not. The old workflow called a Slack-writing integration test a dry run. It has been replaced with truly offline tests. A future live test must explicitly disclose its Slack posts and paid API calls and receive approval first.

## Before recommending activation
1. Confirm the repository home and existing owners; avoid duplicate automation.
2. Verify least-privilege credential scopes and branch protections using actual service evidence.
3. Verify the designated Slack workspace, bot and approval channel, and Malcolm's identity.
4. Implement and test any required write broker and durable, scope-bound, single-use approvals. No Tier 3 executors currently exist.
5. Add approved source connectors or a dated, approved context snapshot; this template cannot fetch Drive/FUB by itself.
6. With explicit approval, run a bounded live read/draft test and a Slack handoff acceptance test. Prove rejection, expiration and PAUSE behavior. Do not call a posted handoff accepted until its recipient responds.
7. Verify official action/version compatibility, pin reviewed action commits, retain 25-turn and 20-minute limits, verify usage logging against actual action output and set a provider spend cap.
8. Review new CI results. Only then request Malcolm's approval for enabling selected work, in a separate PR. Removing PAUSE alone does not activate anything.

No approval to merge or activate is recommended yet. See CLAUDE.md for source links and exact operating boundaries.
