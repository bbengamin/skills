# AFK Readiness

AFK-ready work is Paperclip work that can be delegated to an agent without the operator watching every step.

## Canonical Signal

An issue is ready for AFK execution when:

- status is `todo`
- project is set
- parent issue is set when it belongs to a larger plan
- title is specific and action-oriented
- description contains the execution brief
- acceptance criteria are explicit
- scope and non-goals are clear
- validation path is clear
- unresolved blockers are represented with `blockedByIssueIds`
- required plan or board decision exists before execution
- assignee expectations are clear, even if the assignee is not chosen yet
- stop conditions are explicit

`backlog` means identified but not ready/startable. `todo` is the ready/actionable state.

## Triage Classes

**AFK-ready**: Move or keep in `todo`. The issue can enter the agent loop.

**Needs info**: Keep in `backlog` or move to `blocked` if it is already in flight. Ask specific questions in a comment.

**Blocked**: Use `blockedByIssueIds` for concrete blockers. Add a comment naming the unblock owner and action.

**Needs human**: The work requires judgment, external authority, credentials, or approval before an agent can continue.

**Too broad**: Keep as a planning parent. Run `paperclip-plan-work` recursively to create children.

**Revise**: The issue has a workable shape but the brief, criteria, plan, or dependencies need edits before `todo`.

**Cancel**: The work should not proceed.

**Done**: The work is complete or already satisfied.

## Recommended Issue Brief

Use this shape for AFK-ready issue descriptions:

```markdown
## Context

Why this issue exists and how it connects to the parent strategy.

## What to do

The concrete outcome the agent should produce.

## Acceptance criteria

- [ ] Observable criterion 1
- [ ] Observable criterion 2
- [ ] Observable criterion 3

## Constraints

Scope limits, non-goals, safety rules, budget limits, or technical boundaries.

## Validation

How the agent should prove the work is complete.

## Stop conditions

When the agent should stop and ask the board instead of continuing.
```
