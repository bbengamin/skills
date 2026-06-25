"""Dry demonstration of the RL-427 identity + merge wave on a synthetic sample.

Run:  python3 run_demo.py
No network, no Twenty, no writes. Prints what the engine WOULD do.
"""

import json

from engine_identity import (
    resolve, plan_merge_from_candidate, plan_merge_two_persons,
    build_queue_item, MATCH, FUZZY_CANDIDATE, COLLISION,
)
from sample_data import sample_people, sample_candidates


def rule(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def main():
    people = sample_people()
    by_id = {p.id: p for p in people}
    queue = []

    rule("RL-439  Identity resolver -- match keys + precedence (read-only)")
    resolutions = []
    for c in sample_candidates():
        r = resolve(c, people)
        resolutions.append((c, r))
        line = (f"[{r['outcome']:<15}] {c.name:<14} src={c.source:<7} "
                f"by={str(r['matched_by']):<11} -> {r['person_ids'] or '-'}")
        if r["fills_missing_key"]:
            line += f"  (+fills {r['fills_missing_key']})"
        if r["reason"]:
            line += f"  // {r['reason']}"
        print(line)

    rule("RL-440  Auto-merge + survivorship (dry plans)")
    # exact-key match that supplies a missing channel key -> merge-from-candidate
    for c, r in resolutions:
        if r["outcome"] == MATCH and r["fills_missing_key"]:
            person = by_id[r["person_ids"][0]]
            plan = plan_merge_from_candidate(person, c)
            print(f"\nmerge candidate ({c.source}) into {person.id} [{person.name}]:")
            print(json.dumps(plan, indent=2, default=list))

    # two existing Person records that are the same human (Sven p-010 + p-011)
    plan2 = plan_merge_two_persons(by_id["p-010"], by_id["p-011"])
    print("\nmerge two persons p-010 + p-011 (same human, split channels):")
    print(json.dumps(plan2, indent=2, default=list))

    rule("RL-441  Fuzzy / collision -> human-QA review queue (no auto-merge)")
    for c, r in resolutions:
        if r["outcome"] in (FUZZY_CANDIDATE, COLLISION):
            item = build_queue_item(r)
            queue.append(item)
    print(json.dumps(queue, indent=2, default=list))

    rule("Summary")
    counts = {}
    for _, r in resolutions:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    print("resolution outcomes:", json.dumps(counts))
    print(f"QA queue items: {len(queue)} (auto-merge on fuzzy: never)")
    print("Twenty writes performed: 0 (dry demonstration)")


if __name__ == "__main__":
    main()
