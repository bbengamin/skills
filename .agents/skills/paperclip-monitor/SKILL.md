---
name: paperclip-monitor
description: Produce read-only Paperclip execution reports across issues, agents, heartbeats, approvals, activity, costs, and blocked work. Use when monitoring AFK loops or asking what needs operator attention.
---

# Paperclip Monitor

Inspect active Paperclip execution and surface what needs operator attention.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/control-plane.md`
- `references/docs/paperclip-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Read-Only Workflow

1. Inspect CLI context and company scope.
2. Read dashboard summary.
3. Read issues, focusing on:
   - `blocked`
   - `in_review`
   - `in_progress`
   - stale `todo`
   - parent issues with unfinished children
4. Read approvals, especially pending and revision-requested.
5. Read agents and note paused, error, running, or budget-blocked states.
6. Read activity for recent significant events.
7. Summarize attention items in priority order. Done when every blocked, `in_review`, pending-approval, and errored-agent item appears in the report or is explicitly noted as none.

## Report Format

```markdown
## Paperclip Monitor Report

### Needs Operator Attention

### Blocked Work

### Pending Reviews And Approvals

### Agent Health

### Cost And Budget Signals

### Recent Progress

### Recommended Actions
```

## Action Recommendations

Recommend but do not perform mutations:

- approve, reject, or request revision
- move issue status
- add comments
- create blockers
- retry agents or manually invoke heartbeats
- reassign work
- pause, resume, or terminate agents

## Mutation Rule

Monitoring is read-only by default. Ask before any Paperclip mutation.
