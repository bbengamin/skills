---
name: paperclip-triage
description: Triage Paperclip issues for AFK readiness. Use when reviewing issues, parent issues, plans, or planned work before delegating to an AFK agent loop.
---

# Paperclip Triage

Decide whether Paperclip issues are good enough to enter the AFK agent loop.

## References

Read these first for normal triage:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/afk-readiness.md`
- `references/docs/paperclip-operator/integration-matrix.md`

Open the remaining references only when the issue touches that area:

- `references/docs/paperclip-operator/control-plane.md` for entity semantics, parent/child structure, blockers, comments, documents, approvals, and activity.
- `references/docs/paperclip-operator/cli-contract.md` for CLI/REST auth, fallback examples, and mutation verification.

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

## Wiki Source Material

When readiness depends on a Paperclip wiki URL, wiki page path, or captured wiki source, use `paperclip-wiki-fetch` to verify the source is accessible and sufficient before classifying the issue as AFK-ready. Include the fetched title, path, update time, and hash in the recommendation when available.

If the wiki reference cannot be fetched because credentials, company scope, wiki id, space slug, or page path are missing, classify the issue as `needs-info` and name the missing wiki access in `Missing readiness elements`.

If triage discovers stale, missing, or incorrect wiki content, recommend `paperclip-wiki-manage` as the follow-up skill. Do not mutate wiki content from ordinary triage unless the operator explicitly switches to wiki management and approves the exact mutation.

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

- Use CLI issue reads, updates, and comments first when it supports the needed fields and verification.
- Use MCP issue tools when CLI cannot perform or verify the operation.
- Use MCP `paperclipApiRequest` for Paperclip-native fields that CLI and dedicated MCP tools do not expose, especially `blockedByIssueIds`.
- Use direct REST only when CLI and MCP are unavailable or broken.

If CLI and dedicated MCP tools cannot write blocker links, use the API fallback from `cli-contract.md`.

Verify every mutation by reading the issue back. For blocker changes, confirm the returned issue contains the intended `blockedByIssueIds`; do not treat a comment-only explanation as equivalent unless the operator explicitly approved degraded mode.

If comment history is not exposed by the current issue detail surface, inspect the activity/comment surface if available. If comments still cannot be read, state that limitation in the recommendation and proceed from the visible issue fields instead of blocking the whole triage.
