#!/usr/bin/env python3
"""Independent differential test for HumanEval/40.

The oracle and generated entry points are loaded from distinct, explicit paths.
The finite ordinary suite covers every short-list branch boundary exhaustively;
the final stress case checks the unrestricted-list contract near CPython's
default recursion boundary.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


CANONICAL = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/candidate-src/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load_entry(CANONICAL, "trusted_canonical")
generated = load_entry(GENERATED, "candidate_generated")

documented = [
    [1, 3, 5, 0],
    [1, 3, -2, 1],
    [1, 2, 3, 7],
    [2, 4, -5, 3, 9, 7],
    [1],
]

boundaries = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [1, -1],
    [1, -1, 0],
    [5, -2, -3],
    [5, -2, -2],
    [4, 9, 2, -11],
    [10**50, -(10**50), 0],
    [1, 1, -2],
    [1, 1, 1, -2],
    [9, 8, 7, 6, -13],
]

# All lists through length six over [-3, 3]: 137,257 concrete inputs.
exhaustive = (
    list(values)
    for length in range(7)
    for values in itertools.product(range(-3, 4), repeat=length)
)

rng = random.Random(400026)
generated_samples = [
    [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 18))]
    for _ in range(2000)
]

ordinary_count = 0
ordinary_mismatches: list[tuple[list[int], object, object]] = []
for values in itertools.chain(documented, boundaries, exhaustive, generated_samples):
    expected = canonical(values)
    actual = generated(values)
    ordinary_count += 1
    if actual != expected or type(actual) is not type(expected):
        ordinary_mismatches.append((values, expected, actual))
        if len(ordinary_mismatches) >= 20:
            break

# The first element has no completing pair.  The oracle reaches the triple at
# positions (1, 2, 3) after about 500k checks; the recursive rewrite must scan
# the roughly 1000-element suffix before it can move to that same first index.
stress = [10**9, 1, -1, 0] + [2] * 997
stress_expected = canonical(stress)
try:
    stress_actual: object = generated(stress)
except Exception as error:  # The exception class is material evidence.
    stress_actual = f"{type(error).__name__}: {error}"

stress_mismatch = (
    stress_actual != stress_expected
    or type(stress_actual) is not type(stress_expected)
)

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print("exhaustive_domain=lengths 0..6, values -3..3")
print(f"random_seed=400026 random_cases={len(generated_samples)} lengths=0..18")
print(f"ordinary_cases_run={ordinary_count}")
print(f"ordinary_mismatch_count={len(ordinary_mismatches)}")
for mismatch in ordinary_mismatches:
    print(f"ordinary_mismatch={mismatch!r}")
print(f"stress_length={len(stress)}")
print(f"stress_oracle={stress_expected!r}")
print(f"stress_generated={stress_actual!r}")
print(f"stress_mismatch={stress_mismatch}")

raise SystemExit(1 if ordinary_mismatches or stress_mismatch else 0)
