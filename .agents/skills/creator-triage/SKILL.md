---
name: creator-triage
description: Triage Creator Growth Paperclip issues for AFK readiness. Use when reviewing planned creator, channel, campaign, LinkedIn/content, or creator-led distribution work before delegation to Paperclip agent execution.
---

# Creator Triage

Decide whether planned creator work is ready for AFK execution.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/creator-operator/afk-readiness.md`
- `../../../docs/creator-operator/control-plane.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

Open only when needed:

- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/cli-contract.md`

## Process

1. Read the target issue or issue list.
2. Inspect:
   - status
   - project
   - parent chain
   - linked goals
   - plan document
   - description
   - acceptance criteria
   - creator/persona
   - channel and campaign context
   - audience or ICP
   - source material
   - blockers and `blockedByIssueIds`
   - comments
   - assignee
3. Classify each issue:
   - AFK-ready
   - needs-info
   - blocked
   - needs-human
   - too-broad
   - revise
   - cancel
   - done
4. Recommend exact changes.
5. Ask for approval.
6. Apply approved changes and verify by reading records back.

## Readiness Rule

Creator work is AFK-ready only when the issue gives an agent enough context to act without continuous operator supervision:

- creator/persona
- strategy or campaign context
- channel, if relevant
- audience or ICP
- topic, hypothesis, source material, or research target
- expected output
- acceptance criteria
- validation expectations
- stop conditions
- no unresolved first-class blockers

## Recommendation Format

```markdown
## Creator Triage Recommendation

### <issue identifier/title>

- Classification:
- Current status:
- Recommended status:
- Missing readiness elements:
- Creator/channel context:
- Proposed comment:
- Proposed blocker links:
- Follow-up skill:
```

## Status Rules

- `todo` means ready and actionable.
- `backlog` means parked or not startable.
- `blocked` requires first-class blocker links for concrete issue dependencies when supported.
- Use `creator-plan-work` for too-broad creator strategy or campaign issues.
- Use comments to explain triage reasoning.

## Mutation Rule

Report recommendations first. Only update status, comments, blockers, labels, or assignees after operator approval.
