#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py vs submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "submitted_solution",
    Path("/tmp/audit-work/30-get-positive/solution.py"),
)

named_cases = [
    ("documented-1", [-1, 2, -4, 5, 6]),
    ("documented-2", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]),
    ("empty", []),
    ("branch-boundary-int", [-1, 0, 1]),
    ("branch-boundary-float", [-0.1, -0.0, 0.0, 0.1]),
    ("all-negative-and-zero", [-10, -1, 0]),
    ("all-positive", [1, 2, 3]),
    ("duplicates-order", [2, -1, 2, 0, 1, 2]),
    ("large-ints", [-(10**100), -1, 0, 1, 10**100]),
    ("bool-number-subclass", [False, True, 0, 1, -1]),
    ("float-extremes", [-math.inf, -1.5, math.nan, 0.0, 1.5, math.inf]),
]

cases = list(named_cases)

# Exhaust all lists through length five over representatives on both sides of
# the sole x > 0 branch boundary.
alphabet = [-3, -1, 0, 1, 3]
for length in range(6):
    for values in itertools.product(alphabet, repeat=length):
        cases.append((f"exhaustive-int-len-{length}", list(values)))

# Add a deterministic broader sample of integer and finite-float lists.
rng = random.Random(30030)
for index in range(1000):
    length = rng.randrange(0, 31)
    if index % 2:
        values = [rng.randint(-10**9, 10**9) for _ in range(length)]
    else:
        values = [rng.uniform(-10**6, 10**6) for _ in range(length)]
        if values:
            values[index % length] = 0.0
    cases.append((f"seeded-random-{index}", values))

mismatches = []
for label, values in cases:
    expected = canonical(list(values))
    actual = generated(list(values))
    if actual != expected:
        mismatches.append((label, values, expected, actual))

print(f"oracle=/reference/canonical.py:get_positive")
print(f"subject=/tmp/audit-work/30-get-positive/solution.py:get_positive")
print(f"named_cases={len(named_cases)}")
print(f"exhaustive_alphabet={alphabet!r}")
print("exhaustive_lengths=0..5")
print("random_seed=30030")
print("random_cases=1000")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)

