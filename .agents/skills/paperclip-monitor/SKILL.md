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
7. For recently assigned work, distinguish healthy dispatch (`wake queued`, queued/running run, or `workspace ready`) from skipped/failed dispatch. Treat healthy queued or running pickup as success, not an intervention target.
8. Summarize attention items in priority order. Done when every blocked, `in_review`, pending-approval, errored-agent, and explicitly skipped/failed-dispatch item appears in the report or is explicitly noted as none.

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
- investigate an explicitly skipped or failed dispatch
- reassign work
- pause, resume, or terminate agents

Do not recommend comments, heartbeat/resume, reassignments, workspace/environment changes, or interrupts merely because a wake is queued, a run is active, or a workspace has become ready. Comments during queued/running execution are work injection. An interrupt may create an automatic retry, so any correction plan must wait for the active run and every retry to become terminal before unassigning or reassigning.

## Mutation Rule

Monitoring is read-only by default. Ask before any Paperclip mutation.
