---
name: paperclip-daily-focus
description: Derive a daily or weekly operator focus from the Paperclip goal tree and actionable issues, then print a plain-text Focus Card. Use when the operator wants to prioritize the day — what to focus on or move today as the daily Highlight — or wants a weekly review that re-confirms the North Star and picks this week's Bet.
---

# Paperclip Daily Focus

Turn the live Paperclip goal tree and actionable issues into a single, defensible answer to "what do I move today, and why does it matter?" A read-only prioritization ritual: it surfaces one Highlight and routes the rest. Distinct from planning (`paperclip-plan-work`) and execution-readiness (`paperclip-triage`) — those create and start work; this only decides where attention goes.

Three nested horizons:

- **North Star** — the active root `company` goal. The why everything ladders up to.
- **Weekly Bet** — the one goal, motion, or project that gets prime attention this week.
- **Daily Highlight** — the single issue the operator should personally move today.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/control-plane.md`
- `references/docs/paperclip-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Inputs

- Active Paperclip company and profile, resolved before any read.
- Mode: `daily` (default) or `weekly` review.

## Read Surfaces

Reads only. Prefer `paperclipai` with JSON; fall back to MCP when the CLI lacks the read. See the integration matrix before choosing.

```sh
paperclipai context show --json
paperclipai issue list -C <company-id> --json
```

- Goals: MCP `paperclipListGoals` / `paperclipGetGoal` (no guaranteed CLI goal read).
- Issues: `paperclipai issue list --json` or MCP `paperclipListIssues` when richer filters are needed.

## Daily Workflow

1. Resolve company and profile context. Done when the company id is resolved.
2. Read the goal tree and name the North Star — the active root `company` goal. If more than one active company goal could be the root, surface them and ask. Done when one North Star is named or the operator has chosen.
3. Read actionable issues and build the candidate set: `in_progress`, `todo`, and any `in_review`/`blocked` that wait on the operator; drop `backlog`, `done`, `cancelled`. Map every candidate to its project, then its goal. Done when every candidate is tied to a goal or explicitly flagged goal-less.
4. Confirm this week's Bet. If the operator has not named one, propose the goal or project carrying the most candidates and confirm. Done when the Bet is confirmed, not assumed.
5. Choose one Daily Highlight by the focusing question and the tie-breaks below. Done when exactly one Highlight is named with its leverage rationale.
6. Sort every remaining candidate into one bucket below. Done when no candidate is left unsorted.
7. Print the Focus Card in chat as plain text. Done when the card is printed inline; this is a read, so open no approval dialog.

## Choosing And Sorting

These bind steps 5–6.

- **The focusing question:** "What one thing, done today, makes the rest easier or unnecessary?" The Highlight is the candidate that best answers it.
- **Highlight tie-breaks, in order:** advances the Bet; then unblocks the most other work (a blocker for many); then finishes something already `in_progress` before starting new; then higher native priority.
- **Buckets for the rest:**
  - **Maintenance** — small or owner-only items to do around the Highlight, never instead of it.
  - **Delegate** — work that should go to an agent; recommend routing to `paperclip-triage` / delegation, do not assign here.
  - **Park** — not this week; recommend dropping to `backlog`. Recommendation only.

## Weekly Review Workflow

Run this on the weekly cadence. Same reads, different output:

1. Re-confirm the North Star against the active goal tree; flag any active company goal that no longer reflects reality (recommendation only).
2. List candidate Bets — active goals/projects with their counts of `in_progress` + `todo` issues — and propose the single highest-leverage Bet for the week.
3. Recommend prunes: stale `todo` with no recent activity that should drop to `backlog`, and blockers that need resolving. Recommendations only; route any mutation to `paperclip-admin` or triage.
4. Print a Weekly Focus Card ending with the chosen Bet.

## Focus Card Format

```markdown
## Daily Focus — <date>

North Star: <company goal title> (<goal-id>)
This Week's Bet: <goal/project> — <one line: why it advances the North Star>

★ Today's Highlight: <RL-xxx> <title>
   Why this one: <leverage rationale>
   Advances: <project> -> <goal>

Maintenance (around the Highlight):
- <RL-xxx> <title>

Delegate (route to triage/delegation, not done by you):
- <RL-xxx> <title>

Park (recommend backlog, not this week):
- <RL-xxx> <title>

Filter: "What one thing, done today, makes the rest easier or unnecessary?"
```

## Safety Boundaries

- Read freely: goals, projects, issues, comments, activity.
- Print the card in chat as plain text. A read needs no approval.
- Do not mutate. No status changes, priority bumps, labels, comments, assignment, checkout, or heartbeat invocation. If the operator wants to persist the Highlight or Bet, change priority, park issues to `backlog`, or assign work, present the exact change and route it to `paperclip-admin` (minor edits) or `paperclip-triage` / delegation (making work startable). Say why it crosses out of this skill.

## Stop Conditions

- No company context resolved.
- No active goals, so there is no North Star to anchor to.
- Ambiguous North Star and the operator has not chosen.
- No actionable issues, so there is nothing to make a Highlight from. Report this plainly rather than inventing work.
