# Growth Operator AFK Readiness

Growth planning decides whether inbound or outbound work can later be triaged for execution.

## Shared Readiness Elements

Any growth work item should identify:

- related acquisition goal or sub-goal
- related durable channel or motion project
- parent strategy or campaign issue
- time horizon
- market, vertical, ICP, buyer, or persona
- wedge or painful workflow
- expected output
- acceptance criteria
- validation expectations
- stop conditions
- required approvals
- no unresolved first-class blockers

## Inbound-Specific Elements

Inbound work should additionally identify:

- creator/persona
- channel
- audience
- positioning or story
- source material and proof
- content format or deliverable
- publishing, scheduling, account-action, and claim boundaries
- signal capture expectation

## Outbound-Specific Elements

Outbound work should additionally identify:

- target segment or ICP slice
- lead source and enrichment assumptions
- contact route constraints
- personalization basis
- sequence or message output format
- offer, CTA, or walkthrough ask
- consent, compliance, and account-action boundaries
- reply and learning capture expectation

## Classifications

Use these classifications:

- `AFK-ready` - enough context to move toward execution at the declared readiness level.
- `needs-info` - missing required strategy, audience, artifact, output, or validation context.
- `blocked` - blocked by another issue or unavailable input.
- `needs-human` - requires operator judgment before execution.
- `too-broad` - should be planned into smaller child issues.
- `revise` - existing work item should be rewritten before execution.
- `cancel` - no longer worth pursuing.
- `done` - already completed.

## Inbound Readiness Levels

Use these levels when triaging inbound work:

- `I0 strategy` - strategy or branch parent readiness.
- `I1 source-research` - research or proof collection.
- `I2 asset-draft` - post, newsletter, script, angle, or content asset drafting.
- `I3 publishing-prep` - preparing a reviewed asset for publication without posting.
- `I4 signal-capture` - summarizing inbound responses, comments, conversations, or content signals.

Inbound work is not ready when publishing, scheduling, account actions, or ungrounded claims are implied but not explicitly approved.

## Outbound Readiness Levels

Use these levels when triaging outbound work:

- `O0 strategy` - strategy or campaign parent readiness.
- `O1 asset-prep` - lead-list, enrichment-spec, scoring, personalization, and draft-message assets. No sending.
- `O2 tool-work` - approved setup or configuration in tools such as Instantly, Clay, Grinfi, or a CRM. No launch unless separately approved.
- `O3 send-ready` - actual outreach launch or sending readiness.
- `O4 reply-booking` - reply classification, response drafting, booking support, and learning capture.

Outbound work is not ready above `O1 asset-prep` unless the relevant tool, account, input fields, output fields, budget or credit limits, compliance boundaries, suppression rules, and operator approval gates are explicit.

## Stop Conditions

Stop and ask the operator when:

- inbound and outbound are optimizing for different ICPs, wedges, or CTAs
- the project/channel/motion boundary is unclear
- the work asks for sending, posting, scheduling, CRM changes, paid tools, or account actions without approval
- the artifact ask or proof source is missing
- the success signal is vague or unmeasurable
- the work is too broad for one planning pass
- outbound work implies sending, paid enrichment, CRM mutation, or external account use without explicit approval
- inbound work implies posting, scheduling, or claims that are not grounded in approved source material
