# Growth Operator Control Plane

Growth Operator work uses Paperclip as the source of truth for acquisition strategy, channel strategy, outbound motions, planned work, comments, approvals, assignments, and activity.

## Entity Model

Use Goals for durable direction, Projects for durable channels or motions, and parent Issues with plan documents for strategy periods, campaigns, and experiments.

```text
Company Goal -> Team Goal(s) -> Channel/Motion Project -> Strategy Parent Issues -> Campaign/Experiment Parent Issues -> Work Items
```

## Goals

Goals should express durable acquisition direction. They must use Paperclip's native goal fields when created or revised:

- `level: "company"` for the top-level acquisition outcome, usually active once approved.
- `level: "team"` for inbound, outbound, creator, expertise, vertical, validation, channel, or motion child goals.
- `level: "agent"` only when a specific Paperclip agent owns the goal; set `ownerAgentId`.
- `level: "task"` rarely; prefer Issues for executable or short-lived work.
- `parentId` for every child goal in the acquisition tree.

Recommended shape:

```text
[company] Build repeatable acquisition
|-- [team] Build inbound trust engine through <creator>'s personal brand
|   `-- [team] Establish <creator>'s <domain> expertise brand
`-- [team] Build outbound engine for operator walkthroughs and validation
    `-- [team] Build repeatable <vertical/persona> outreach motion
```

Avoid creating goals for every month, channel campaign, message sequence, lead list, or content sprint. Use issues for those.

## Projects

Create one project per durable channel or durable motion.

Examples:

- `Inbound: Ihor LinkedIn`
- `Inbound: Ihor Newsletter`
- `Inbound: Ihor YouTube`
- `Outbound: Operator walkthroughs`
- `Outbound: Partnerships and warm intros`

Each project should link to the durable acquisition company goal and any relevant inbound, outbound, creator, expertise, vertical, or validation team goals.

Use a broader project such as `Growth ops: Ihor` only when the channel or motion is not yet durable enough to deserve its own project.

## Strategy Parent Issues

Use parent issues and plan documents for time horizons and strategy structure.

Recommended inbound hierarchy:

```text
Growth 2026
`-- Growth strategy Q3 2026
    `-- June inbound logistics strategy
        `-- LinkedIn campaign: logistics workflow pain
            `-- executable child work items
```

Recommended outbound hierarchy:

```text
Outbound growth 2026
`-- Outbound strategy Q3 2026
    `-- June construction walkthrough strategy
        `-- Campaign: estimate-to-invoice walkthroughs
            `-- executable child work items
```

Create only the next missing layer unless the operator approves a larger structure.

## Shared Strategy Fields

Inbound and outbound branches must stay aligned through shared fields:

- acquisition goal
- vertical or market
- ICP and buyer/persona
- wedge or painful workflow
- artifact ask
- proof/source material
- offer or CTA
- success signals
- validation expectations
- stop conditions
- signal logging expectations

## Branch Ownership

Shared `growth-*` skills clarify and record the strategy layer.

Inbound planning owns channel/content execution such as audience, positioning, source material, post angles, drafts, publishing constraints, and inbound signal capture.

Outbound planning owns lead sourcing, enrichment, personalization, sequence assets, reply handling, walkthrough asks, and outbound signal capture.

## Mutation Rule

Growth Operator skills may inspect Paperclip freely. They must present proposed goals, projects, issues, plan documents, comments, status changes, and assignments before mutating the control plane.
