# Paperclip Operator Skills

Local operator skills for preparing and operating AFK work in Paperclip through the `paperclipai` CLI.

These skills help a human operator turn fuzzy intent into Paperclip-native goals, projects, parent issues, plans, child issues, triage decisions, and monitoring reports while keeping Paperclip as the source of truth.

## Install

List available skills:

```sh
npx skills add bbengamin/skills --list
```

Install all Paperclip operator skills into the current project:

```sh
npx skills add bbengamin/skills --all
```

Install globally:

```sh
npx skills add bbengamin/skills --all -g
```

Install selected skills:

```sh
npx skills add bbengamin/skills --skill paperclip-setup paperclip-clarify paperclip-record-strategy
```

After installing in a fresh project, run `paperclip-setup`. It checks your `paperclipai` context and can scaffold the shared operator docs into the project after you approve:

```text
AGENTS.md
CONTEXT.md
docs/paperclip-operator/
```

## Skills

- `paperclip-setup` — check local `paperclipai` context and shared operator docs.
- `paperclip-clarify` — run a non-mutating clarification session.
- `paperclip-record-strategy` — create or select the Paperclip planning chain: Goal, Project, Parent Issue, and `plan` document.
- `paperclip-plan-work` — decompose a strategy artifact or parent issue into one level of child issues.
- `paperclip-triage` — review issues for AFK readiness before delegation.
- `paperclip-monitor` — inspect active execution across agents, heartbeats, activity, approvals, costs, and blocked work.

## Workflow

```text
clarify -> record strategy -> plan work -> triage -> monitor -> recursive planning
```

The suite is designed around Paperclip's native hierarchy:

```text
Company -> Goal -> Project -> Issue -> Workspace -> Agent run
```

## Shared References

- `AGENTS.md` — repo-level operating rules.
- `CONTEXT.md` — glossary.
- `docs/paperclip-operator/control-plane.md` — Paperclip entities and lifecycle.
- `docs/paperclip-operator/workflow.md` — skill workflow.
- `docs/paperclip-operator/afk-readiness.md` — readiness rules for AFK issues.
- `docs/paperclip-operator/cli-contract.md` — `paperclipai` usage contract.
- `docs/paperclip-operator/integration-matrix.md` — MCP/CLI/REST operation matrix.
- `docs/paperclip-operator/paperclip-docs-index.md` — upstream Paperclip docs index.

These docs are bundled inside `paperclip-setup` as templates so they can be copied into fresh projects.

## Principles

- Paperclip is the source of truth.
- Operator skills inspect before mutating.
- Mutations require operator approval.
- `backlog` means not ready or parked.
- `todo` means ready and actionable.
- Plan one child-issue level at a time.
- Use `blockedByIssueIds` for real dependencies.
