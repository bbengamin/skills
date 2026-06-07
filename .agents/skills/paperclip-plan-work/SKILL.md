---
name: paperclip-plan-work
description: Decompose a Paperclip strategy artifact or parent issue into one level of child issues. Use when converting a Paperclip plan into AFK-ready issues or planning parent issues.
---

# Paperclip Plan Work

Plan one child-issue level at a time. Do not produce a fully expanded multi-level issue tree.

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
3. Propose one level of child issues.
4. Classify each proposed child:
   - AFK-ready
   - planning parent
   - needs-human
   - blocked
   - needs-info
5. Show the proposed breakdown and ask for approval.
6. After approval, create issues in dependency order.
7. For planning parent issues, ask whether to run another planning iteration on each one.

## Proposed Breakdown Format

```markdown
## Proposed Child Issues

### 1. <title>

- Type: AFK-ready | planning parent | needs-human | blocked | needs-info
- Priority:
- Blocked by:
- Acceptance criteria:
- Validation:
- Stop conditions:
```

## Creation Rules

- Create AFK-ready issues as `todo` only when they satisfy the AFK readiness rules.
- Create planning parent issues as `backlog`.
- Use `parentId` to link children to the parent.
- Use `blockedByIssueIds` for dependencies.
- Do not assign broad planning parent issues to execution agents.
- Add a comment explaining planning decisions when useful.

## Mutation Rule

Never create child issues until the operator approves the proposed breakdown.
