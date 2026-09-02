#!/usr/bin/env python3
"""Independent differential test for HumanEval 97-multiply."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


canonical = load_function("trusted_canonical_97", Path("/reference/canonical.py"))
candidate = load_function(
    "generated_candidate_97",
    Path("/tmp/audit-work/97-multiply/solution.py"),
)

documented_and_boundary = [
    (148, 412),
    (19, 28),
    (2020, 1851),
    (14, -15),
    (0, 0),
    (0, 7),
    (7, 0),
    (-1, 1),
    (1, -1),
    (-1, -1),
    (9, 9),
    (10, 10),
    (11, 11),
    (-9, 9),
    (-10, 10),
    (-11, 11),
    (9, -9),
    (10, -10),
    (11, -11),
    (10**100 + 9, -(10**100 + 1)),
    (-(10**100 + 9), 10**100 + 1),
]

# This contract has no valid "empty integer"; zero is its neutral boundary.
# The implementation has no explicit branch. Values immediately around positive
# and negative multiples of ten cover Python remainder discontinuities.
exhaustive = [(a, b) for a in range(-125, 126) for b in range(-125, 126)]

rng = random.Random(970097)
generated = []
for _ in range(20_000):
    bits_a = rng.randrange(0, 1025)
    bits_b = rng.randrange(0, 1025)
    a = rng.getrandbits(bits_a)
    b = rng.getrandbits(bits_b)
    if rng.randrange(2):
        a = -a
    if rng.randrange(2):
        b = -b
    generated.append((a, b))

cases = documented_and_boundary + exhaustive + generated
mismatches = []
for a, b in cases:
    expected = canonical(a, b)
    actual = candidate(a, b)
    if actual != expected:
        mismatches.append((a, b, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"documented_and_boundary_cases={len(documented_and_boundary)}")
print(f"exhaustive_grid=-125..125 x -125..125 ({len(exhaustive)} cases)")
print("generated_seed=970097")
print(f"generated_arbitrary_precision_cases={len(generated)}")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", mismatch)

raise SystemExit(1 if mismatches else 0)
