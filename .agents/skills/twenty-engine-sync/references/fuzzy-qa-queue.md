# RL-441 — Fuzzy-match → human-QA review queue

Route fuzzy (name+company) candidates that are NOT exact-key matches to a
human-QA review queue. **No auto-merge on fuzzy, ever.**

## Scoring

- `name_score`: max of Jaro-Winkler (whole string) and token-set overlap
  (order-independent; drops corp stopwords like inc/llc/ltd/ab/gmbh).
- `company_score`: same blend on company name.
- `shared_email_domain`: small confidence nudge when domains match.
- `score = 0.65*name_score + 0.35*company_score (+0.05 domain)`, capped at 1.0.

## Thresholds

- `SURFACE_THRESHOLD = 0.72` — at/above, surface as a `fuzzy-candidate` to the queue.
- Below threshold → treated as `no-match` (net-new).
- `HIGH_CONFIDENCE = 0.90` — informational only; high scores still go to a human.

## Queue item shape

```json
{
  "candidate": "Priya Nair",
  "source": "apollo",
  "reason": "no exact key; name+company match",
  "matched_person_ids": ["p-003"],
  "score": 0.99,
  "evidence": {"name_score": 0.99, "company_score": 0.99, "shared_email_domain": false},
  "decision": "pending",
  "auto_merge": false
}
```

Cross-key and exact-key collisions also land here (with `score: null` and the
collision reason) because they need a human to decide one-vs-two records.

## Reviewer workflow

`decision: pending` → reviewer sets:
- `merge` → hand the chosen pair to the RL-440 merge planner (still approval-gated).
- `reject` → keep records separate; optionally record the candidate as net-new.

## Acceptance demonstrated (dry, on the synthetic sample)

`run_demo.py` builds 3 queue items: Priya (fuzzy, score ≈ 0.99), Sven (cross-key
collision), Lena (shared-email collision). `auto_merge` is `false` on all.

## Boundary

Human-gated. No auto-merge, no Twenty writes without approval.
