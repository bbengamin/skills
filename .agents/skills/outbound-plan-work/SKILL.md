---
name: outbound-plan-work
description: Split a shared growth strategy or outbound branch artifact into one level of Paperclip backlog work items for outbound acquisition. Use when planning lead sourcing, enrichment, personalization, sequences, reply handling, operator walkthrough booking, warm intros, or outbound validation work after growth-record-strategy.
---

# Outbound Plan Work

Plan one child-issue level at a time from a selected growth strategy, outbound branch, or outbound campaign parent issue.

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

1. Identify the target growth strategy, outbound branch, or outbound campaign parent issue.
2. Read the issue, plan document, parent chain, project, linked goals, blockers, and comments.
3. Confirm the intended planning depth.
4. Propose one level of child issues.
5. Classify each proposed child into exactly one of:
   - ready-looking
   - planning parent
   - needs-human
   - blocked
   - needs-info

   Done when every proposed child carries exactly one type.
6. If more than two proposed children are unclear, pause for focused clarification before creating issues.
7. Include the exact title, body, status, parent, project, blockers, and assignee for each issue.
8. Ask for approval.
9. After approval, create issues in dependency order and verify each record.

## Wiki Source Material

When the parent issue, plan document, comments, or operator prompt reference a Paperclip wiki URL, wiki page path, or captured wiki source, use `paperclip-wiki-fetch` before proposing outbound child issues. Carry the relevant fetched source title, path, update time, hash, and proof snippets into proposed issue bodies when they affect market, ICP, wedge, artifact ask, offer, CTA, lead source, or personalization basis.

If the wiki reference cannot be fetched because credentials, company scope, wiki id, space slug, or page path are missing, pause planning and ask for the missing input. Do not create child issues that depend on inaccessible wiki material.

If the operator explicitly asks to publish, sync, or update wiki content from outbound planning output, finish the proposed breakdown first, then use `paperclip-wiki-manage` for the wiki mutation after approval.

## Planning Patterns

Examples:

- Yearly outbound strategy -> quarterly strategy parent issues.
- Quarterly outbound strategy -> monthly strategy parent issues.
- Monthly outbound strategy -> campaign parent issues.
- Walkthrough campaign -> define ICP slice, build lead list, enrich routes, draft sequence, prepare walkthrough script, capture replies and learnings.
- Warm-intro campaign -> map intro paths, draft asks, prepare context blurbs, track responses, and capture learning.

Create broad children as planning parents, not execution-ready issues.

## Proposed Breakdown Format

```markdown
## Proposed Outbound Child Issues

### 1. <title>

- Type: ready-looking | planning parent | needs-human | blocked | needs-info
- Priority:
- Status to write: backlog
- Parent:
- Project:
- Linked goals:
- Blocked by:
- Assignee: null
- Readiness level: O0 strategy | O1 asset-prep | O2 tool-work | O3 send-ready | O4 reply-booking
- Market/vertical:
- ICP/buyer/persona:
- Wedge or painful workflow:
- Artifact ask:
- Offer/CTA:
- Lead source or contact route:
- Compliance/account-action boundaries:
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
- Do not send messages, scrape behind auth, modify CRM records, buy tools, or use external accounts unless explicitly approved in the parent strategy.
- Use `parentId`/native parent linkage and verify it after creation.
- Use first-class `blockedByIssueIds` for concrete dependencies when available.
- Do not replace plan documents or blocker links with comments unless the operator explicitly approves degraded mode.

## Mutation Rule

Never create child issues until the operator approves the proposed breakdown.
