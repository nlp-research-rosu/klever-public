#!/usr/bin/env python3
"""Independent differential audit for problem 127-intersection."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/127-intersection/trusted")
CANDIDATE = Path("/tmp/audit-work/127-intersection/candidate-src")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


canonical = load_entry("trusted_canonical", TRUSTED / "canonical.py")
generated = load_entry("audited_solution", CANDIDATE / "solution.py")


documented_and_boundary_cases = [
    ((1, 2), (2, 3), "prompt: touching endpoints / length 0"),
    ((-1, 1), (0, 4), "prompt: overlap length 1"),
    ((-3, -1), (-5, 5), "prompt: overlap length 2"),
    ((5, 5), (5, 5), "degenerate closed intervals"),
    ((0, 0), (1, 1), "disjoint degenerate intervals"),
    ((0, 1), (1, 2), "length 0 boundary"),
    ((0, 1), (0, 1), "length 1 boundary"),
    ((0, 2), (0, 2), "length 2 / prime boundary"),
    ((0, 3), (0, 3), "length 3 / loop non-divisor"),
    ((0, 4), (0, 4), "length 4 / first divisor"),
    ((0, 5), (0, 5), "length 5 / prime loop"),
    ((0, 6), (0, 6), "length 6 / multiple divisors"),
    ((-10, -3), (-8, -1), "negative endpoints"),
    ((0, 20), (3, 14), "second interval strictly inside"),
    ((3, 14), (0, 20), "first interval strictly inside"),
    ((0, 5), (2, 10), "left=max(second), right=min(first)"),
    ((2, 10), (0, 5), "left=max(first), right=min(second)"),
    ((10**18, 10**18 + 5), (10**18 + 1, 10**18 + 4), "large integers"),
    ((-10**18 - 5, -10**18), (-10**18 - 4, -10**18 - 1), "large negatives"),
]


cases: list[tuple[tuple[int, int], tuple[int, int], str]] = list(
    documented_and_boundary_cases
)

# Exhaust all ordered intervals over a small domain. This covers both choices
# of max/min, disjointness, all return branches, and composite/prime loop paths.
small_intervals = [
    (start, end)
    for start in range(-8, 9)
    for end in range(start, 9)
]
for first, second in itertools.product(small_intervals, repeat=2):
    cases.append((first, second, "exhaustive endpoints [-8,8]"))

# Add a deterministic broader sample without sharing implementation logic.
rng = random.Random(127)
for _ in range(2_000):
    a0, a1 = sorted((rng.randint(-100, 100), rng.randint(-100, 100)))
    b0, b1 = sorted((rng.randint(-100, 100), rng.randint(-100, 100)))
    cases.append(((a0, a1), (b0, b1), "seeded generated sample"))


mismatches = []
digest = hashlib.sha256()
result_counts = {"YES": 0, "NO": 0}
for index, (first, second, label) in enumerate(cases):
    expected = canonical(first, second)
    actual = generated(first, second)
    result_counts[actual] = result_counts.get(actual, 0) + 1
    record = [first, second, expected, actual, label]
    digest.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
    if expected != actual:
        mismatches.append(
            {
                "index": index,
                "interval1": first,
                "interval2": second,
                "canonical": expected,
                "generated": actual,
                "label": label,
            }
        )

summary = {
    "oracle": str(TRUSTED / "canonical.py"),
    "candidate": str(CANDIDATE / "solution.py"),
    "documented_boundary_cases": len(documented_and_boundary_cases),
    "small_ordered_intervals": len(small_intervals),
    "exhaustive_ordered_pairs": len(small_intervals) ** 2,
    "seed": 127,
    "generated_cases": 2_000,
    "total_cases": len(cases),
    "result_counts": result_counts,
    "mismatch_count": len(mismatches),
    "case_result_sha256": digest.hexdigest(),
    "mismatches": mismatches[:20],
}
print(json.dumps(summary, indent=2, sort_keys=True))
sys.exit(1 if mismatches else 0)
