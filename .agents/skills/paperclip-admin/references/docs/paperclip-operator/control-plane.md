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

Interrupt/cancel is not a neutral pause: Paperclip may create process recovery. Separately, a missing required issue comment may create one comment retry. A correction is safe only after live runs and relevant recovery actions are settled. Then the operator may unassign, repair configuration, verify quiescence, and assign once again.

Run records do not replace issue lifecycle. Inspect `paperclipai issue runs`, `live-runs`, `active-run`, and `recovery-actions` before intervening. Newer builds may expose additional run-liveness or continuation metadata; feature-detect it from the returned schema instead of assuming canary fields exist in stable environments.

## Runtime Entities

**Agent** is a configured AI worker with a role, manager, adapter, budget, skills, and heartbeat policy.

**Heartbeat** is the execution window where an agent wakes, checks work, checks out an issue, acts, comments, and exits.

**Adapter** connects Paperclip to the runtime that executes the agent, such as Codex local or Claude local.

**Skill** is a reusable instruction package installed in the Paperclip company skill library and attached to agents.

**Approval** is a board-review gate. Common types include CEO strategy approval, hire approval, budget override, and general board approval.

**Budget** is an enforced spending cap at company, agent, or project scope.

## Issue Review Gates

Paperclip's issue reviewer UI is backed by `executionPolicy.stages[].participants`, not `reviewRequest`.

To require an agent reviewer, set an issue `executionPolicy` with `mode: "normal"`, `commentRequired: true`, and a `review` stage. Comment-required is a runtime backstop for issue-bound agent runs, not merely a reviewer preference:

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

Use `type: "user"` with the native user id for human reviewers or approvers. Approval stages use `type: "approval"`; stages are ordered, and current stable Paperclip supports one required approval per stage. Read the issue back after writing and verify the participants in `executionPolicy.stages`.

The executor submits work by transitioning the issue to `done`, not by manually assigning a reviewer or setting `in_review`. The runtime intercepts `done`, moves the issue to `in_review`, sets `executionState.status: "pending"`, records `currentStageType` and `currentParticipant`, and assigns/wakes the selected participant. An approving participant also transitions to `done` with a required comment; the runtime either advances to the next stage or reaches actual `done`. A change request returns the issue to the original executor through `executionState.returnAssignee`.

Use `executionState` to diagnose review routing. Do not treat a `reviewRequest` field as equivalent unless current Paperclip API documentation explicitly says it is mapped by that environment.

## Issue Documents And Interactions

Issue documents are keyed, revisioned artifacts such as `plan`, `design`, or `notes`. Read and write them with native CLI document commands when available. Updates should include the current base revision so stale writes fail instead of overwriting concurrent edits.

Issue-thread interactions are structured decision cards. Use `request_confirmation` for ordinary issue-scoped yes/no decisions and plan approval, bound to the exact document revision with an idempotency key. Use formal Approvals for governed actions such as hires, strategy gates, spend, or security-sensitive changes. A normal comment is not a substitute for a structured confirmation when acceptance controls continuation.

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
