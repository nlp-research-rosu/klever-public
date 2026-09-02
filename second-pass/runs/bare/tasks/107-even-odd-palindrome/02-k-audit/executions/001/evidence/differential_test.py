#!/usr/bin/env python3
"""Independent differential test for HumanEval 107.

The oracle is the trusted mounted canonical implementation copied into the
isolated scratch directory.  The implementation under test is the candidate's
generated Python entry point copied into the same directory.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", ROOT / "canonical.py")
candidate = load_module("candidate_solution", ROOT / "solution.py")
oracle = canonical.even_odd_palindrome
actual = candidate.even_odd_palindrome

examples = {3: (1, 2), 12: (4, 6)}
for n, expected in examples.items():
    oracle_result = oracle(n)
    actual_result = actual(n)
    print(
        f"example n={n}: canonical={oracle_result} "
        f"candidate={actual_result} expected={expected}"
    )
    assert oracle_result == expected
    assert actual_result == expected

branch_points = [
    1, 2, 3, 8, 9, 10, 11, 12, 98, 99, 100, 101, 102, 109, 110,
    111, 120, 121, 191, 202, 292, 505, 909, 989, 999, 1000,
]
for n in branch_points:
    print(f"boundary n={n}: canonical={oracle(n)} candidate={actual(n)}")

rng = random.Random(107)
generated_points = sorted(rng.sample(range(1, 1001), 40))
print(f"seeded_generated_inputs={generated_points}")

branch_coverage = {
    "n_lt_10": set(),
    "pairs_gt_9": set(),
    "n_ge_101": set(),
    "lead_gt_9": set(),
    "candidate_le_n": set(),
    "lead_even": set(),
}
mismatches: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
for n in range(1, 1001):
    expected = oracle(n)
    observed = actual(n)
    if expected != observed:
        mismatches.append((n, expected, observed))

    branch_coverage["n_lt_10"].add(n < 10)
    if n >= 10:
        pairs = n // 11
        branch_coverage["pairs_gt_9"].add(pairs > 9)
        branch_coverage["n_ge_101"].add(n >= 101)
    if n >= 101:
        lead = n // 100
        branch_coverage["lead_gt_9"].add(lead > 9)
        if lead <= 9:
            middle = (n // 10) % 10
            palindrome_candidate = lead * 101 + middle * 10
            branch_coverage["candidate_le_n"].add(palindrome_candidate <= n)
        effective_lead = min(lead, 9)
        branch_coverage["lead_even"].add(effective_lead % 2 == 0)

for branch, outcomes in branch_coverage.items():
    print(f"branch_coverage {branch}={sorted(outcomes)}")
    assert outcomes == {False, True}, (branch, outcomes)

print(f"intended_domain=1..1000 tested=1000 mismatches={len(mismatches)}")
if mismatches:
    print(f"first_mismatches={mismatches[:20]}")
raise SystemExit(1 if mismatches else 0)
