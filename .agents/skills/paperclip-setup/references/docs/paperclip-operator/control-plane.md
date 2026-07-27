# Paperclip Control Plane

Paperclip is an AI organisation control plane. Operator skills should use these entities as the native structure instead of inventing a parallel task system.

## Planning Hierarchy

```text
Company -> Goal tree -> Project -> Issue -> Workspace -> Agent run
```

**Company** is the top-level organisation. It owns the company goal, agents, issues, approvals, budgets, skills, routines, projects, and activity log.

**Goal** is the why. A goal is an outcome statement. It does not get worked directly. Projects link to goals. Paperclip goals have `level`, `status`, optional `parentId`, and optional `ownerAgentId`.

Goal levels are native Paperclip structure:

- `company` - top-level durable company outcome. Prefer an active root company goal for the main north star.
- `team` - durable team, domain, motion, or functional outcome under a company goal.
- `agent` - outcome owned by a specific Paperclip agent; set `ownerAgentId` when ownership is real.
- `task` - narrow goal-like outcome. Use sparingly; most execution units should be Issues instead.

Use `parentId` for goal hierarchy instead of encoding hierarchy only in titles or descriptions. Do not create goals for every campaign, month, sprint, lead list, content draft, or task unless the operator explicitly wants that level represented as a goal.

**Project** is the concrete deliverable container. It groups issues, workspaces, runtime configuration, project budget, and links to one or more goals.

**Issue** is the executable work object. It has status, priority, description, comments, parent/child relationships, blockers, labels, assignees, documents, approvals, execution policy, and activity.

**Parent Issue** is an issue that owns child issues. When paired with a `plan` document, it can serve as the strategy artifact for a body of work.

**Workspace** is the execution environment for project issues. It may be a local folder, git repository, managed remote workspace, or isolated worktree.

**Agent run** is a heartbeat execution tied to an agent, issue, and often a checkout run id.

Assignment is an event-producing dispatch trigger. Changing an eligible issue from unassigned to an executor creates the assignment wake; it is not necessary to invoke heartbeat/resume, mention the agent, or repeat assignment. `wake queued`, a queued/running run, and `workspace ready` are healthy pickup states and should be observed read-only.

Comments added after dispatch are work injection. They may appear as separate queued interactions and change what the active agent receives. Configure the complete issue handoff and reviewer policy before assignment.

Interrupt/cancel is not a neutral pause: Paperclip may create an automatic retry. A correction is safe only after the active run and every retry are terminal. Then the operator may unassign, repair configuration, verify quiescence, and assign once again.

## Runtime Entities

**Agent** is a configured AI worker with a role, manager, adapter, budget, skills, and heartbeat policy.

**Heartbeat** is the execution window where an agent wakes, checks work, checks out an issue, acts, comments, and exits.

**Adapter** connects Paperclip to the runtime that executes the agent, such as Codex local or Claude local.

**Skill** is a reusable instruction package installed in the Paperclip company skill library and attached to agents.

**Approval** is a board-review gate. Common types include CEO strategy approval, hire approval, budget override, and general board approval.

**Budget** is an enforced spending cap at company, agent, or project scope.

## Issue Review Gates

Paperclip's issue reviewer UI is backed by `executionPolicy.stages[].participants`, not `reviewRequest`.

To require an agent reviewer, set an issue `executionPolicy` with `mode: "normal"`, `commentRequired: true` when the reviewer must leave a comment, and a `review` stage:

```json
{
  "executionPolicy": {
    "mode": "normal",
    "commentRequired": true,
    "stages": [
      {
        "type": "review",
        "approvalsNeeded": 1,
        "participants": [
          {
            "type": "agent",
            "agentId": "<reviewer-agent-id>"
          }
        ]
      }
    ]
  }
}
```

Use `type: "user"` with the native user id for human reviewers when supported by the target Paperclip environment. Read the issue back after writing and verify the reviewer appears in `executionPolicy.stages[].participants`. Do not treat a `reviewRequest` field as equivalent unless current Paperclip API documentation explicitly says it is mapped by that environment.

## Issue Lifecycle

Paperclip issue statuses are lifecycle state:

- `backlog` — parked, unscheduled, not picked up by default.
- `todo` — ready and actionable; waiting for agent checkout.
- `in_progress` — checked out by one agent/run.
- `in_review` — paused for reviewer, approver, board, or user feedback.
- `blocked` — cannot proceed until a named blocker is resolved.
- `done` — complete and terminal.
- `cancelled` — intentionally abandoned and terminal.

Use `blockedByIssueIds` for dependencies. A free-text blocked comment is not enough because Paperclip cannot auto-wake dependents when blockers resolve.
