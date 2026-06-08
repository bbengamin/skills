# Paperclip Operator Workflow

The operator workflow moves from human intent to AFK execution while keeping Paperclip as the source of truth.

```text
clarify -> record strategy -> plan work -> triage -> delegate/monitor -> recursive planning
```

For narrow administration requests that do not need the full planning chain, use `paperclip-admin` instead. It handles ad hoc reads, minor approved mutations, existing-agent administration, and company skill-library maintenance. For new agents, use `paperclip-create-agent`.

## 0. Admin

Use `paperclip-admin` when the operator asks to check something, make a small control-plane change, update an existing agent, inspect or attach company skills, adjust assignments, or perform one-off maintenance.

Use `paperclip-create-agent` when the operator asks to create, hire, provision, draft, or configure a new Paperclip agent. Agent creation follows Paperclip's native governance-aware hire workflow: inspect context and org conventions, draft role/config/instructions, ask for approval, create or submit the hire, verify the record, then set up local CLI/runtime access only after creation is valid.

Admin and create-agent flows may inspect freely. Any mutation still requires operator approval, and agent creation must never be a side effect of planning.

## 1. Clarify

Use `paperclip-clarify` when intent is still fuzzy. It interviews the operator one question at a time and produces a non-mutating clarification summary.

Clarification is intentionally rigorous. Do not stop after a shallow pass. Continue until outcome, scope, validation, autonomy, risks, and stop conditions are concrete enough to create a Paperclip strategy artifact.

Resolve:

- goal and desired outcome
- success criteria
- scope and non-goals
- constraints and risks
- autonomy level
- validation expectations
- open questions

## 2. Record Strategy

Use `paperclip-record-strategy` after the clarification summary is approved. It creates or selects the missing planning chain:

```text
Goal -> linked Project -> Parent Issue + plan document
```

The result is a Paperclip-native strategy artifact.

## 3. Plan Work

Use `paperclip-plan-work` on a strategy artifact or parent issue. It proposes one child-issue level at a time and waits for approval before creating issues.

Planning creates backlog structure only. Proposed children may look complete enough for later triage, but this phase must not move issues to `todo`, assign agents, checkout work, or otherwise make work startable.

Others may be planning parent issues that need a later recursive planning pass. If the breakdown produces many uncertain children, pause for focused Q&A before creating issue records.

## 4. Triage

Use `paperclip-triage` to decide whether existing issues are good enough for AFK execution. Triage is issue-centered and recommendation-first.

It classifies issues as AFK-ready, needs-info, blocked, needs-human, too-broad, revise, cancel, or done.

Triage is the first phase that may recommend moving backlog work to `todo`; it still waits for approval before mutating lifecycle, blockers, labels, comments, or assignees.

## 5. Delegate And Monitor

Delegation starts only after explicit operator intent. It may assign or checkout approved issues, then Paperclip's heartbeat loop handles agent pickup. Do not manually invoke another agent's heartbeat; Paperclip rejects cross-agent invocation and assignments are enough for eligible agents with heartbeat policy enabled.

Use `paperclip-monitor` to inspect active execution. It reads dashboard, agents, issues, approvals, activity, costs, blocked work, and heartbeats.

Monitoring is read-only by default. Any proposed mutation needs operator approval.

## 6. Recursive Planning

When a child issue is too broad, keep it in `backlog` as a planning parent. Run `paperclip-plan-work` on it later to create the next child level.
