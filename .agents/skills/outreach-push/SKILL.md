---
name: outreach-push
description: "Run the push stage of an outbound-engine run - create the list in the wired sending tool (Instantly or Grinfi via metamcp) and attach it to a campaign, the run's last operator action. Use when the operator wants to push or resume pushing a run's assembled segment to the sending tool, build the send list, or hand a QA-passed segment to automatic sending. Send-enabling and operator-gated: activating the campaign starts automatic sending; verifies suppression and consent, honors caps."
---

# Outreach Push

Run the push stage for one outreach run: take the assembled, QA-passed segment and create the list in the sending tool, then attach it to a campaign. This is the run's last operator action. Activating the campaign starts automatic sending in-tool, so activation is the send-enabling step and requires explicit operator approval.

This is the highest-risk stage: it queues real contacts for automatic outreach. Verify suppression and consent, honor caps, and confirm exact tool schemas before acting.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/outreach-operator/run-contract.md`
- `references/docs/outreach-operator/tool-map.md`
- `references/docs/outreach-operator/control-plane.md`
- `references/docs/growth-operator/afk-readiness.md`

Open when checkpointing to Paperclip or choosing a surface:

- `references/docs/outreach-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

## Process

Follow the bulk-stage pattern in `run-contract.md`. The push tools are wired through metamcp; see `tool-map.md` for the push row.

1. Resume. Read the Run Record. Confirm `push` is in the run's stage scope and read its checkpoint. Confirm `assemble` is `done`; push depends on assembled assets.
   - Read the sending tool (Instantly or Grinfi), the target campaign, the suppression and consent rules, and the volume caps.
   - Done when the tool, target campaign, and current counts are stated.
2. Confirm the tool surface. Learn the exact create-list, add-leads, and activate tool schemas for the configured sending tool before acting (for example `instantly__create_lead_list`, `instantly__add_leads_to_campaign_or_list_bulk`, `instantly__activate_campaign`, or `grinfi__create_list`, `grinfi__add_contact_to_automation`, `grinfi__start_automation`).
   - If the configured tool is not the wired one, or a needed connection is missing, stop and route to `growth-tooling-scout`. Do not improvise a surface.
3. Build the list and dry-run. Read the QA-passed, eligible segment from Twenty: leads with an assembled-asset reference, not suppressed, consent satisfied. Show the list size, a sample, the target campaign, and the suppression and cap check. Create or update the list and add leads, but do not activate.
   - Done when the list exists in the tool with the intended members and the campaign is not yet activated.
4. Approval gate. Activation is send-enabling: it starts automatic sending. Require explicit operator approval that names the tool, the campaign, the list size, and that sending will begin automatically. Do not proceed on a generic prior approval.
5. Activate within caps. Activate the campaign or start the automation through the learned tool. Stop and checkpoint as `stopped` if a cap or stop condition trips.
6. Record back. Through `twenty-engine-sync`, write each pushed lead's campaign membership and push status, plus the list and campaign reference. Checkpoint counts (pushed, skipped or suppressed, errored), then move `push` to `qa`.
   - Done when every eligible lead is pushed or carries an explicit skip reason, and the counts sum to the eligible total.
7. QA gate. Verify the list in the sending tool matches the intended segment: count, suppression honored, correct campaign, expected sending state. On pass, set `push` to `done`. On fail, set it to `revise` or `stopped` with a comment.

## Boundaries

- Send-enabling and operator-gated. Activation starts automatic sending, so it needs explicit, specific approval. Building and populating the list is safe; activating is not. Never auto-approve activation from an earlier gate.
- Confirm schemas, never improvise. Learn the exact tool schema before acting; if the configured surface is missing, route to `growth-tooling-scout`.
- Verify suppression and consent before pushing. Never push suppressed or no-consent leads, and never exceed volume caps.
- All Twenty writes go through `twenty-engine-sync`. Never write Twenty directly.
- Push only, no content edits. Message content is the assemble stage; push does not rewrite assets.
- v1 stops here. Do not build deliverability infrastructure, scheduling, reply handling, or analytics; sending and its automation are owned by the sending tool.
