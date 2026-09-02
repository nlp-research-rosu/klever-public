#!/usr/bin/env python3
"""Independent canonical-vs-generated differential tests for HumanEval 72."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random


SCRATCH = Path("/tmp/audit-work/72-will-it-fly-audit")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


canonical = load_function(SCRATCH / "reference/canonical.py", "trusted_canonical")
generated = load_function(SCRATCH / "candidate/solution.py", "generated_solution")


DOCUMENTED_AND_BOUNDARY_CASES = [
    ("example-unbalanced", [1, 2], 5),
    ("example-overweight", [3, 2, 3], 1),
    ("example-balanced", [3, 2, 3], 9),
    ("example-singleton", [3], 5),
    ("empty-at-bound", [], 0),
    ("empty-overweight", [], -1),
    ("singleton-at-bound", [3], 3),
    ("singleton-overweight", [3], 2),
    ("two-palindrome-at-bound", [2, 2], 4),
    ("two-mismatch-underweight", [2, 3], 5),
    ("odd-palindrome-at-bound", [-1, 4, -1], 2),
    ("odd-middle-mismatch", [1, 2, 3, 2, 9], 20),
    ("even-inner-mismatch", [1, 2, 3, 1], 7),
    ("negative-sum-negative-bound-true", [-3, 1, -3], -5),
    ("negative-sum-negative-bound-false", [-3, 1, -3], -6),
    ("large-integers", [10**40, -10**40, 10**40], 10**40),
]


def check(q: list[int], w: int, label: str) -> None:
    global checked
    expected = canonical(list(q), w)
    actual = generated(list(q), w)
    checked += 1
    if type(expected) is not bool or type(actual) is not bool or actual != expected:
        mismatches.append((label, q, w, expected, actual))


checked = 0
mismatches: list[tuple[object, ...]] = []

for label, q, w in DOCUMENTED_AND_BOUNDARY_CASES:
    check(q, w, label)

# Exhaust all lists over {-2,-1,0,1,2} through length 6, with weight bounds
# around and beyond every possible sum in that finite region.
for length in range(7):
    for values in product(range(-2, 3), repeat=length):
        q = list(values)
        for w in range(-13, 14):
            check(q, w, f"exhaustive-length-{length}")

# Broader deterministic samples cover longer lists and unbounded Python ints.
rng = random.Random(720072)
for index in range(20_000):
    length = rng.randrange(0, 65)
    q = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
    if index % 4 == 0:
        q = q[: (length + 1) // 2] + q[: length // 2][::-1]
    choices = [sum(q) - 1, sum(q), sum(q) + 1, rng.randrange(-(10**15), 10**15)]
    check(q, choices[index % len(choices)], f"generated-{index}")

print(f"documented_and_boundary_cases={len(DOCUMENTED_AND_BOUNDARY_CASES)}")
print("exhaustive_lengths=0..6 values=-2..2 weights=-13..13")
print("deterministic_generated_cases=20000 seed=720072 lengths=0..64")
print(f"comparisons={checked}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
