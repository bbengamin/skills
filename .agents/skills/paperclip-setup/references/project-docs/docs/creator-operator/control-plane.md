# Creator Growth Control Plane

Creator Growth work uses Paperclip as the source of truth for strategy, planning, work items, comments, approvals, assignments, and activity.

## Entity Model

Use stable direction at the Goal layer and changing strategy at the Project/Issue/document layer.

```text
Goal -> related Goal(s) -> Creator Project -> Strategy Parent Issues -> Campaign Parent Issues -> Work Items
```

## Goals

Goals should express durable direction, not every campaign or month.

Recommended shape:

- Top-level goal: `Build creator-led distribution as a repeatable acquisition asset`
- Related creator goal: `Use <creator>'s founder brand to generate trust and qualified conversations`
- Related expertise goal: `Establish <creator>'s <domain> expertise`

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

## Work Items

Executable work items should be small enough for one AFK loop.

Examples:

- research source material for a campaign
- propose post angles
- draft a bounded LinkedIn post
- revise a draft from operator feedback
- summarize creator-channel signals

## Mutation Rule

Creator Growth skills may inspect Paperclip freely. They must present proposed goals, projects, issues, comments, status changes, plan documents, and assignments before mutating the control plane.
