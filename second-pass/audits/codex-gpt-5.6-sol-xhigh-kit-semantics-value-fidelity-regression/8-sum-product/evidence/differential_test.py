#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/8."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/source/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], tuple[int, int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(CANDIDATE_PATH, "audited_candidate")

documented_and_boundaries = [
    [],
    [1, 2, 3, 4],
    [0],
    [1],
    [-1],
    [2],
    [-2],
    [0, 0],
    [0, 7],
    [7, 0],
    [-1, 1],
    [1, -1],
    [-3, -2],
    [-3, -2, -1],
    [2, 3, 5],
    [10**100],
    [-(10**100)],
    [10**100, -(10**100), 2],
]

# Exhaust all loop-length boundaries through length 5 over signs, zero, and
# small magnitudes. This is 1 + 7 + ... + 7**5 = 19,608 inputs.
exhaustive_small = [
    list(values)
    for length in range(6)
    for values in itertools.product(range(-3, 4), repeat=length)
]

# Add deterministic generated longer and large-magnitude integer inputs.
rng = random.Random(0x8_5A_9D)
generated = []
for _ in range(500):
    length = rng.randrange(0, 21)
    values = []
    for _ in range(length):
        selector = rng.randrange(4)
        if selector == 0:
            values.append(rng.randrange(-10, 11))
        elif selector == 1:
            values.append(rng.randrange(-(10**9), 10**9 + 1))
        elif selector == 2:
            values.append(rng.randrange(-(10**50), 10**50 + 1))
        else:
            values.append(rng.choice([-1, 0, 1]))
    generated.append(values)

cases = documented_and_boundaries + exhaustive_small + generated
mismatches: list[tuple[list[int], object, object]] = []

for numbers in cases:
    expected = canonical(list(numbers))
    actual = candidate(list(numbers))
    if type(actual) is not tuple or actual != expected:
        mismatches.append((numbers, expected, actual))

print(f"canonical={CANONICAL_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print("exhaustive_small_domain=lengths 0..5, elements -3..3")
print(f"exhaustive_small_cases={len(exhaustive_small)}")
print("generated_seed=0x85A9D")
print("generated_domain=500 lists, lengths 0..20, mixed small/1e9/1e50 integers")
print(f"generated_cases={len(generated)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")

for mismatch in mismatches[:20]:
    print(f"MISMATCH input={mismatch[0]!r} expected={mismatch[1]!r} actual={mismatch[2]!r}")

raise SystemExit(1 if mismatches else 0)
