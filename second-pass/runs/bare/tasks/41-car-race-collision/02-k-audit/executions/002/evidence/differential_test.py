#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for task 41."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.car_race_collision


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_solution", Path("/tmp/audit-work/candidate/solution.py")
)

# The prompt contains no literal examples. For the count domain, 0 is the empty
# case and 1 is the smallest nonempty boundary. The implementation has no
# branches. Large cases exercise Python's unbounded integers.
fixed_intended = [0, 1, 2, 3, 10, 41, 100, 10**6, 10**20, 10**100]

rng = random.Random(410041)
generated_intended = [rng.randrange(0, 10**12 + 1) for _ in range(1000)]

# These are outside the natural "n cars" count domain, but they document that
# both Python functions nevertheless agree over representative negative ints.
observational_negative = [-1, -2, -10, -(10**20)]
observational_negative += [-rng.randrange(1, 10**12 + 1) for _ in range(100)]

cases = fixed_intended + generated_intended + observational_negative
mismatches = []
for n in cases:
    expected = canonical(n)
    actual = candidate(n)
    if expected != actual or type(expected) is not type(actual):
        mismatches.append((n, expected, actual, type(expected), type(actual)))

print("documented_examples=none")
print(f"fixed_intended={fixed_intended}")
print(f"generated_seed=410041 generated_intended_count={len(generated_intended)}")
print(f"observational_negative_count={len(observational_negative)}")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", mismatch)
    raise SystemExit(1)
