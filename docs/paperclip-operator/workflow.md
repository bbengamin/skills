# Paperclip Operator Workflow

The operator workflow moves from human intent to AFK execution while keeping Paperclip as the source of truth.

```text
clarify -> record strategy -> plan work -> triage -> monitor -> recursive planning
```

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

Some proposed children may be AFK-ready. Others may be planning parent issues that need a later recursive planning pass.

## 4. Triage

Use `paperclip-triage` to decide whether existing issues are good enough for AFK execution. Triage is issue-centered and recommendation-first.

It classifies issues as AFK-ready, needs-info, blocked, needs-human, too-broad, revise, cancel, or done.

## 5. Monitor

Use `paperclip-monitor` to inspect active execution. It reads dashboard, agents, issues, approvals, activity, costs, blocked work, and heartbeats.

Monitoring is read-only by default. Any proposed mutation needs operator approval.

## 6. Recursive Planning

When a child issue is too broad, keep it in `backlog` as a planning parent. Run `paperclip-plan-work` on it later to create the next child level.
