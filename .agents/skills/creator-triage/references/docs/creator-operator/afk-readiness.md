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
