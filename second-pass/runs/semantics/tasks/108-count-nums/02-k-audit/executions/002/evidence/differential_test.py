#!/usr/bin/env python3
"""Independent differential test: trusted HumanEval canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_nums


canonical = load_function("trusted_canonical_108", ROOT / "canonical.py")
candidate = load_function("submitted_solution_108", ROOT / "solution.py")

documented = [
    [],
    [-1, 11, -11],
    [1, 1, 2],
]

# Boundaries cover both digit loops and all decisions:
# n < 0 vs n >= 0; magnitude < 10 vs >= 10; while continuation at 10;
# signed digit sum <= 0 vs > 0; decimal carry boundaries; and zero.
boundary_values = [
    -1000, -999, -110, -109, -101, -100, -99, -21, -20, -19,
    -12, -11, -10, -9, -2, -1, 0, 1, 2, 9, 10, 11, 12,
    19, 20, 21, 99, 100, 101, 109, 110, 999, 1000,
]
boundaries = [[value] for value in boundary_values]
boundaries += [
    boundary_values,
    list(reversed(boundary_values)),
    [-99999999999999999999999999999999999999, 99999999999999999999999999999999999999],
    [-101, -100, -99, -12, -11, -10, -9, -1, 0, 1, 9, 10, 11, 12, 99, 100, 101],
]

# Exhaust all lists through length 4 over a compact value set selected to
# exercise the result-class and loop boundaries.
small_values = [-101, -11, -10, -1, 0, 1, 10, 11, 101]
exhaustive = [
    list(values)
    for length in range(5)
    for values in itertools.product(small_values, repeat=length)
]

rng = random.Random(108_20260726)
generated: list[list[int]] = []
for _ in range(2000):
    arr: list[int] = []
    for _ in range(rng.randrange(0, 21)):
        digits = rng.randrange(1, 101)
        magnitude = rng.randrange(10 ** (digits - 1), 10 ** digits)
        arr.append(-magnitude if rng.randrange(2) else magnitude)
    generated.append(arr)

cases = documented + boundaries + exhaustive + generated
mismatches: list[tuple[list[int], int, int]] = []
for arr in cases:
    expected = canonical(arr)
    actual = candidate(arr)
    if actual != expected:
        mismatches.append((arr, expected, actual))

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_small_cases={len(exhaustive)}")
print(f"generated_cases={len(generated)}")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH={mismatch!r}")
assert not mismatches
print("DIFFERENTIAL_RESULT=PASS")
