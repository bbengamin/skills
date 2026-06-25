---
name: outreach-review
description: Run the review stage of an outbound-engine run - pull reply and campaign signal from the sending tools, summarize outcomes, and write the kill/continue signal back to Paperclip. Use when the operator wants to review or resume reviewing a run's results, read campaign analytics and replies, capture learnings, or make the go/pivot/stop call that feeds the next strategy loop. Reads freely; the kill/continue decision and any reply send are operator-gated.
---

# Outreach Review

Run the review stage for one outreach run: gather what the run produced, summarize it, and feed the signal back to strategy. Reading is free; the kill/continue decision and any reply send are operator-gated. This stage closes the loop the strategy plane opened.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/outreach-operator/run-contract.md`
- `references/docs/outreach-operator/tool-map.md`
- `references/docs/outreach-operator/control-plane.md`

Open when writing the signal back or choosing a surface:

- `references/docs/growth-operator/control-plane.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

## Process

1. Resume. Read the Run Record. Confirm `push` is `done` (a run with no sent campaign has no outcome to review). Read the success signal and kill/continue thresholds.
   - Done when the success signal, thresholds, and the campaign under review are stated.
2. Pull signal from the sending tools (see `tool-map.md`): campaign analytics (`instantly__get_campaign_analytics`, `grinfi__get_outreach_metrics`, `grinfi__get_dashboard`, `grinfi__list_outbound_log`) and replies (`instantly__list_emails`, `grinfi__list_linkedin_messages`, `grinfi__get_unread_conversations`).
3. Reconcile outcome to Twenty through `twenty-engine-sync`: write each lead's reply or outcome signal so the lead ledger stays current.
4. Summarize against the run's success signal: volume sent, positive replies, meetings or walkthroughs booked, and the learnings the run produced.
   - Done when the summary states each success-signal metric and whether the thresholds were met.
5. Kill/continue. Present the go / pivot / stop recommendation against the thresholds. The decision is the operator's; do not act on it unilaterally.
6. Write the signal back to Paperclip. After the operator decides, record the outcome and decision on the campaign or strategy parent issue, and checkpoint the Run Record (`review` to `done`, or `stopped` on a kill).
   - Done when the signal lives on the Paperclip campaign or strategy issue and the Run Record reflects the decision.

## Boundaries

- Read freely, decide gated. The kill/continue call is the operator's; never declare a run a success or a kill unilaterally.
- Reply sends are gated. Drafting a reply is fine; sending one (`instantly__reply_to_email`, `grinfi__send_email`, `grinfi__send_linkedin_message`) needs explicit operator approval.
- Twenty lead outcomes go through `twenty-engine-sync`; the strategy signal goes on the Paperclip campaign or strategy issue. Keep each in its own source of truth.
- v1 stops at signal capture. Do not build dashboards, attribution, or autonomous reply handling.
