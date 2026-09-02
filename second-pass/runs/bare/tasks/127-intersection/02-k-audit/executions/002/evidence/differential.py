#!/usr/bin/env python3
"""Independent Stage-2 differential test for HumanEval 127."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


REFERENCE = Path("/tmp/audit-work/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/candidate-src/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


canonical = load_entry(REFERENCE, "trusted_canonical_127")
generated = load_entry(CANDIDATE, "generated_solution_127")


def contract_oracle(interval1: tuple[int, int], interval2: tuple[int, int]) -> str:
    """Independent primality oracle over geometric intersection length."""
    length = min(interval1[1], interval2[1]) - max(interval1[0], interval2[0])
    if length < 2:
        return "NO"
    divisor = 2
    while divisor <= length // divisor:
        if length % divisor == 0:
            return "NO"
        divisor += 1
    return "YES"


named_cases = [
    ("prompt_touch", (1, 2), (2, 3)),
    ("prompt_length_1", (-1, 1), (0, 4)),
    ("prompt_length_2", (-3, -1), (-5, 5)),
    ("canonical_doc_length_5", (-3, 9), (-1, 4)),
    ("both_degenerate_same", (0, 0), (0, 0)),
    ("first_degenerate_inside", (3, 3), (0, 8)),
    ("second_degenerate_inside", (0, 8), (3, 3)),
    ("disjoint_gap", (-10, -4), (2, 9)),
    ("reversed_order_disjoint", (2, 9), (-10, -4)),
    ("intersection_length_0", (0, 3), (3, 7)),
    ("intersection_length_1", (0, 3), (2, 7)),
    ("intersection_length_2_prime", (0, 3), (1, 7)),
    ("intersection_length_3_prime", (0, 3), (0, 7)),
    ("intersection_length_4_composite", (0, 4), (0, 7)),
    ("intersection_length_5_prime", (-5, 0), (-8, 8)),
    ("intersection_length_9_composite", (-9, 0), (-20, 20)),
    ("large_prime_101", (0, 101), (-50, 200)),
    ("large_composite_121", (0, 121), (-50, 200)),
    ("spec_case_1", (0, 5), (-2, 7)),
    ("spec_case_2", (0, 5), (-2, 3)),
    ("spec_case_3", (0, 5), (2, 7)),
    ("spec_case_4", (0, 5), (2, 4)),
]

mismatches: list[tuple] = []
branch_counts = {"C<=A,D>=B": 0, "C<=A,D<B": 0, "C>A,D>=B": 0, "C>A,D<B": 0}


def check(label: str, interval1: tuple[int, int], interval2: tuple[int, int]) -> None:
    assert interval1[0] <= interval1[1]
    assert interval2[0] <= interval2[1]
    expected = contract_oracle(interval1, interval2)
    cvalue = canonical(interval1, interval2)
    gvalue = generated(interval1, interval2)
    key = (
        ("C<=A" if interval2[0] <= interval1[0] else "C>A")
        + ","
        + ("D>=B" if interval2[1] >= interval1[1] else "D<B")
    )
    branch_counts[key] += 1
    if cvalue != expected or gvalue != expected:
        mismatches.append((label, interval1, interval2, expected, cvalue, gvalue))


for label, interval1, interval2 in named_cases:
    check(label, interval1, interval2)

intervals = [(a, b) for a in range(-8, 9) for b in range(a, 9)]
for interval1 in intervals:
    for interval2 in intervals:
        check("grid", interval1, interval2)

rng = random.Random(127)
for index in range(5000):
    a, b = sorted((rng.randint(-10000, 10000), rng.randint(-10000, 10000)))
    c, d = sorted((rng.randint(-10000, 10000), rng.randint(-10000, 10000)))
    check(f"random-{index}", (a, b), (c, d))

print(f"named_cases={len(named_cases)}")
print(f"exhaustive_grid_cases={len(intervals) ** 2}")
print("random_cases=5000 seed=127 endpoints=[-10000,10000]")
print(f"branch_counts={branch_counts}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", mismatch)
    raise SystemExit(1)
