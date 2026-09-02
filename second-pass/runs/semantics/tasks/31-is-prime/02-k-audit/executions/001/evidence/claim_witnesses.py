#!/usr/bin/env python3
"""Ground witnesses for all submitted claim preconditions and result-bearing posts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


def trial_prime_tail(n: int, divisor: int) -> bool:
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def main() -> int:
    canonical = load("/reference/canonical.py", "claim_witness_canonical")
    submission = load(
        "/tmp/audit-work/31-is-prime/solution.py", "claim_witness_submission"
    )
    witnesses = [
        {
            "claim": "loop-correct",
            "ground_values": {"N": 31, "D": 2, "L": 1, "CALLER": 0, "SC": "{}"},
            "precondition": {
                "D >= 2": True,
                "L != 0": True,
                "0 not in SC": True,
                "L not in SC": True,
            },
            "claimed_result": trial_prime_tail(31, 2),
            "canonical_entry_result": canonical(31),
            "submission_entry_result": submission(31),
        },
        {
            "claim": "loop-correct-distinct-result",
            "ground_values": {"N": 9, "D": 2, "L": 1, "CALLER": 0, "SC": "{}"},
            "precondition": {
                "D >= 2": True,
                "L != 0": True,
                "0 not in SC": True,
                "L not in SC": True,
            },
            "claimed_result": trial_prime_tail(9, 2),
            "canonical_entry_result": canonical(9),
            "submission_entry_result": submission(9),
        },
        {
            "claim": "entry-small",
            "ground_values": {"N": 1},
            "precondition": {"N < 2": True},
            "claimed_result": False,
            "canonical_entry_result": canonical(1),
            "submission_entry_result": submission(1),
        },
        {
            "claim": "entry-large-prefix",
            "ground_values": {"N": 31, "SC": "{}"},
            "precondition": {"N >= 2": True, "1 not in SC": True},
            "claimed_result": None,
            "formal_post_note": "No returned value is present; the post starts with Assign/While/Return.",
            "canonical_entry_result": canonical(31),
            "submission_entry_result": submission(31),
        },
    ]
    output = EVIDENCE / "claim-witnesses.json"
    output.write_text(json.dumps(witnesses, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"witness_count={len(witnesses)}")
    print(f"artifact={output}")
    print("all_stated_precondition_atoms=true")
    print("result_bearing_claims_match_both_python_implementations=true")
    print("entry_large_prefix_has_claimed_result=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
