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
6. For active or recently assigned issues, use `paperclipai issue live-runs`, `active-run`, `runs`, and `recovery-actions` with `--json` when available. Distinguish queued delivery, process recovery, missing-comment retry, and explicit recovery actions instead of labeling all follow-up runs as generic retries. Feature-detect additional run-liveness fields in newer environments.
7. Read activity for recent significant events.
8. For recently assigned work, distinguish healthy dispatch (`wake queued`, queued/running run, or `workspace ready`) from skipped/failed dispatch. Treat healthy queued or running pickup as success, not an intervention target.
9. For review-stage issues, inspect `executionState.currentStageType`, `currentParticipant`, and `returnAssignee` when available. The executor normally submits by transitioning to `done`; Paperclip owns the resulting `in_review` routing to the agent reviewer. When human final acceptance is required, also inspect issue interactions: a pending `request_confirmation` is healthy waiting state, while accepted/rejected interactions with failed resume or no reviewer follow-through need attention. A user approval-stage participant is a flow defect, not a reason to tell the operator to use CLI.
10. Summarize attention items in priority order. Done when every blocked, `in_review`, pending-approval, errored-agent, unresolved recovery action, and explicitly skipped/failed-dispatch item appears in the report or is explicitly noted as none.

## Report Format

```markdown
## Paperclip Monitor Report

### Needs Operator Attention

### Blocked Work

### Pending Reviews And Approvals

### Run And Recovery State

### Agent Health

### Cost And Budget Signals

### Recent Progress

### Recommended Actions
```

## Action Recommendations

Recommend but do not perform mutations:

- approve, reject, or request revision
- accept or reject a pending issue `request_confirmation`
- move issue status
- add comments
- create blockers
- investigate an explicitly skipped or failed dispatch
- reassign work
- pause, resume, or terminate agents

Do not recommend comments, heartbeat/resume, reassignments, workspace/environment changes, or interrupts merely because a wake is queued, a run is active, or a workspace has become ready. Comments during queued/running execution are work injection. An interrupt may create process recovery, and missing required comments may create one comment retry. Any correction plan must wait for all live runs and relevant recovery actions to settle before unassigning or reassigning.

## Mutation Rule

Monitoring is read-only by default. Ask before any Paperclip mutation.
