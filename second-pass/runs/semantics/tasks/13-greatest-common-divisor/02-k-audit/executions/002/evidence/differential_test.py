#!/usr/bin/env python3
"""Independent generated-vs-canonical differential and math.gcd comparison."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function("generated_solution", Path("/tmp/audit-work/gcd/solution.py"))

# Integers have no empty value; (0, 0) is the zero/empty-magnitude boundary.
# These fixed cases cover both prompt examples, b == 0 versus b != 0,
# signs in each position, equal values, divisibility, coprimality, and large ints.
fixed_cases = [
    (3, 5),
    (25, 15),
    (0, 0),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (-1, -1),
    (-54, 24),
    (54, -24),
    (-54, -24),
    (13, 17),
    (17, 13),
    (20, 5),
    (5, 20),
    (2**127 - 1, 2**61 - 1),
    (-(2**127 - 1), 2**61 - 1),
    (2**127 - 1, -(2**61 - 1)),
]

all_cases = list(fixed_cases)
all_cases.extend((a, b) for a in range(-100, 101) for b in range(-100, 101))
rng = random.Random(130013)
all_cases.extend(
    (
        rng.randint(-(2**255), 2**255),
        rng.randint(-(2**255), 2**255),
    )
    for _ in range(1000)
)

seen = set()
unique_cases = []
for case in all_cases:
    if case not in seen:
        seen.add(case)
        unique_cases.append(case)

candidate_math_mismatches = []
canonical_math_mismatches = []
candidate_canonical_mismatches = []
for a, b in unique_cases:
    expected = math.gcd(a, b)
    got_generated = generated(a, b)
    got_canonical = canonical(a, b)
    if got_generated != expected:
        candidate_math_mismatches.append((a, b, got_generated, expected))
    if got_canonical != expected:
        canonical_math_mismatches.append((a, b, got_canonical, expected))
    if got_generated != got_canonical:
        candidate_canonical_mismatches.append((a, b, got_generated, got_canonical))

print(f"unique_cases={len(unique_cases)}")
print(f"candidate_vs_math_gcd_mismatches={len(candidate_math_mismatches)}")
print(f"canonical_vs_math_gcd_mismatches={len(canonical_math_mismatches)}")
print(f"candidate_vs_canonical_mismatches={len(candidate_canonical_mismatches)}")
print("first_candidate_vs_canonical_mismatches=")
for mismatch in candidate_canonical_mismatches[:12]:
    print(mismatch)

# The generated implementation must meet the natural-language gcd contract.
raise SystemExit(1 if candidate_math_mismatches else 0)
