#!/usr/bin/env python3
"""Finite witnesses supporting the exhaustive arithmetic rule review."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/122-add-elements")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_equations", SCRATCH / "canonical.py")
candidate = load("candidate_equations", SCRATCH / "solution.py")


def candidate_contribution(value: int) -> int:
    return value if -100 < value and value < 100 else 0


def canonical_contribution(value: int) -> int:
    return value if len(str(value)) <= 2 else 0


overlaps = []
uncovered = []
candidate_rule_mismatches = []
canonical_rule_mismatches = []
for value in range(-1000, 1001):
    first_guard = -100 < value and value < 100
    second_guard = value <= -100 or value >= 100
    if first_guard and second_guard:
        overlaps.append(value)
    if not first_guard and not second_guard:
        uncovered.append(value)
    if candidate_contribution(value) != (value if first_guard else 0):
        candidate_rule_mismatches.append(value)
    if candidate_contribution(value) != canonical_contribution(value):
        canonical_rule_mismatches.append(value)

print("smallContribution_guard_overlaps:", overlaps)
print("smallContribution_guard_uncovered:", uncovered)
print("candidate_equation_mismatches:", candidate_rule_mismatches)
print(
    "canonical_mismatch_interval:",
    (min(canonical_rule_mismatches), max(canonical_rule_mismatches)),
)
print("canonical_mismatch_count_in_-1000_to_1000:", len(canonical_rule_mismatches))

rng = random.Random(12205)
summary_candidate_mismatches = 0
summary_canonical_mismatches = 0
for _ in range(1000):
    length = rng.randint(1, 100)
    arr = [rng.randint(-10000, 10000) for _ in range(length)]
    k = rng.randint(1, length)
    summary = sum(candidate_contribution(value) for value in arr[:k])
    if summary != candidate.add_elements(arr, k):
        summary_candidate_mismatches += 1
    if summary != canonical.add_elements(arr, k):
        summary_canonical_mismatches += 1

print("sumRange_vs_candidate_mismatches:", summary_candidate_mismatches)
print("sumRange_vs_canonical_mismatches:", summary_canonical_mismatches)
raise SystemExit(0)
