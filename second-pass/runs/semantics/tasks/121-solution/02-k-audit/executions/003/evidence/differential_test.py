#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 121."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


canonical = load_entry("trusted_canonical_121", Path("/reference/canonical.py"))
generated = load_entry(
    "candidate_generated_121", Path("/tmp/audit-work/reconstruction/solution.py")
)

# Named cases cover all examples; empty/one-element boundaries; odd/even values
# at both even and odd positions; zero; negative Python-modulo behavior; and
# unbounded-Int-sized values.
named_cases = [
    ("example-1", [5, 8, 7, 1]),
    ("example-2", [3, 3, 3, 3, 3]),
    ("example-3", [30, 13, 24, 321]),
    ("empty-extension", []),
    ("single-zero", [0]),
    ("single-positive-even", [2]),
    ("single-positive-odd", [7]),
    ("single-negative-even", [-4]),
    ("single-negative-odd", [-5]),
    ("odd-index-values-ignored", [2, 9, 4, -7]),
    ("all-branch-combinations", [-5, -4, -3, -2, -1, 0, 1, 2]),
    ("large-magnitudes", [10**100 + 1, -(10**120 + 1), -(10**99 + 1)]),
]

mismatches: list[tuple[str, list[int], int, int]] = []
tested = 0
for label, values in named_cases:
    expected = canonical(values)
    actual = generated(values)
    tested += 1
    if actual != expected:
        mismatches.append((label, values, expected, actual))

# Exhaust every list through length five over a small sign/parity basis.
small_basis = (-3, -2, -1, 0, 1, 2, 3)
for length in range(0, 6):
    for values_tuple in itertools.product(small_basis, repeat=length):
        values = list(values_tuple)
        expected = canonical(values)
        actual = generated(values)
        tested += 1
        if actual != expected:
            mismatches.append((f"exhaustive-length-{length}", values, expected, actual))

# Deterministic broader representatives exercise longer lists and large values.
seed = 121_20260726
rng = random.Random(seed)
for case_number in range(10_000):
    length = rng.randint(1, 80)
    values = [rng.randint(-(10**30), 10**30) for _ in range(length)]
    expected = canonical(values)
    actual = generated(values)
    tested += 1
    if actual != expected:
        mismatches.append((f"random-{case_number}", values, expected, actual))

print("oracle: /reference/canonical.py:solution")
print("candidate: /tmp/audit-work/reconstruction/solution.py:solution")
print("named_cases:", len(named_cases))
print("exhaustive_basis:", small_basis)
print("exhaustive_lengths: 0..5")
print("random_seed:", seed)
print("random_cases: 10000, lengths 1..80, values in [-10^30, 10^30]")
print("total_cases:", tested)
print("mismatch_count:", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH:", mismatch)
raise SystemExit(1 if mismatches else 0)
