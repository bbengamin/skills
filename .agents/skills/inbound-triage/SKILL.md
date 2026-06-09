---
name: inbound-triage
description: Triage inbound Growth Operator Paperclip issues for AFK readiness. Use when reviewing inbound, creator-led, channel-led, LinkedIn, newsletter, YouTube, content, trust-building, publishing-prep, or inbound signal-capture work before delegation.
---

# Inbound Triage

Decide whether planned inbound work is ready for AFK execution at the declared readiness level.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/growth-operator/afk-readiness.md`
- `../../../docs/growth-operator/control-plane.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

Open only when needed:

- `../../../docs/creator-operator/afk-readiness.md`
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
   - inbound readiness level
   - creator/persona
   - channel and campaign context
   - audience or ICP
   - wedge, positioning, story, and claims
   - source material and proof
   - expected output
   - publishing, scheduling, and account-action boundaries
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

## Wiki Source Material

When readiness depends on a Paperclip wiki URL, wiki page path, or captured wiki source, use `paperclip-wiki-fetch` to verify the source is accessible and sufficient before classifying the issue as AFK-ready. Include the fetched title, path, update time, and hash in `Source/proof status` when available.

If the wiki reference cannot be fetched because credentials, company scope, wiki id, space slug, or page path are missing, classify the issue as `needs-info` and name the missing wiki access in `Missing readiness elements`.

## Readiness Levels

- `I0 strategy` - strategy or branch parent readiness.
- `I1 source-research` - research or proof collection.
- `I2 asset-draft` - post, newsletter, script, angle, or content asset drafting.
- `I3 publishing-prep` - preparing a reviewed asset for publication without posting.
- `I4 signal-capture` - summarizing inbound responses, comments, conversations, or content signals.

## Readiness Rule

Inbound work is AFK-ready only when the issue gives an agent enough context to act without continuous operator supervision:

- related acquisition company goal or team goal
- durable inbound channel project
- parent strategy or campaign context
- readiness level
- creator/persona
- channel
- audience or ICP
- wedge, story, positioning, or hypothesis
- approved source material and proof
- expected output
- acceptance criteria
- validation expectations
- stop conditions
- no unresolved first-class blockers

Inbound work is not ready when publishing, scheduling, external account actions, or ungrounded claims are implied but not explicitly approved.

## Recommendation Format

```markdown
## Inbound Triage Recommendation

### <issue identifier/title>

- Classification:
- Readiness level:
- Current status:
- Recommended status:
- Missing readiness elements:
- Creator/channel context:
- Source/proof status:
- Publishing/account-action boundary:
- Proposed comment:
- Proposed blocker links:
- Follow-up skill:
```

## Status Rules

- `todo` means ready and actionable at the declared inbound readiness level.
- `backlog` means parked or not startable.
- `blocked` requires first-class blocker links for concrete issue dependencies when supported.
- Use `inbound-plan-work` for too-broad inbound strategy or campaign issues.
- Use comments to explain triage reasoning.

## Mutation Rule

Report recommendations first. Only update status, comments, blockers, labels, or assignees after operator approval.
