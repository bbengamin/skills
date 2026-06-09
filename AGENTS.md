# Agent Skills

This repository contains local operator skills for preparing and operating AFK work in Paperclip through the `paperclipai` CLI.

## Paperclip Operator Skills

Use the Paperclip operator suite when the user wants to turn fuzzy intent into Paperclip-native goals, projects, issues, plans, triage decisions, monitoring reports, ad hoc admin changes, or agent creation.

Shared references:

- `CONTEXT.md` — glossary only. Do not put implementation decisions here.
- `docs/paperclip-operator/control-plane.md` — Paperclip entities and hierarchy.
- `docs/paperclip-operator/workflow.md` — operator workflow and skill map.
- `docs/paperclip-operator/afk-readiness.md` — issue readiness rules.
- `docs/paperclip-operator/cli-contract.md` — how skills call `paperclipai`.
- `docs/paperclip-operator/integration-matrix.md` — MCP/CLI/REST surface matrix.
- `docs/paperclip-operator/paperclip-docs-index.md` — upstream docs used by this suite.

## Creator Growth Operator Skills

Use the Creator Growth operator suite when the user wants to turn creator-led distribution intent into creator strategy, channel/campaign plans, backlog work items, and AFK-readiness decisions.

Creator Growth skills use Paperclip as the source of truth, but they are domain skills for personal-brand and creator-growth workflows. Use `creator-*` for creator strategy and campaign planning; use `paperclip-*` for generic Paperclip control-plane operations.

Shared references:

- `CONTEXT.md` — glossary only. Do not put implementation decisions here.
- `docs/creator-operator/workflow.md` — Creator Growth workflow and skill map.
- `docs/creator-operator/control-plane.md` — Paperclip entity model for creator strategy, periods, campaigns, and work items.
- `docs/creator-operator/afk-readiness.md` — creator work readiness rules.
- `docs/paperclip-operator/cli-contract.md` — how skills call `paperclipai`.
- `docs/paperclip-operator/integration-matrix.md` — MCP/CLI/REST surface matrix.

## Operating Rules

- Paperclip is the source of truth for goals, projects, issues, comments, approvals, activity, assignments, and skill attachments.
- Local operator skills may inspect Paperclip freely, but must ask before mutating the control plane.
- Prefer Paperclip-native lifecycle state over parallel local ledgers: `backlog` is parked, `todo` is ready/actionable, `blockedByIssueIds` are first-class blockers.
- Plan recursively. Create one child-issue level at a time, and treat broad children as planning parents for later passes.
- Keep phase boundaries strict: planning creates backlog, unassigned structure only; triage may recommend `todo`; delegation may assign or checkout approved work. Do not manually invoke another agent's heartbeat; Paperclip's heartbeat policy handles pickup after assignment.
- Use `paperclip-admin` for narrow reads, minor approved mutations, existing-agent administration, and company skill-library maintenance outside the planning chain.
- Use `paperclip-create-agent` for creating, hiring, drafting, or provisioning new Paperclip agents.
- Use `creator-clarify`, `creator-record-strategy`, `creator-plan-work`, and `creator-triage` for the v1 Creator Growth workflow. Defer creator verification, reflection, scheduling, and publishing skills until planned separately.
- Use `growth-clarify`, `growth-record-strategy`, `inbound-plan-work`, `outbound-plan-work`, `inbound-triage`, and `outbound-triage` for shared acquisition strategy and branch-specific growth planning. Outbound triage is level-aware; it must not send outreach, launch campaigns, mutate CRM records, spend credits, or modify external accounts.

## Growth Operator Skills

Use the Growth operator suite when the user wants to create or revise a shared acquisition strategy that aligns inbound and outbound work before branching into channel-specific or outbound-motion-specific planning.

Growth skills use Paperclip as the source of truth. Use `growth-clarify` and `growth-record-strategy` for shared acquisition strategy, company/team goal trees, durable channel or motion projects, and strategy parent issues. Use `inbound-plan-work` for inbound/channel planning and `outbound-plan-work` for outbound planning after the shared strategy exists. Use `inbound-triage` and `outbound-triage` for branch-specific readiness decisions before delegation. Use `growth-tooling-scout` before adopting, integrating, extending, or building acquisition tooling.

Shared references:

- `CONTEXT.md` — glossary only. Do not put implementation decisions here.
- `docs/growth-operator/workflow.md` — Growth workflow and skill map.
- `docs/growth-operator/control-plane.md` — Paperclip entity model for acquisition goals, channel/motion projects, strategy issues, and branch planning.
- `docs/growth-operator/afk-readiness.md` — shared inbound/outbound planning readiness rules.
- `docs/growth-operator/tooling-scout.md` — growth tooling evaluation and build-vs-buy rubric.
- `docs/paperclip-operator/cli-contract.md` — how skills call `paperclipai`.
- `docs/paperclip-operator/integration-matrix.md` — MCP/CLI/REST surface matrix.
