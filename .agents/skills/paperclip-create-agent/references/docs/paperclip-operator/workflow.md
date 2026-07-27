# Paperclip Operator Workflow

The operator workflow moves from human intent to AFK execution while keeping Paperclip as the source of truth.

```text
clarify -> record strategy -> plan work -> triage -> delegate/monitor -> recursive planning
```

For narrow administration requests that do not need the full planning chain, use `paperclip-admin` instead. It handles ad hoc reads, minor approved mutations, existing-agent administration, and company skill-library maintenance. For new agents, use `paperclip-create-agent`. For Paperclip llm-wiki retrieval, use `paperclip-wiki-fetch`. For Paperclip llm-wiki mutations, use `paperclip-wiki-manage`.

## 0. Admin

Use `paperclip-admin` when the operator asks to check something, make a small control-plane change, update an existing agent, inspect or attach company skills, adjust assignments or reviewer gates, or perform one-off maintenance.

Use `paperclip-create-agent` when the operator asks to create, hire, provision, draft, or configure a new Paperclip agent. Agent creation follows Paperclip's native governance-aware hire workflow: inspect context and org conventions, draft role/config/instructions, ask for approval, create or submit the hire, verify the record, then set up local CLI/runtime access only after creation is valid.

Use `paperclip-wiki-fetch` when the operator asks to read Paperclip llm-wiki page markdown, list wiki pages, list captured wiki sources, or convert a public-looking wiki SPA URL into the plugin bridge REST API request.

Use `paperclip-wiki-manage` when the operator asks to create, update, rename, archive, delete, publish, sync, or otherwise mutate Paperclip llm-wiki content. Wiki management requires a confirmed plugin bridge write route, exact proposed content or diff, explicit approval, and readback verification.

Admin, create-agent, and wiki flows may inspect freely. Any mutation still requires operator approval, and agent creation must never be a side effect of planning.

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
Goal tree -> linked Project -> Parent Issue + plan document
```

The result is a Paperclip-native strategy artifact.

## 3. Plan Work

Use `paperclip-plan-work` on a strategy artifact or parent issue. It proposes one child-issue level at a time and waits for approval before creating issues.

Planning creates backlog structure only. Proposed children may look complete enough for later triage, but this phase must not move issues to `todo`, assign agents, checkout work, or otherwise make work startable.

Others may be planning parent issues that need a later recursive planning pass. If the breakdown produces many uncertain children, pause for focused Q&A before creating issue records.

## 4. Triage

Use `paperclip-triage` to decide whether existing issues are good enough for AFK execution. Triage is issue-centered and recommendation-first.

It classifies issues as AFK-ready, needs-info, blocked, needs-human, too-broad, revise, cancel, or done.

Triage is the first phase that may recommend moving backlog work to `todo`; it still waits for approval before mutating lifecycle, blockers, labels, comments, assignees, or reviewer gates.

## 5. Delegate And Monitor

Delegation starts only after explicit operator intent. Use a prepare-dispatch-observe sequence:

1. Prepare the complete handoff while the issue is unassigned. Read blockers, comments, activity, `live-runs`, `active-run`, recent runs, recovery actions, executor configuration, project workspace, and review policy. Preserve the executor's existing/default environment unless the operator explicitly requests an override. Add the final brief and configure required reviewers through `executionPolicy.stages[].participants`; read the issue back and verify there are no live runs or unresolved recovery actions.
2. Dispatch exactly once. Assign the executor and set `todo` if necessary as the final startable mutation. Assignment creates the wake automatically. Do not also invoke heartbeat/resume, mention the agent, checkout, comment, or create a second assignment wake.
3. Observe read-only. `wake queued`, a queued/running run, or `workspace ready` means pickup succeeded. Do not mutate issue, agent, workspace, environment, policy, or comments while the run is queued/running.
4. The executor submits by transitioning to `done`. Let Paperclip intercept that transition, move the issue to `in_review`, update `executionState`, and route the configured reviewer/approver. Do not manually assign or wake the participant unless Paperclip explicitly reports skipped or failed review dispatch.
5. For a material correction, interrupt/cancel once and wait for live runs, process recovery, comment retries, and relevant recovery actions to settle. Only then unassign, repair, verify, and reassign once.

Hard rule: after Paperclip reports `wake queued`, a queued/running run, or `workspace ready`, switch to read-only observation unless dispatch is explicitly skipped or failed.

Use `paperclip-monitor` to inspect active execution. It reads dashboard, agents, issues, approvals, activity, costs, blocked work, and heartbeats.

Monitoring is read-only by default. Any proposed mutation needs operator approval.

## 6. Recursive Planning

When a child issue is too broad, keep it in `backlog` as a planning parent. Run `paperclip-plan-work` on it later to create the next child level.
