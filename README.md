# malcolm-os-agents

A team of autonomous Claude agents (Chief of Staff, Cirql, Steadfast, Portfolio) that run on a schedule via GitHub Actions, read all your repos, and talk to you in Slack.

**Rules they follow (enforced in code and in `CLAUDE.md`)**
- Tier 1 (automatic): read repos, research, logs, post in agent channels.
- Tier 2 (pull request): any change to your code/docs goes in a PR. Never direct to `main`.
- Tier 3 (needs your approval in `#agent-approvals`): email, publishing, spending, CRM changes, deleting, messaging outsiders, creating repos/projects, acting on suggestions from communications. Unknown actions default to Tier 3.

## Setup (no coding needed)

### 1. Slack
1. Go to https://api.slack.com/apps → **Create New App** → From scratch.
2. **OAuth & Permissions** → Bot Token Scopes: `chat:write`, `channels:read`, `channels:history`, `reactions:read` (add `groups:read`, `groups:history` if channels are private).
3. **Install to Workspace**. Copy the **Bot User OAuth Token** (starts `xoxb-`) → this is `SLACK_BOT_TOKEN`.
4. Create channels: `#agent-chief-of-staff`, `#agent-cirql`, `#agent-steadfast`, `#agent-portfolio`, `#agent-handoffs`, `#agent-approvals`. In each, type `/invite @YourBotName`.
5. Your Slack user ID: click your profile → ⋮ → **Copy member ID** (starts `U`) → `SLACK_APPROVER_USER_ID`.

### 2. Anthropic
https://console.anthropic.com → **API Keys** → Create key → `ANTHROPIC_API_KEY`. Set a monthly spend limit there too.

### 3. GitHub token
GitHub → Settings → Developer settings → Fine-grained tokens → **Generate new token**.
- Resource owner: you. Repository access: **All repositories**.
- Permissions: Contents **Read** and write (needed to push agent branches), Pull requests **Read and write**, Metadata Read. Leave everything else off.
- Also add a **branch protection rule / ruleset** on every repo's default branch requiring a pull request, so the token cannot push to main even by mistake.
- Copy the token → `GH_AGENT_TOKEN`.

### 4. Add the secrets
In this repo: **Settings → Secrets and variables → Actions → New repository secret**. Add `ANTHROPIC_API_KEY`, `SLACK_BOT_TOKEN`, `SLACK_APPROVER_USER_ID`, `GH_AGENT_TOKEN`.
Also install the Claude GitHub app: https://github.com/apps/claude

### 5. Test
**Actions → Dry run test → Run workflow.** It runs unit tests, reads one repo, posts a test message to `#agent-chief-of-staff`, and posts a test approval request in `#agent-approvals`. Nothing is changed.

## Everyday use
- **Approve/reject:** react ✅ or ❌ on the request in `#agent-approvals`. Only your reaction counts. Requests expire after 72 hours. The next agent run checks reactions and only then acts.
- **Run an agent now:** Actions → pick the agent → Run workflow.
- **Change schedule:** edit the `cron:` line in `.github/workflows/agent-<name>.yml` (times are UTC; https://crontab.guru helps). Defaults: chief-of-staff 07:00, others 08:00–09:00, weekdays.
- **Kill switch:** create an empty file named `PAUSE` in the repo root. Every workflow exits immediately. Delete it to resume.
- **Cost controls:** each run has `--max-turns 25` and a 20-minute timeout (edit in the `agent-*.yml` files). Approximate usage (turns, tokens, cost) is shown in each run's summary.
- **Edit agents:** change `agents/*.md` (role, repos, channel, metrics) and `CLAUDE.md`. Add an agent by adding a file in `agents/` and copying a workflow.

## Developer notes
`python -m unittest discover tests` — helper scripts in `scripts/` use only the Python standard library.
