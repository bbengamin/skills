# Creator Growth AFK Readiness

Creator Growth triage decides whether a planned creator work item can safely enter AFK execution.

## Ready

A creator work item is AFK-ready when it has:

- Creator/persona
- Related project or strategy parent
- Time horizon or campaign context
- Channel, if channel-specific
- Audience or ICP
- Topic, hypothesis, source material, or research target
- Expected output format
- Acceptance criteria
- Validation expectations
- Stop conditions
- Any required human approvals already captured
- No unresolved first-class blockers

For individual scheduled post work, it also has:

- `creator-post` label when it should be handled by the Creator Queue Steward
- `targetSlotAt` with timezone
- `draftWindow`, or enough complete context to safely use the default `24h`
- `postizMode: create-draft-only`
- explicit done definition that the operator manually records the final LinkedIn URL

## Classifications

Use these classifications:

- `AFK-ready` - enough context to move toward execution.
- `needs-info` - missing creator, audience, channel, source, output, or acceptance criteria.
- `blocked` - blocked by another Paperclip issue or unavailable input.
- `needs-human` - requires operator judgment before execution.
- `too-broad` - should be planned into smaller child issues.
- `revise` - existing work item should be rewritten before execution.
- `cancel` - no longer worth pursuing.
- `done` - already completed.

## Stop Conditions

Stop and ask the operator when:

- the creator/persona is unclear
- the target audience or ICP is unclear
- the strategy conflicts with an existing creator goal or plan
- the work would require posting, scheduling, account actions, CRM ownership, or external tool setup not explicitly approved
- source material is missing or claims cannot be grounded
- the issue asks for full business experiment tracking instead of creator-channel contribution
- the work is too broad for a single AFK loop
- an individual future post is in `todo` before `targetSlotAt - draftWindow`; return or recommend returning it to `backlog` so the Creator Queue Steward can promote it later

## Queue Readiness

Individual campaign post issues can be planning-ready before they are execution-ready.

- `backlog` + `creator-post` + complete queue fields means queued for future promotion.
- `todo` + due `draftOpenAt` + Creator Drafter assignment means actionable draft work.
- `in_review` means the operator may review the Paperclip/Postiz draft; multiple post issues may be in review at once.
- `done` requires the final published LinkedIn URL to be recorded in Paperclip.

Triage should not move a whole post calendar to `todo`. When many post tasks are planned together, leave them in `backlog` and rely on the Creator Queue Steward routine to promote at most the due items.

## Triage Output

Use this shape:

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
