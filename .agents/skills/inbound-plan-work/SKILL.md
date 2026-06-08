---
name: inbound-plan-work
description: Split a shared growth strategy or inbound branch artifact into one level of Paperclip backlog work items for inbound, creator-led, or channel-led acquisition. Use when planning LinkedIn, newsletter, YouTube, content, personal-brand, or trust-building work after growth-record-strategy.
---

# Inbound Plan Work

Plan one child-issue level at a time from a selected growth strategy, inbound branch, or inbound campaign parent issue.

Planning creates `backlog`, unassigned structure. It does not make work startable.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/growth-operator/workflow.md`
- `../../../docs/growth-operator/control-plane.md`
- `../../../docs/growth-operator/afk-readiness.md`
- `../../../docs/paperclip-operator/cli-contract.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

Open creator references when the work is explicitly creator-led:

- `../../../docs/creator-operator/workflow.md`
- `../../../docs/creator-operator/control-plane.md`

## Process

1. Identify the target growth strategy, inbound branch, or inbound campaign parent issue.
2. Read the issue, plan document, parent chain, project, linked goals, blockers, and comments.
3. Confirm the intended planning depth.
4. Propose one level of child issues.
5. Classify each proposed child:
   - ready-looking
   - planning parent
   - needs-human
   - blocked
   - needs-info
6. If more than two proposed children are unclear, pause for focused clarification before creating issues.
7. Include the exact title, body, status, parent, project, blockers, and assignee for each issue.
8. Ask for approval.
9. After approval, create issues in dependency order and verify each record.

## Planning Patterns

Examples:

- Yearly inbound strategy -> quarterly strategy parent issues.
- Quarterly inbound strategy -> monthly strategy parent issues.
- Monthly inbound strategy -> channel campaign parent issues.
- LinkedIn campaign -> source research, angle proposals, draft posts, review revisions, and signal capture.
- Newsletter campaign -> source research, outline, draft, edit, distribution prep, and signal capture.

Create broad children as planning parents, not execution-ready issues.

## Proposed Breakdown Format

```markdown
## Proposed Inbound Child Issues

### 1. <title>

- Type: ready-looking | planning parent | needs-human | blocked | needs-info
- Priority:
- Status to write: backlog
- Parent:
- Project:
- Linked goals:
- Blocked by:
- Assignee: null
- Channel:
- Creator/persona:
- Audience/ICP:
- Wedge or story:
- Source material/proof:
- Body:
- Acceptance criteria:
- Validation:
- Stop conditions:
```

## Creation Rules

- Create planned issues as `backlog` and unassigned.
- Do not move issues to `todo`.
- Do not assign agents.
- Do not checkout work.
- Do not manually invoke heartbeats.
- Do not post, schedule, publish, or modify external accounts.
- Use `parentId`/native parent linkage and verify it after creation.
- Use first-class `blockedByIssueIds` for concrete dependencies when available.
- Do not replace plan documents or blocker links with comments unless the operator explicitly approves degraded mode.

## Mutation Rule

Never create child issues until the operator approves the proposed breakdown.
