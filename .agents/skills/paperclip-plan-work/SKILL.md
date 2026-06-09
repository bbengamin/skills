---
name: paperclip-plan-work
description: Decompose a Paperclip strategy artifact or parent issue into one level of backlog child issues. Use when turning a Paperclip plan into planned issue structure or planning parent issues, before triage or delegation.
---

# Paperclip Plan Work

Plan one child-issue level at a time. Do not produce a fully expanded multi-level issue tree.

Planning is not execution. This skill may classify whether proposed children look ready for later triage, but it must not make them startable. Create planned issues as `backlog` and unassigned unless the operator explicitly switches to `paperclip-triage` or a delegation workflow.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/workflow.md`
- `../../../docs/paperclip-operator/afk-readiness.md`
- `../../../docs/paperclip-operator/cli-contract.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Process

1. Identify the parent strategy issue or parent issue.
2. Read the issue, parent chain, project, plan document, blockers, and comments.
3. Run a Paperclip surface preflight.
4. Propose one level of child issues.
5. Classify each proposed child:
   - ready-looking
   - planning parent
   - needs-human
   - blocked
   - needs-info
6. If more than two proposed children are `needs-human`, `blocked`, `needs-info`, or broad planning parents, pause for a focused Q&A/grilling pass before creating issues.
7. Include the exact title, body, status, parent, project, goal, blocker links, and assignee that will be written for each issue.
8. Show the proposed breakdown and ask for approval.
9. After approval, create issues in dependency order.
10. For planning parent issues, ask whether to run another planning iteration on each one.

## Surface Preflight

Before proposing mutations, confirm the writable surface for:

- active company and company id
- issue create/update
- child issue parent linkage
- issue status update, only for keeping planned work in `backlog`
- `blockedByIssueIds`
- plan document read/write, when plan documents are involved
- MCP API request or direct REST availability if CLI and dedicated MCP tools cannot write the required native field

Use `paperclipai context show --json`, `paperclipai auth whoami --json`, and `~/.paperclip/auth.json` only to derive API connection details. Never print bearer tokens. If a required native field cannot be written, stop and report the missing capability. Do not replace first-class blockers, parent links, or plan documents with comments unless the operator explicitly approves that degraded mode.

## Proposed Breakdown Format

```markdown
## Proposed Child Issues

### 1. <title>

- Type: ready-looking | planning parent | needs-human | blocked | needs-info
- Priority:
- Status to write: backlog
- Parent:
- Project:
- Goal:
- Blocked by:
- Assignee: null
- Body:
- Acceptance criteria:
- Validation:
- Stop conditions:
```

## Creation Rules

- Planning creates `backlog` and unassigned issues only.
- Do not create or update `todo`, assign agents, checkout work, or manually invoke heartbeats from this skill.
- Treat `todo` as operationally active; it may trigger pickup. Only `paperclip-triage` or an explicit delegation workflow may move planned work to `todo`.
- Preserve operator intent: "plan", "break down", or "create the structure" means backlog structure, not execution.
- Create planning parent issues as `backlog`.
- Use `parentId` or the current surface's native parent field to link children to the parent. If using MCP, confirm the exposed tool schema and verify that parent linkage persists in the created record.
- Use MCP `paperclipApiRequest` for `blockedByIssueIds` unless CLI or a dedicated MCP issue tool exposes and verifies the field.
- Do not assign any planning-created issue to an execution agent.
- Add a comment explaining planning decisions when useful.

## Mutation Transaction Discipline

Paperclip does not expose an obvious multi-issue transaction through the current operator surfaces. For multi-issue creation:

1. Create one issue.
2. Immediately verify:
   - `parentId` matches the expected parent
   - `projectId` matches the target project
   - `goalId` is inherited or linked correctly
   - `status` is `backlog`
   - assignee is null
   - `blockedByIssueIds` links exist when expected
3. Repair structural mismatches through CLI, MCP, `paperclipApiRequest`, or direct REST when possible.
4. Do not patch planned issues to `todo`; report ready-looking issues as triage candidates instead.
5. Continue to the next issue only after verification succeeds.

If parent linkage, blocker linkage, project linkage, goal linkage, backlog status, or null assignee cannot be made correct, stop before creating the remaining issues and report the partial state.

## Mutation Rule

Never create child issues until the operator approves the proposed breakdown.
