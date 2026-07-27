---
name: eligibility-gate
description: "Engine-side decision skill that returns the per-person eligibility verdict for the outbound engine. Use when an outbound-engine agent must decide, before sourcing, enrichment, or outreach, whether a person is reuse / re-enrich / source / suppress / skip and how to route them. Decision-only: it reads Twenty and returns a verdict; callers (twenty-engine-sync, Apollo ingest, Clay enrichment, campaign assembly) perform the writes."
---

# Eligibility Gate

The single decision authority for "should we act on this person for this
campaign, and how." Every person entering the outbound loop passes the gate
first and lands on exactly one **verdict**: `reuse`, `re-enrich`, `source`,
`suppress`, or `skip`, plus a routing hint for the actionable three.

The gate is **deterministic code, not agent judgment** — same inputs, same
verdict, every run. The agent orchestrates (fetch the batch, act on the verdict
table, raise exceptions to a human); the verdict itself comes from
`demo/eligibility_gate.py`, never from per-lead reasoning. This is the decision
counterpart to `twenty-engine-sync` (which owns the reads/writes) and the
identity resolver (RL-439, which owns match / no-match / fuzzy / collision).

Decision-only. The gate never writes Twenty, never enriches, never contacts,
never changes schema or skills. Reads are free.

## Verdicts

- `suppress` — policy-excluded from this campaign (do-not-contact, existing
  client, blocklist, or already active in another campaign). Not re-eligible
  until policy changes.
- `skip` — not actionable now but not excluded: within TTL cooldown, awaiting
  human QA (fuzzy/collision), or no open channel. Re-runnable later.
- `source` — net-new, eligible. Caller creates the golden record, then routes.
- `re-enrich` — matched, enrichment stale or a required channel key missing.
  Caller refreshes via Clay, then routes.
- `reuse` — matched, enrichment fresh. Caller uses as-is, then routes.

## Decision order

Hard stops are evaluated before any verdict that implies spend, so the gate
never recommends `re-enrich` (a Clay credit cost) for a person it would
suppress. The full ordered logic + routing rules live in
`references/decision-order.md`. In short:

1. identity (consume the RL-439 outcome) — fuzzy/collision -> `skip` (QA).
2. hard suppression -> `suppress`.
3. active-campaign suppression (one active per person, global) -> `suppress`.
4. TTL / re-contact cooldown -> `skip`.
5. data verdict for eligible people -> `source` / `re-enrich` / `reuse`.
6. connection-aware routing; no open channel downgrades to `skip`.

## Operating loop

1. Resolve `engineConfig` (campaign override -> company default); read `ttlDays`
   (default 90), suppression rule, routing rules. Halt if neither config row
   exists.
2. Fetch the candidate batch from Twenty with the **suppression filters pushed
   into the query** so the database eliminates the obvious exclusions, not the
   agent. See `references/twenty-filter-strategy.md`.
3. Run the gate over the batch (`decide_batch`) to get one verdict row per
   person. This is read-only and deterministic.
4. Raise exceptions to a human: fuzzy/collision (`skip: awaiting-qa`) go to the
   QA queue / a Paperclip issue interaction; the issue waits in `in_review`.
5. Hand the verdict table to the caller. The gate writes nothing.

Completion criterion: every person in the batch carries exactly one verdict, and
every fuzzy/collision row is on the QA queue rather than silently decided.

## Reference implementation + demo

`demo/eligibility_gate.py` is the dependency-free decision layer (verdict order,
TTL math, routing). It performs no Twenty access. `demo/run_demo.py` exercises it
on the synthetic batch in `demo/sample_data.py`:

```sh
python3 demo/run_demo.py
```

Expected: 3 `suppress`, 4 `skip`, 1 `source`, 1 `re-enrich`, 1 `reuse`;
`Twenty reads/writes performed: 0`. The run asserts this distribution, so it
doubles as the fixture test for the canonical cases.

## Guarantees

Decision-only and deterministic. Forbidden: any Twenty write, membership
enroll, enrichment spend, outreach send, schema/metadata change, or Paperclip
skill install/attach. Halt (emit no verdict) on unresolvable `engineConfig`,
schema drift, or unavailable reads. Identity ambiguity does not halt — it
returns `skip` so the loop stays re-runnable.

## Callers

Operator pipeline: `outreach-gate` applies this verdict over a run's segment,
and `outreach-enrich` consults it to skip leads it would suppress before spend.

Engine: `twenty-engine-sync` (suppression/TTL/routing), RL-429 (Apollo ingest),
RL-430 (Clay enrichment), RL-431 (campaign assembly).
