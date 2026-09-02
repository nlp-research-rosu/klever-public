#!/usr/bin/env python3
"""Independent candidate/canonical/math-GCD differential over documented cases."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[int, int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/source/solution.py"), "generated_solution"
)

explicit = [
    (3, 5),       # prompt example
    (25, 15),     # prompt example
    (0, 0),       # both zero and zero-iteration loop
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (-1, 1),
    (1, -1),
    (-1, -1),
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (25, -15),
    (-25, 15),
    (-25, -15),
    (2**63 - 1, 2**31 - 1),
    (-(2**63), 2**31 - 1),
]

grid = [(a, b) for a in range(-20, 21) for b in range(-20, 21)]
rng = random.Random(130013)
random_cases = [
    (rng.randint(-10**12, 10**12), rng.randint(-10**12, 10**12))
    for _ in range(1000)
]

cases: list[tuple[int, int]] = []
seen: set[tuple[int, int]] = set()
for case in explicit + grid + random_cases:
    if case not in seen:
        cases.append(case)
        seen.add(case)

candidate_canonical_mismatches: list[tuple[int, int, int, int]] = []
candidate_math_mismatches: list[tuple[int, int, int, int]] = []
canonical_math_mismatches: list[tuple[int, int, int, int]] = []

print("input_scope=20 explicit + exhaustive grid [-20,20]^2 + 1000 seeded pairs")
print("seed=130013")
print("empty_case_note=scalar signature has no empty collection; (0,0) is the empty-loop boundary")
print(f"unique_case_count={len(cases)}")
print("explicit_results:")
for a, b in explicit:
    generated_result = generated(a, b)
    canonical_result = canonical(a, b)
    math_result = math.gcd(a, b)
    print(
        f"  ({a},{b}) generated={generated_result} "
        f"canonical={canonical_result} math.gcd={math_result}"
    )

for a, b in cases:
    generated_result = generated(a, b)
    canonical_result = canonical(a, b)
    math_result = math.gcd(a, b)
    if generated_result != canonical_result:
        candidate_canonical_mismatches.append(
            (a, b, generated_result, canonical_result)
        )
    if generated_result != math_result:
        candidate_math_mismatches.append((a, b, generated_result, math_result))
    if canonical_result != math_result:
        canonical_math_mismatches.append((a, b, canonical_result, math_result))

print(
    "generated_vs_canonical_mismatch_count="
    f"{len(candidate_canonical_mismatches)}"
)
print(f"generated_vs_math_gcd_mismatch_count={len(candidate_math_mismatches)}")
print(f"canonical_vs_math_gcd_mismatch_count={len(canonical_math_mismatches)}")
print("first_generated_vs_canonical_mismatches:")
for row in candidate_canonical_mismatches[:20]:
    print(f"  a={row[0]} b={row[1]} generated={row[2]} canonical={row[3]}")

raise SystemExit(1 if candidate_canonical_mismatches else 0)
