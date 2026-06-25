"""Dry demonstration of the RL-428 eligibility gate on a synthetic batch.

Run:  python3 run_demo.py
No network, no Twenty, no writes. Prints the verdict a caller WOULD act on, then
asserts the expected verdict distribution so this doubles as a fixture test.
"""

from eligibility_gate import decide_batch, ACTIONABLE
from sample_data import sample_inputs, sample_config


EXPECTED = {"suppress": 3, "skip": 4, "source": 1, "re-enrich": 1, "reuse": 1}


def main():
    cfg = sample_config()
    rows = decide_batch(sample_inputs(), cfg)

    print("=" * 72)
    print("RL-428  Eligibility gate -- per-person verdict (read-only)")
    print("=" * 72)
    counts = {}
    for gi, v in rows:
        who = gi.person.name if gi.person else f"<{gi.outcome}>"
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
        route = ""
        if v["verdict"] in ACTIONABLE and v["routing"]:
            r = v["routing"]
            route = f"  -> {r['channel']}/{r['action']} via {r['account']}"
        print(f"[{v['verdict']:<10}] {who:<18} // {v['reason']}{route}")

    print("\nverdict counts:", counts)
    print("Twenty reads/writes performed: 0 (dry demonstration)")

    assert counts == EXPECTED, f"verdict distribution {counts} != expected {EXPECTED}"
    print("OK: verdict distribution matches the canonical-case expectation.")


if __name__ == "__main__":
    main()
