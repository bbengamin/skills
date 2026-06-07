# Agent Skills

This repository contains local operator skills for preparing and operating AFK work in Paperclip through the `paperclipai` CLI.

## Paperclip Operator Skills

Use the Paperclip operator suite when the user wants to turn fuzzy intent into Paperclip-native goals, projects, issues, plans, triage decisions, or monitoring reports.

Shared references:

- `CONTEXT.md` — glossary only. Do not put implementation decisions here.
- `docs/paperclip-operator/control-plane.md` — Paperclip entities and hierarchy.
- `docs/paperclip-operator/workflow.md` — operator workflow and skill map.
- `docs/paperclip-operator/afk-readiness.md` — issue readiness rules.
- `docs/paperclip-operator/cli-contract.md` — how skills call `paperclipai`.
- `docs/paperclip-operator/integration-matrix.md` — MCP/CLI/REST surface matrix.
- `docs/paperclip-operator/paperclip-docs-index.md` — upstream docs used by this suite.

## Operating Rules

- Paperclip is the source of truth for goals, projects, issues, comments, approvals, activity, assignments, and skill attachments.
- Local operator skills may inspect Paperclip freely, but must ask before mutating the control plane.
- Prefer Paperclip-native lifecycle state over parallel local ledgers: `backlog` is parked, `todo` is ready/actionable, `blockedByIssueIds` are first-class blockers.
- Plan recursively. Create one child-issue level at a time, and treat broad children as planning parents for later passes.
