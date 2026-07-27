# Agent Skills

This repository contains local operator skills for preparing and operating AFK work in Paperclip through the `paperclipai` CLI, Paperclip MCP fallback, and API fallback surfaces.

## Paperclip Operator Skills

Use the Paperclip operator suite when the user wants to turn fuzzy intent into Paperclip-native goals, projects, issues, plans, triage decisions, monitoring reports, ad hoc admin changes, or agent creation.

Shared references:

- `CONTEXT.md` — glossary only. Do not put implementation decisions here.
- `docs/paperclip-operator/control-plane.md` — Paperclip entities and hierarchy.
- `docs/paperclip-operator/workflow.md` — operator workflow and skill map.
- `docs/paperclip-operator/afk-readiness.md` — issue readiness rules.
- `docs/paperclip-operator/cli-contract.md` — how skills choose CLI, MCP, MCP API request, and direct REST surfaces.
- `docs/paperclip-operator/integration-matrix.md` — CLI/MCP/API fallback surface matrix.
- `docs/paperclip-operator/paperclip-docs-index.md` — upstream docs used by this suite.

## Operating Rules

- Root `AGENTS.md`, `CONTEXT.md`, and `docs/**` are the authored sources for shared skill references. Do not edit generated `.agents/skills/*/references/` copies directly; update `skill-references.json`, run `python3 scripts/sync_skill_references.py`, and verify with `--check`.
- Paperclip is the source of truth for goals, projects, issues, comments, approvals, activity, assignments, and skill attachments.
- Local operator skills may inspect Paperclip freely, but must ask before mutating the control plane.
- `paperclip-setup` installs Paperclip MCP config project-locally by default after explicit approval; global MCP install is allowed only when the operator asks for it.
- Prefer Paperclip-native lifecycle state over parallel local ledgers: `backlog` is parked, `todo` is ready/actionable, `blockedByIssueIds` are first-class blockers.
- Paperclip issue reviewers are native execution-policy review stages: use `executionPolicy.stages[].participants`, not `reviewRequest`, and verify the field after mutation.
- Executors submit reviewed work by transitioning to `done`; Paperclip intercepts the transition, moves the issue to `in_review`, and routes the active `executionState` participant. Use `request_confirmation` interactions for ordinary issue-scoped yes/no or plan decisions, and formal Approvals for governed actions.
- Plan recursively. Create one child-issue level at a time, and treat broad children as planning parents for later passes.
- Keep phase boundaries strict: planning creates backlog, unassigned structure only; triage may recommend `todo`; delegation prepares the full handoff and reviewer policy while unassigned, then assigns exactly once. Assignment is the dispatch trigger. After Paperclip reports a queued or running wake, observe read-only; do not invoke heartbeat/resume, mention the agent, comment, reassign, or alter workspace/environment unless a material correction is explicitly approved and all live runs and recovery actions have settled.
- Use `paperclip-admin` for narrow reads, minor approved mutations, prepared assignment handoffs, existing-agent administration, and company skill-library maintenance outside the planning chain.
- Use `paperclip-daily-focus` for read-only daily or weekly operator prioritization: derive a North Star, Weekly Bet, and Daily Highlight from the goal tree and actionable issues, then print a plain-text Focus Card. It mutates nothing; persisting a Highlight or re-prioritizing routes to `paperclip-admin` or triage.
- Use `paperclip-create-agent` for creating, hiring, drafting, or provisioning new Paperclip agents.
- Use `paperclip-wiki-fetch` when reading Paperclip llm-wiki page content, listing wiki pages or sources, or converting wiki SPA URLs into plugin bridge API requests.
- Use `paperclip-wiki-manage` when creating, updating, renaming, archiving, deleting, or otherwise mutating Paperclip llm-wiki content. Wiki management must use confirmed plugin bridge write routes, explicit approval, and readback verification.
- Use `growth-clarify`, `growth-record-strategy`, `inbound-plan-work`, `outbound-plan-work`, `inbound-triage`, and `outbound-triage` for shared acquisition strategy and branch-specific growth planning. Outbound triage is level-aware; it must not send outreach, launch campaigns, mutate CRM records, spend credits, or modify external accounts.

## Growth Operator Skills

Use the Growth operator suite when the user wants to create or revise a shared acquisition strategy that aligns inbound and outbound work before branching into channel-specific or outbound-motion-specific planning.

Growth skills use Paperclip as the source of truth. Use `growth-clarify` and `growth-record-strategy` for shared acquisition strategy, company/team goal trees, durable channel or motion projects, and strategy parent issues. Use `inbound-plan-work` for inbound/channel planning and `outbound-plan-work` for outbound planning after the shared strategy exists. Use `inbound-triage` and `outbound-triage` for branch-specific readiness decisions before delegation.

Shared references:

- `CONTEXT.md` — glossary only. Do not put implementation decisions here.
- `docs/growth-operator/workflow.md` — Growth workflow and skill map.
- `docs/growth-operator/control-plane.md` — Paperclip entity model for acquisition goals, channel/motion projects, strategy issues, and branch planning.
- `docs/growth-operator/afk-readiness.md` — shared inbound/outbound planning readiness rules.
- `docs/paperclip-operator/cli-contract.md` — how skills choose CLI, MCP, MCP API request, and direct REST surfaces.
- `docs/paperclip-operator/integration-matrix.md` — CLI/MCP/API fallback surface matrix.
