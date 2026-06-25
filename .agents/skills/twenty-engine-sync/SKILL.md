---
name: twenty-engine-sync
description: Engine-side execution skill for syncing the outbound golden record to Twenty CRM. Use when an outbound-engine agent needs to query Twenty by identity, resolve a candidate contact to a Person, run idempotent match-or-create, merge into a golden record, route fuzzy matches to human QA, or apply suppression/routing — always additive, dry-run first, no sending, no credit spend.
---

# Twenty Engine Sync

The shared read/write capability every Twenty-touching outbound-engine skill
depends on. Resolve identity, keep one golden record per person, and write
additively. Reads are free; every write is dry-run first and operator-gated.

Twenty is the sales system of record and is shared with live SDR work. Never
delete, never overwrite a populated identity value, never send outreach, never
spend enrichment credits, never change schema/metadata. Ambiguity halts.

## Capabilities

1. **Query by identity** — look up a Person by `linkedinLink.primaryLinkUrl` or
   `emails.primaryEmail`, plus ICP filters, with `find_many_*` + explicit `select`.
2. **Identity resolution (RL-439)** — classify a candidate as `match`,
   `no-match`, `fuzzy-candidate`, or `collision`. See
   `references/identity-resolution.md`.
3. **Idempotent match-or-create** — 0 matches → `would-create`; 1 → `would-update`
   (additive, by id); ≥2 → `collision-skip` (halt). No `upsert_*` on email/LinkedIn
   (no unique constraint).
4. **Auto-merge + survivorship (RL-440)** — fold matches into one golden record
   by field class (identity keys fill-if-empty; enrichment freshest-wins; manual
   override wins; multi-value appends). See `references/merge-survivorship.md`.
5. **Fuzzy → human-QA queue (RL-441)** — surface name+company candidates and all
   collisions to a review queue; never auto-merge fuzzy. See
   `references/fuzzy-qa-queue.md`.
6. **Suppression + routing (defer to `eligibility-gate`)** — the per-person
   verdict (suppress / skip / source / re-enrich / reuse) and routing are owned
   by the `eligibility-gate` skill, the single deterministic decision authority.
   Run the gate first; this skill owns only the writes that carry out a cleared
   verdict (membership enroll via `activeCampaignMembershipId` + `status=ACTIVE`,
   the new `campaignTouch`, and binding the routed `sendingAccount`).

## Golden-record schema

`references/golden-record-schema.md` holds the object/field/identity map
(Person, Campaign, CampaignMembership, campaignTouch, SendingAccount, EngineConfig).
Identity precedence is always `linkedinLink.primaryLinkUrl` → `emails.primaryEmail`.

## Operating loop

1. Connect and learn exact tool schemas (meta-tool pattern: `get_tool_catalog` →
   `learn_tools` → `execute_tool`); never guess operation schemas.
2. Resolve identity for each candidate with the decision layer in `demo/engine_identity.py`.
3. Run `eligibility-gate` per record for the verdict (suppress / skip / source /
   re-enrich / reuse) + routing; do not re-derive suppression, TTL, or routing here.
4. Produce a dry plan: per record `would-create` / `would-update` /
   `collision-skip` / `blocked`, with field-level diffs and survivorship audit.
5. Route fuzzy + collisions to the QA queue. Do not auto-merge them.
6. Ask for approval before any create, update, merge, action, or external effect.
7. Execute only the approved operation, additive and by id.
8. Read back and verify the changed record and the guarded non-changes.

## Reference implementation + demo

`demo/engine_identity.py` is the dependency-free decision layer (normalization,
Jaro-Winkler + token-set fuzzy scoring, resolver, survivorship merge planner,
queue builder). It performs no Twenty access. `demo/run_demo.py` exercises it on
the synthetic sample in `demo/sample_data.py`:

```sh
python3 demo/run_demo.py
```

Expected: 2 `match`, 1 `no-match`, 1 `fuzzy-candidate`, 2 `collision`; two dry
merge plans; a 3-item QA queue; `Twenty writes performed: 0`.

## Guarantees

Additive, idempotent, non-destructive. Reads free. Forbidden without explicit
approval: deletes, overwriting populated fields, schema/metadata changes,
outreach send, credit spend, Paperclip skill install/attach. Halt on identity
collision or schema drift. Read-back verification after every write.

## Callers

Operator pipeline: the local `outreach-*` stage runners (`outreach-source`,
`outreach-resolve`, `outreach-enrich`, `outreach-gate`, `outreach-assemble`,
`outreach-review`) route their Twenty reads and writes through this skill.

Paperclip engine tasks: RL-429 (Apollo ingest), RL-430 (Clay write-back),
RL-431 (campaign assembly), RL-433 (outcome write-back), RL-439/440/441
(identity + merge wave).
