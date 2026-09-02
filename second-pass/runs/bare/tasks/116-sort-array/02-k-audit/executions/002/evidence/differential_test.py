#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 116."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


ROOT = Path("/tmp/audit-work")
canonical = load_function("trusted_canonical", ROOT / "reference/canonical.py")
generated = load_function("generated_solution", ROOT / "candidate/solution.py")

documented = [
    [1, 5, 2, 3, 4],
    [-2, -3, -4, -5, -6],
    [1, 0, 2, 3, 4],
]

boundary = [
    [],
    [0],
    [1],
    [2, 1],
    [3, 5],             # equal popcount, ascending decimal already
    [5, 3],             # equal popcount, decimal tie-break reverses
    [1, 2, 4, 8],       # equal popcount throughout
    [8, 7],             # one-bit value precedes three-bit value
    [7, 8],             # already ordered by popcount
    [0, 0, 1, 1],
    [2**63, 2**63 - 1, 0, 3],
    [1, 5, 2, 3],       # first symbolic length beyond the proof's pair cases
    [1, 5, 2, 3, 4],    # length beyond every symbolic end-to-end claim
]

cases: list[tuple[str, list[int]]] = []
cases.extend(("documented", case) for case in documented)
cases.extend(("boundary", case) for case in boundary)

# Complete finite grid: every list of length 0..5 over values 0..5.
for length in range(6):
    for values in itertools.product(range(6), repeat=length):
        cases.append(("exhaustive_nonnegative", list(values)))

# Broader deterministic intended-domain sample.
rng = random.Random(116)
for _ in range(3000):
    length = rng.randrange(0, 21)
    cases.append(
        (
            "random_nonnegative",
            [rng.randrange(0, 2**80) for _ in range(length)],
        )
    )

# Out-of-contract evidence for the prompt's contradictory negative example.
for _ in range(1000):
    length = rng.randrange(0, 16)
    cases.append(
        (
            "random_mixed_sign",
            [rng.randrange(-(2**40), 2**40) for _ in range(length)],
        )
    )

mismatches: list[tuple[str, list[int], object, object]] = []
mutations = 0
counts: dict[str, int] = {}
for group, values in cases:
    counts[group] = counts.get(group, 0) + 1
    canonical_input = list(values)
    generated_input = list(values)
    expected = canonical(canonical_input)
    actual = generated(generated_input)
    if canonical_input != values or generated_input != values:
        mutations += 1
    if expected != actual:
        mismatches.append((group, values, expected, actual))

print("oracle: trusted canonical.py sort_array, imported independently")
print("subject: candidate solution.py sort_array, imported independently")
print("intended domain: finite lists of non-negative Python integers")
print("exhaustive scope: every list of length 0..5 over values 0..5")
print("random seed: 116")
print("random nonnegative scope: 3000 lists, length 0..20, values 0..2**80-1")
print("mixed-sign supplemental scope: 1000 lists, length 0..15")
for group in sorted(counts):
    print(f"cases[{group}]={counts[group]}")
print(f"total_cases={len(cases)}")
print(f"input_mutations={mutations}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:10]:
    print(f"MISMATCH {mismatch!r}")

print("documented_outputs:")
for case in documented:
    print(f"  {case!r} -> canonical={canonical(case)!r}, generated={generated(case)!r}")

raise SystemExit(1 if mismatches or mutations else 0)
