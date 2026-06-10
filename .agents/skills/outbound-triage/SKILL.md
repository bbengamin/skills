---
name: outbound-triage
description: Triage outbound Growth Operator Paperclip issues for level-aware AFK readiness. Use when reviewing lead sourcing, enrichment, personalization, sequences, Instantly, Clay, Grinfi, CRM, reply handling, warm-intro, operator walkthrough booking, or outbound validation work before delegation.
---

# Outbound Triage

Decide whether planned outbound work is ready for AFK execution at the declared outbound readiness level.

Outbound triage is level-aware because outbound work ranges from harmless asset preparation to external account actions and real prospect contact.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/growth-operator/afk-readiness.md`
- `references/docs/growth-operator/control-plane.md`
- `references/docs/paperclip-operator/integration-matrix.md`

Open only when needed:

- `references/docs/paperclip-operator/control-plane.md`
- `references/docs/paperclip-operator/cli-contract.md`

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
   - outbound readiness level
   - market, vertical, ICP, buyer, and persona
   - wedge or painful workflow
   - artifact ask, offer, CTA, or walkthrough ask
   - lead source and enrichment assumptions
   - contact route and personalization basis
   - tool names, accounts, fields, budgets, and limits
   - consent, compliance, suppression, and account-action boundaries
   - reply handling and learning capture
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

When readiness depends on a Paperclip wiki URL, wiki page path, or captured wiki source, use `paperclip-wiki-fetch` to verify the source is accessible and sufficient before classifying the issue as AFK-ready. Include the fetched title, path, update time, and hash in ICP, wedge, or source context when available.

If the wiki reference cannot be fetched because credentials, company scope, wiki id, space slug, or page path are missing, classify the issue as `needs-info` and name the missing wiki access in `Missing readiness elements`.

If triage discovers stale, missing, or incorrect wiki content, recommend `paperclip-wiki-manage` as the follow-up skill. Do not mutate wiki content from ordinary triage unless the operator explicitly switches to wiki management and approves the exact mutation.

## Readiness Levels

- `O0 strategy` - strategy or campaign parent readiness.
- `O1 asset-prep` - lead-list, enrichment-spec, scoring, personalization, and draft-message assets. No sending.
- `O2 tool-work` - approved setup or configuration in tools such as Instantly, Clay, Grinfi, or a CRM. No launch unless separately approved.
- `O3 send-ready` - actual outreach launch or sending readiness.
- `O4 reply-booking` - reply classification, response drafting, booking support, and learning capture.

## Readiness Rule

Outbound work is AFK-ready only when the issue gives an agent enough context to act without continuous operator supervision at the requested level:

- related acquisition company goal or team goal
- durable outbound motion project
- parent strategy or campaign context
- readiness level
- market, vertical, ICP, buyer, or persona
- wedge or painful workflow
- artifact ask, offer, CTA, or walkthrough ask
- expected output
- acceptance criteria
- validation expectations
- stop conditions
- no unresolved first-class blockers

Additional requirements by level:

- `O1 asset-prep`: lead source, enrichment assumptions, personalization basis, output fields, and no sending.
- `O2 tool-work`: named tool, account, input fields, output fields, budget or credit limit, and approved configuration boundary.
- `O3 send-ready`: explicit operator approval to send, sender accounts, sequence, suppression rules, compliance boundary, daily caps, launch timing, monitoring plan, and stop conditions.
- `O4 reply-booking`: reply categories, approved response boundaries, booking handoff, escalation rules, and learning capture target.

Outbound work is not ready above `O1 asset-prep` when tool access, paid credits, CRM mutation, external account use, sending, or reply handling is implied but not explicitly approved.

## Recommendation Format

```markdown
## Outbound Triage Recommendation

### <issue identifier/title>

- Classification:
- Readiness level:
- Current status:
- Recommended status:
- Missing readiness elements:
- ICP/wedge context:
- Tool/action boundary:
- Sending/reply boundary:
- Proposed comment:
- Proposed blocker links:
- Follow-up skill:
```

## Status Rules

- `todo` means ready and actionable at the declared outbound readiness level.
- `backlog` means parked or not startable.
- `in_review` is preferred for send-ready work that needs final operator approval before launch.
- `blocked` requires first-class blocker links for concrete issue dependencies when supported.
- Use `outbound-plan-work` for too-broad outbound strategy or campaign issues.
- Use comments to explain triage reasoning.

## Mutation Rule

Report recommendations first. Only update status, comments, blockers, labels, or assignees after operator approval. Never send outreach, launch campaigns, mutate CRM records, spend credits, or modify external accounts from this skill.
