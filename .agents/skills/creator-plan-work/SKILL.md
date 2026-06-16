---
name: creator-plan-work
description: Split a Creator Growth strategy or campaign artifact into one level of Paperclip backlog work items. Use when planning creator strategy periods, channel campaigns, LinkedIn/content work, or creator-led distribution tasks before triage or AFK execution.
---

# Creator Plan Work

Plan one child-issue level at a time from a selected creator strategy or campaign issue.

Planning creates `backlog`, unassigned structure. It does not make work startable.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/creator-operator/workflow.md`
- `references/docs/creator-operator/control-plane.md`
- `references/docs/creator-operator/afk-readiness.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

## Process

1. Identify the target creator strategy or campaign parent issue.
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

## Wiki Source Material

When the parent issue, plan document, comments, or operator prompt reference a Paperclip wiki URL, wiki page path, or captured wiki source, use `paperclip-wiki-fetch` before proposing creator child issues. Carry the relevant fetched source title, path, update time, hash, and proof snippets into proposed issue bodies when they affect topic, hypothesis, source material, or research targets.

If the wiki reference cannot be fetched because credentials, company scope, wiki id, space slug, or page path are missing, pause planning and ask for the missing input. Do not create child issues that depend on inaccessible wiki material.

If the operator explicitly asks to publish, sync, or update wiki content from creator planning output, finish the proposed breakdown first, then use `paperclip-wiki-manage` for the wiki mutation after approval.

## Planning Patterns

Examples:

- Yearly strategy -> quarterly strategy parent issues.
- Quarterly strategy -> monthly strategy parent issues.
- Monthly strategy -> channel/campaign parent issues.
- LinkedIn campaign -> research, angle, draft, revision, and signal-capture work items.
- LinkedIn campaign calendar -> one `backlog` `creator-post` issue per planned post, each with `targetSlotAt`, `draftWindow`, `channel: LinkedIn`, `postizMode: create-draft-only`, source refs, brief, acceptance criteria, and final-URL done definition.

Create broad children as planning parents, not execution-ready issues.

When planning campaign posts, do not move future posts to `todo` and do not assign Creator Drafter. Future posts are queued in `backlog`; the Creator Queue Steward routine promotes due `creator-post` issues later.

## Proposed Breakdown Format

```markdown
## Proposed Creator Child Issues

### 1. <title>

- Type: ready-looking | planning parent | needs-human | blocked | needs-info
- Priority:
- Status to write: backlog
- Parent:
- Project:
- Blocked by:
- Assignee: null
- Creator/persona:
- Channel:
- Labels:
- targetSlotAt:
- draftWindow:
- postizMode:
- Body:
- Acceptance criteria:
- Validation:
- Stop conditions:
```

## Creation Rules

- Create planned issues as `backlog` and unassigned.
- Add the `creator-post` label to individual campaign post issues that should enter the scheduled drafting queue.
- Do not move issues to `todo`.
- Do not assign agents.
- Do not checkout work.
- Do not manually invoke heartbeats.
- Use `parentId`/native parent linkage and verify it after creation.
- Use first-class `blockedByIssueIds` for concrete dependencies when available.
- Do not replace plan documents or blocker links with comments unless the operator explicitly approves degraded mode.

## Mutation Rule

Never create child issues until the operator approves the proposed breakdown.
