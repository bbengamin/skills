---
name: paperclip-triage
description: Triage Paperclip issues for AFK readiness. Use when reviewing issues, parent issues, plans, or planned work before delegating to an AFK agent loop.
---

# Paperclip Triage

Decide whether Paperclip issues are good enough to enter the AFK agent loop.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/afk-readiness.md`
- `../../../docs/paperclip-operator/cli-contract.md`

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

## Status Rules

- `todo` means ready and actionable.
- `backlog` means parked or not startable.
- `blocked` requires a named blocker in comments or first-class `blockedByIssueIds`.
- Use `paperclip-plan-work` for too-broad issues.
- Use comments to explain triage reasoning.

## Mutation Rule

Report recommendations first. Only update status, comments, blockers, labels, or assignees after operator approval.
