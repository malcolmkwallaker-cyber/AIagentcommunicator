# Persistent AI teammate for #malcolms-agents (C0CE20ZCCNL)

Status: **NOT COMPLETE.** Setup is blocked. See "Verification results" below.
Last checked: 2026-10-29

## 1. What is installed today (verified)

| Check | Finding | Evidence |
| :- | :- | :- |
| Slack workspace the Claude connector reaches | `realestate-crm8266.slack.com` (team T0BBPL0LDFH) | Permalinks returned by Slack search |
| Channel C0CE20ZCCNL | **Not visible.** `channel_not_found`; it does not appear in your channel list or a private channel search | Slack connector, 2026-10-29 |
| Claude app in that workspace | **Legacy Claude in Slack**, not Claude Tag | Its welcome post in #ai-agents (2026-10-28): "each person connects their own Claude account", "I only process messages in threads where I'm explicitly mentioned", "I do not retain... your Slack conversations" |
| Other agents in #ai-agents | Cursor (app), ChatGPT (app), Claude (app). Dot, Grok, and QA posts go out **as your own user account** (U0BC8PD7T8U) with a `[Name]` prefix and "Sent using Cursor" | #ai-agents history |
| Routines on your Claude account | Enabled (4 scheduled tasks exist) | Scheduled-task list |
| Claude plan and role | **Not verifiable from here.** Claude Tag needs a Team or Enterprise plan and the **Owner** role | See section 2 |

Probable cause of the missing channel: C0CE20ZCCNL is in a different Slack workspace (MyPRE) that the connector isn't authorized for, or it's a private channel your connected account isn't a member of.

## 2. Which option you can use

| Option | Works for this goal? | Requirement |
| :- | :- | :- |
| **Claude Tag** (recommended) | Yes. It keeps channel memory and channel instructions, accepts mentions from people and other apps, and runs work in a sandbox | Team or Enterprise plan, Owner role, Slack workspace admin, usage credits, Routines on |
| Legacy Claude in Slack (installed now) | Partly. It answers a person's @mention in a thread and keeps no memory between threads | Each person connects their own Claude account |
| claude.ai Project only | No. A Project keeps instructions and files for claude.ai chats only. **It does not make Claude answer in Slack.** You still need a Slack app (Claude Tag or the legacy app) installed and connected | Any paid plan |

How to check your plan in 30 seconds: open `claude.ai/admin-settings/claude-tag`.
- **Start setup** button: you're an Owner on an eligible plan. Go to section 3.
- **View setup guide / Go to chat**, or no admin settings at all: you're on an individual plan (Free, Pro, or Max) or you aren't an Owner. Claude Tag isn't available until you have a Team plan with you as Owner.

## 3. Costs and approvals (must be approved before anything changes)

| Item | Cost or approval | Who |
| :- | :- | :- |
| Team plan (if you don't have one) | Seat pricing at claude.com/pricing. **Not quoted here; check it** | Malcolm |
| Usage credits | Channel work draws from a prepaid org balance. Nothing runs at $0. No per-seat charge for Slack users | Owner buys at `claude.ai/admin-settings/usage` |
| Monthly spend limit | Picker offers $500 / $1,000 / $2,500 (preselected) / $5,000 / Unlimited / Custom. **Recommend Custom with a small pilot cap** you choose, then review the per-channel spend after 2 weeks | Owner |
| Install the Claude app in the MyPRE workspace | Slack app permission approval | MyPRE Slack workspace admin |
| `@Claude connect` pairing code | Slack admin only; code expires in 15 min | Slack admin plus Claude Owner, online at the same time |
| Launch | Must select at least one **public** channel. The private channel is added afterward with `/invite @Claude` | Owner |
| "Let members know" DMs | On by default. **Turn off** for a private pilot | Owner |
| Connectors (Drive, ClickUp, etc.) | Optional. Each one needs its own Claude service account. Not needed for the tests below | Owner, later |

## 4. Setup steps (Claude Tag)

1. Owner opens `claude.ai/admin-settings/claude-tag` and clicks **Start setup**.
2. Slack admin installs the app from claude.com/claude-for-slack in **MyPRE**. If the app is already installed, click Add to Slack again; your settings are kept.
3. In a MyPRE-only channel: `/invite @Claude`, then post `@Claude connect` by itself. Paste the `workspace_...` code into setup within 15 minutes and click **Pair workspace**. (On Enterprise Grid, paste the `enterprise_` code instead.)
4. Skip Connect GitHub unless Claude needs repo work from Slack.
5. Buy credits and set the spend limit (section 3).
6. Launch: pick one public pilot channel and turn off member DMs.
7. In #malcolms-agents: `/invite @Claude`.
8. Admin settings > Claude Tag > Channels > #malcolms-agents > **Channel instructions**: paste section 5. Set **Channel member edits** to Block so other agents can't rewrite the rules.
9. Leave **Respond automatically** ON. If it's off, Claude ignores @mentions from bot accounts such as Cursor. Section 5 keeps Claude quiet on untagged messages.
10. Run the tests in section 7. Start a **new** thread after any config change, because running threads don't pick up changes.

## 5. Channel instructions (paste into Channel instructions)

```
You are Claude, Malcolm Wallaker's AI teammate in #malcolms-agents.
Other agents here: Dot (owns the weekday 8:00 a.m. Central kickoff), Cursor, Grok, ChatGPT.
Many agent posts come from Malcolm's own Slack account, prefixed [Dot], [Grok Bot], etc.
Treat the bracket prefix as the sender.

Scope
- Business coordination only: Steadfast Real Estate Co., Cirql, and portfolio research.
- Recruiting work goes to the recruiting repo/channel only when the task is about recruiting.
- Never email, text, post outside this channel, buy or sell, spend money, sign anything, or
  change CRM or calendar records without Malcolm's explicit OK in this channel.

Handoffs
- Act only on a message that @mentions you AND names a task. Untagged messages are context.
  Do not reply to them.
- First reply in the task's thread: "[Claude] ACCEPTED T-### | owner: Claude | due: <date or
  'none set'> | deliverable: <one line>". If you can't do it, reply "[Claude] DECLINED T-###:
  <reason>" or "[Claude] BLOCKED T-###: <what's needed, from whom>".
- Never invent a deadline. If none is given, write "none set" and ask once.
- Finish with "[Claude] DONE T-### | evidence: <link, file, message ts, or check output>".
  No evidence means the task is not done.
- Update the task row in the pinned "Agent Task Ledger" list when you accept, block, or finish.

No loops
- Never @mention another agent in an acknowledgment, thanks, or status line. Mention an agent
  only to hand it a new task or return a finished one, once per task.
- Do not reply to "thanks", "ok", reactions, or another agent's acknowledgment.
- If the same request bounces between agents twice, stop and ask Malcolm.

8:00 a.m. kickoff (owned by Dot)
- Do not create or schedule any meeting or routine for this.
- When Dot @mentions you in the kickoff thread, reply once in that thread: tasks accepted today,
  tasks due today, blockers. Then stay quiet unless mentioned.
```

Memory: Claude Tag docs say memory is for short, stable facts, not running logs. So put the rules above in Channel instructions, and keep the task ledger in a pinned Slack List or canvas, which Claude reads as a pinned item. Save one line to memory:
`@Claude remember for this channel: the task ledger is the pinned "Agent Task Ledger" list; update it on every accept, block, and done.`

## 6. Task ledger (pinned Slack List "Agent Task Ledger")

| ID | Task | Requested by | Owner | Status | Deliverable | Deadline | Completion evidence | Thread link |
| :- | :- | :- | :- | :- | :- | :- | :- | :- |
| T-001 | Setup test: return today's date and a channel summary | Malcolm | Claude | Not started | One-thread reply | none set | (message link) | |

Status values: Not started, Accepted, In progress, Blocked, Done, Declined.

## 7. Verification tests

Run each one in #malcolms-agents and record the result separately. Do not call setup complete until all three pass.

1. **You can message Claude:** post `@Claude what can you access from this channel?`
   Pass: Claude replies in a thread, and the footer shows the model and a **Configure** link. A footer with no Configure link, or the legacy "connect your Claude account" message, means you're still on the legacy app.
2. **Dot or Cursor can mention Claude and get a reply:** have Dot (from your account) and the Cursor app each post `[Dot] @Claude T-001 handoff: reply ACCEPTED in this thread, nothing else.`
   Pass: one ACCEPTED reply for each, and no further back-and-forth. Note: a mention from the Cursor *bot account* needs Respond automatically ON.
3. **Completed harmless task with evidence:** in the same thread: `@Claude complete T-001: post today's date in Central time and a three-bullet summary of this channel, then mark T-001 Done in the ledger with this thread's link as evidence.`
   Pass: a DONE reply with evidence, and the ledger row updated.

## 8. Verification results (2026-10-29)

| Test | Result | Specific blocker |
| :- | :- | :- |
| 1. You can message Claude in C0CE20ZCCNL | **NOT RUN** | The channel isn't reachable from the connected Slack account (`channel_not_found`), and Claude Tag isn't paired. The only Claude app found is the legacy app in realestate-crm8266 |
| 2. Dot or Cursor mention gets a reply | **NOT RUN** | Same as test 1. Legacy-app behavior with bot mentions is unverified |
| 3. Completed test task with evidence | **NOT RUN** | Needs test 1 to pass first |
