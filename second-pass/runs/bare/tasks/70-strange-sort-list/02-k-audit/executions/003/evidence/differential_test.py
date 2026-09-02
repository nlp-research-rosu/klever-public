#!/usr/bin/env python3
"""Independent deterministic differential test of candidate vs trusted canonical."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strange_sort_list


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(Path("/candidate/solution.py"), "generated_solution")

cases: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 5, 5, 5],
    [],
    [0],
    [-1],
    [2, 1],
    [1, 2],
    [2, 2],
    [3, 2, 1],
    [-2, 0, 2],
    [3, -1, 2, 3, 0],
    [4, 1, 7, 2, 6],
    [9, -9, 4, 4, 0, 2],
    list(range(12)),
    list(range(11, -1, -1)),
]

# Exhaust every list of lengths 0..7 over a small integer alphabet. This crosses
# every candidate recursive boundary and goes beyond the proof's length-4 families.
alphabet = (-2, -1, 0, 1, 2)
for length in range(8):
    cases.extend(list(values) for values in itertools.product(alphabet, repeat=length))

# Broader representative integer lists with a fixed seed.
rng = random.Random(70070)
for _ in range(500):
    length = rng.randrange(0, 31)
    cases.append([rng.randrange(-10**6, 10**6 + 1) for _ in range(length)])

mismatches: list[tuple[list[int], object, object]] = []
mutation_mismatches = 0
for original in cases:
    left_input = list(original)
    right_input = list(original)
    left = canonical(left_input)
    right = candidate(right_input)
    if left != right:
        mismatches.append((original, left, right))
    # Canonical consumes its local list argument; the return value is the contract.
    if right_input != original:
        mutation_mismatches += 1

print(f"cases={len(cases)}")
print(f"min_length={min(map(len, cases))} max_length={max(map(len, cases))}")
print(f"result_mismatches={len(mismatches)}")
print(f"candidate_input_mutations={mutation_mismatches}")
for mismatch in mismatches[:10]:
    print(f"MISMATCH {mismatch!r}")
assert not mismatches
assert mutation_mismatches == 0
print("DIFFERENTIAL PASS")
