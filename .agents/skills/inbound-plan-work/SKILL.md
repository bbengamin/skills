---
name: inbound-plan-work
description: Split a shared growth strategy or inbound branch artifact into one level of Paperclip backlog work items for inbound, personal-brand, content-led, or channel-led acquisition. Use when planning LinkedIn, newsletter, YouTube, content, personal-brand, or trust-building work after growth-record-strategy.
---

# Inbound Plan Work

Plan one child-issue level at a time from a selected growth strategy, inbound branch, or inbound campaign parent issue.

Planning creates `backlog`, unassigned structure. It does not make work startable.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/growth-operator/workflow.md`
- `references/docs/growth-operator/control-plane.md`
- `references/docs/growth-operator/afk-readiness.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

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

## Wiki Source Material

When the parent issue, plan document, comments, or operator prompt reference a Paperclip wiki URL, wiki page path, or captured wiki source, use `paperclip-wiki-fetch` before proposing inbound child issues. Carry the relevant fetched source title, path, update time, hash, and proof snippets into proposed issue bodies or `Source material/proof` when they affect audience, wedge, story, claims, or validation.

If the wiki reference cannot be fetched because credentials, company scope, wiki id, space slug, or page path are missing, pause planning and ask for the missing input. Do not create child issues that depend on inaccessible wiki material.

If the operator explicitly asks to publish, sync, or update wiki content from inbound planning output, finish the proposed breakdown first, then use `paperclip-wiki-manage` for the wiki mutation after approval.

### Creator source spaces

When planning content posts for a specific creator, their raw and distilled source material may live in a dedicated **creator wiki space** (captured via `paperclip-source-capture`, e.g. `spaceSlug: creator-jane`). Pull from it when proposing post issues:

- As the operator, read the space directly with `paperclip-wiki-fetch` using the creator's `spaceSlug` (list pages/sources, read the relevant `wiki/...` pages), and carry the supporting angle, story, and proof into `Source material/proof`.
- For the executing draft agent, reference the company `wiki-ask` skill in the issue body and name the creator's `spaceSlug`, so the agent retrieves cited detail and voice at draft time.
- Do not anonymize source material during planning. Note in `Stop conditions` that the draft/publish stage must strip client/carrier names and identifying detail before any public post.

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
- Readiness level: I0 strategy | I1 source-research | I2 asset-draft | I3 publishing-prep | I4 signal-capture
- Channel:
- Author/persona:
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
