---
name: paperclip-triage
description: Triage Paperclip issues for AFK readiness. Use when reviewing issues, parent issues, plans, or planned work before delegating to an AFK agent loop.
---

# Paperclip Triage

Decide whether Paperclip issues are good enough to enter the AFK agent loop.

## References

Read these first for normal triage:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/afk-readiness.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

Open the remaining references only when the issue touches that area:

- `../../../docs/paperclip-operator/control-plane.md` for entity semantics, parent/child structure, blockers, comments, documents, approvals, and activity.
- `../../../docs/paperclip-operator/cli-contract.md` for CLI/REST auth, fallback examples, and mutation verification.

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Process

1. Read the target issue or issue list.
2. For each issue, inspect:
   - status
   - project
   - parent
   - description
   - acceptance criteria
   - blockers and `blockedByIssueIds`
   - plan document
   - comments
   - assignee, if present
3. Classify the issue:
   - AFK-ready
   - needs-info
   - blocked
   - needs-human
   - too-broad
   - revise
   - cancel
   - done
4. Recommend exact changes.
5. Wait for approval.
6. Apply approved changes.

## Scope Depth

When triaging a parent issue, inspect its direct children. Inspect one additional child level when the operator says "child tasks", when newly planned children are present, or when a readiness decision depends on grandchildren. Do not recursively walk large trees by default; summarize deeper branches and recommend `paperclip-plan-work` for children that are still planning parents.

## Recommendation Format

```markdown
## Triage Recommendation

### <issue identifier/title>

- Classification:
- Current status:
- Recommended status:
- Missing readiness elements:
- Proposed comment:
- Proposed blocker links:
- Follow-up skill:
```

For large issue trees, use compact mode:

```markdown
## Triage Recommendation

- Parent summary:
- Executable now:
- Blocked:
- Needs planning/info:
- Approved mutations table:
```

## Status Rules

- `todo` means ready and actionable.
- `backlog` means parked or not startable.
- `blocked` requires first-class `blockedByIssueIds` for concrete issue dependencies. Comments may explain the owner and unblock action, but they do not replace blocker links unless the operator explicitly approves degraded mode.
- Use `paperclip-plan-work` for too-broad issues.
- Use comments to explain triage reasoning.

## Mutation Rule

Report recommendations first. Only update status, comments, blockers, labels, or assignees after operator approval.

## Apply Approved Changes

Use the narrowest Paperclip surface that can perform the native mutation:

- Read/update issue lifecycle and write triage comments with MCP when available: `get_issue`, `update_issue`, and `comment_on_issue`.
- Use CLI only when MCP does not expose the operation and `paperclipai` does.
- Use REST for Paperclip-native fields that MCP/CLI do not expose, especially `blockedByIssueIds`.

If MCP/CLI cannot write blocker links, use the REST fallback from `cli-contract.md`:

```sh
curl -sS -X PATCH "$PAPERCLIP_API_BASE/api/issues/$ISSUE_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"blockedByIssueIds":["<blocking-issue-id>"]}'
```

Verify every mutation by reading the issue back. For blocker changes, confirm the returned issue contains the intended `blockedByIssueIds`; do not treat a comment-only explanation as equivalent unless the operator explicitly approved degraded mode.

If comment history is not exposed by the current issue detail surface, inspect the activity/comment surface if available. If comments still cannot be read, state that limitation in the recommendation and proceed from the visible issue fields instead of blocking the whole triage.
