# RL-439 — Identity resolver: match keys + precedence

Given a candidate contact (Apollo, Clay, or LinkedIn), decide whether it maps to
an existing Twenty Person. Read-only: the resolver classifies, it never writes.

## Inputs / outputs

Input: a candidate with any of `linkedinUrl`, `email`, `name`, `companyName`.
Output: exactly one outcome.

| Outcome | Meaning | Next step |
| --- | --- | --- |
| `match` | Exactly one Person via an exact key | additive update by id (RL-440) |
| `no-match` | No exact key, no fuzzy candidate over threshold | net-new create (downstream) |
| `fuzzy-candidate` | No exact key, ≥1 name+company candidate ≥ threshold | human-QA queue (RL-441) |
| `collision` | Exact-key collision or cross-key conflict | human-QA queue (RL-441) |

## Match-key normalization

- **linkedinUrl**: lowercase; drop scheme/host/`www`/`linkedin.com`; drop query
  and fragment; strip trailing slash. `http://linkedin.com/in/x/` and
  `https://www.linkedin.com/in/x?utm=1` both key to `in/x`.
- **email**: lowercase + trim. Plus-addressing and dotted gmail localparts are
  **not** folded — that is a lossy assumption left to an explicit opt-in rule.

## Precedence

1. Exact `linkedinUrl` match (one Person) → `match` by linkedinUrl.
2. Else exact `email` match (one Person) → `match` by email.
3. Else fuzzy `name`+`company` ≥ surface threshold → `fuzzy-candidate`.
4. Else → `no-match` (net-new).

## Collision rules (never auto-resolve)

- Two+ Persons share the candidate's linkedinUrl → `collision`.
- Two+ Persons share the candidate's email (and no linkedinUrl match) → `collision`.
- linkedinUrl resolves to Person A and email resolves to Person B, A ≠ B →
  `collision` (cross-key): a likely two-record merge, sent to QA.

## Missing-key fill

When a `match` candidate carries a channel key the matched Person lacks
(e.g. LinkedIn-keyed Person + candidate email), the resolver flags
`fills_missing_key`. RL-440 turns that into an additive fill — this is how the
golden record gets both keys for omnichannel.

## Acceptance demonstrated (dry, on the synthetic sample)

`python3 demo/run_demo.py` →
`match` (Dana, fills email), `match` (Marco, by linkedinUrl despite messy URL),
`no-match` (Quinn), `fuzzy-candidate` (Priya), `collision` cross-key (Sven),
`collision` shared-email (Lena). Zero Twenty reads/writes.

## Boundary

Read-only resolution. No Twenty writes. Live lookups use `find_many_people`
through the `twenty-engine-sync` query rules; this module is the decision layer.
