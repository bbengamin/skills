# Creator Growth Control Plane

Creator Growth work uses Paperclip as the source of truth for strategy, planning, work items, comments, approvals, assignments, and activity.

## Entity Model

Use stable direction at the Goal layer and changing strategy at the Project/Issue/document layer.

```text
Company Goal -> Team Goal(s) -> Creator Project -> Strategy Parent Issues -> Campaign Parent Issues -> Work Items
```

## Goals

Goals should express durable direction, not every campaign or month. Use Paperclip's native goal fields when creating or revising them:

- `level: "company"` for a top-level creator-led acquisition outcome when it is the durable company strategy.
- `level: "team"` for creator/persona and expertise child goals under the company goal.
- `level: "agent"` only when a specific Paperclip agent owns the goal; set `ownerAgentId`.
- `level: "task"` rarely; prefer Issues for execution.
- `parentId` for every creator/persona or expertise child goal.

Recommended shape:

- Company goal: `Build creator-led distribution as a repeatable acquisition asset`
- Team goal: `Use <creator>'s founder brand to generate trust and qualified conversations`
- Team goal: `Establish <creator>'s <domain> expertise`

Avoid creating a new goal for every month, channel, or short-lived campaign unless that campaign becomes strategically important beyond creator operations.

## Projects

Create one Creator Growth project per creator/persona.

Examples:

- `Creator ops: Ihor`
- `Creator ops: <name>`

The project groups the creator's strategy, campaign planning, execution work, and review artifacts.

## Strategy Parent Issues

Use parent issues and plan documents for time horizons and campaign structure.

Recommended hierarchy:

```text
Creator strategy 2026
└── Creator strategy Q3 2026
    └── Creator strategy June 2026
        └── LinkedIn campaign: logistics hypothesis X
            └── executable child work items
```

Create only the next missing layer unless the operator approves a larger structure.

## Campaigns

Campaign parent issues represent channel-specific hypotheses or focused content efforts.

Examples:

- `LinkedIn campaign: logistics MVP hypothesis X`
- `X/Twitter campaign: short-form positioning tests`
- `Newsletter campaign: AI logistics lessons from customer calls`

Campaigns may capture lightweight signals and learnings, but v1 does not own full business experiment tracking.

## Scheduled Post Queue

Individual campaign post tasks use Paperclip as the queue. Plan all known posts up front as child issues under the campaign parent, but keep future post work in `backlog` until it is inside its draft window.

Use the `creator-post` label on every individual post issue that should enter the Creator Drafter queue:

- Label: `creator-post`
- Label id: `043f348f-1e22-4fe8-bb6f-8bcbde18e4c6`

Required issue fields or clearly parseable body lines:

- `creator`: creator/persona for the post
- `channel`: `LinkedIn`
- `targetSlotAt`: intended review or publish slot as an ISO timestamp with timezone
- `draftWindow`: how far before `targetSlotAt` the draft should be prepared; default `24h` only when the rest of the issue is complete
- `postizMode`: `create-draft-only`
- `sourceRefs`: source issue, plan document, wiki page, notes, transcript, or other approved source material
- `brief`: topic, angle, audience, claim boundaries, and CTA
- `acceptanceCriteria`: what a good draft must satisfy
- `doneDefinition`: final LinkedIn URL is manually recorded in Paperclip by the operator

Queue lifecycle:

- Future individual post issues stay `backlog`, labelled `creator-post`, unassigned or assigned only if the queue policy explicitly allows it.
- The Creator Queue Steward routine scans `backlog` `creator-post` issues hourly, computes `draftOpenAt = targetSlotAt - draftWindow`, and promotes due posts to `todo`.
- The steward assigns promoted posts to Creator Drafter.
- Creator Drafter drafts the post and creates a Postiz review-only draft.
- Multiple post issues may sit in `in_review` at the same time.
- Publishing and scheduling remain manual in v1; the operator records the final LinkedIn URL in Paperclip.

Do not move every planned future post to `todo`. A too-early post in `todo` is expected to be returned to `backlog`, which can strand it unless the queue steward later promotes it.

## Work Items

Executable work items should be small enough for one AFK loop.

Examples:

- research source material for a campaign
- propose post angles
- draft a bounded LinkedIn post
- revise a draft from operator feedback
- summarize creator-channel signals

### Campaign Post Task Template

Use this shape when planning individual LinkedIn campaign posts:

```markdown
# <Campaign>: LinkedIn post for <targetSlotAt date/topic>

Labels: creator-post
Status: backlog
Assignee: null
Parent: <campaign parent issue>
Project: <creator project>

## Queue

- creator: <creator/persona>
- channel: LinkedIn
- targetSlotAt: <YYYY-MM-DDTHH:mm:ssZ or timezone-qualified ISO timestamp>
- draftWindow: 24h
- postizMode: create-draft-only

## Brief

- audience:
- topic/angle:
- sourceRefs:
- claim boundaries:
- CTA:

## Acceptance Criteria

- Draft is grounded in the listed source material.
- Draft is suitable for LinkedIn and in the creator's voice.
- Unsupported claims, private details, and invented numbers are avoided or flagged.
- Postiz handoff is draft-only.

## Done Definition

- Creator Drafter has produced the Paperclip `draft` document.
- Postiz has a review-only draft, or Paperclip records `postizStatus: handoff_failed`.
- Operator manually reviews/publishes in Postiz.
- Operator records the final LinkedIn URL in Paperclip.
```

## Mutation Rule

Creator Growth skills may inspect Paperclip freely. They must present proposed goals, projects, issues, comments, status changes, plan documents, and assignments before mutating the control plane.
