#!/usr/bin/env python3
"""Independent differential test for HumanEval 145.

The complete input recipe is kept here: explicit boundary lists, an exhaustive
small alphabet, and a deterministic pseudo-random generator with the stated
seed. The trusted canonical module and scratch-copied candidate module are
loaded from distinct paths.
"""

import hashlib
import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_digit_sum(number: int) -> int:
    text = str(number)
    if text[0] == "-":
        return -int(text[1]) + sum(int(char) for char in text[2:])
    return sum(int(char) for char in text)


if len(sys.argv) != 3:
    raise SystemExit("usage: differential_test.py CANONICAL.py SOLUTION.py")

canonical_path = Path(sys.argv[1]).resolve()
candidate_path = Path(sys.argv[2]).resolve()
canonical = load_module("trusted_canonical_145", canonical_path)
candidate = load_module("candidate_solution_145", candidate_path)

documented_and_boundary_cases = [
    [1, 11, -1, -11, -12],
    [],
    [0],
    [-1],
    [1],
    [-10, -9, -1, 0, 1, 9, 10],
    [9, 10],
    [10, 9],
    [-9, -10],
    [-10, -9],
    [99, 100, 101, 109, 110],
    [-99, -100, -101, -109, -110],
    [1, 10, 100, 1000, 10000],
    [-1, -10, -100, -1000, -10000],
    [12, 21, 30, 3, 102, 120, 201, 210],
    [-12, -21, -30, -3, -102, -120, -201, -210],
    [10**100, -(10**100), 10**100 - 1, -(10**100 - 1)],
    [
        123456789012345678901234567890,
        -123456789012345678901234567890,
        987654321,
        -987654321,
    ],
]

alphabet = (-12, -11, -10, -1, 0, 1, 9, 10, 11, 12)
exhaustive_cases = [
    list(values)
    for length in range(5)
    for values in itertools.product(alphabet, repeat=length)
]

random_seed = 14520260729
rng = random.Random(random_seed)
generated_cases = []
for _ in range(2000):
    length = rng.randrange(0, 31)
    values = []
    for _ in range(length):
        selector = rng.randrange(4)
        if selector == 0:
            value = rng.randrange(-1000, 1001)
        elif selector == 1:
            value = rng.randrange(-(10**30), 10**30 + 1)
        elif selector == 2:
            bits = rng.randrange(0, 513)
            value = rng.getrandbits(bits)
            if rng.randrange(2):
                value = -value
        else:
            digits = rng.randrange(1, 151)
            value = 10**digits + rng.randrange(-1000, 1001)
            if rng.randrange(2):
                value = -value
        values.append(value)
    generated_cases.append(values)

all_cases = documented_and_boundary_cases + exhaustive_cases + generated_cases
digest = hashlib.sha256()
mismatches = []
for index, values in enumerate(all_cases):
    digest.update(repr(values).encode("utf-8"))
    expected = canonical.order_by_points(list(values))
    actual = candidate.order_by_points(list(values))
    independent_expected = sorted(values, key=independent_digit_sum)
    if expected != independent_expected or actual != expected:
        mismatches.append((index, values, expected, actual, independent_expected))
        if len(mismatches) >= 10:
            break

scalar_boundaries = [
    -10**100,
    -(10**100 - 1),
    -101,
    -100,
    -99,
    -11,
    -10,
    -9,
    -1,
    0,
    1,
    9,
    10,
    11,
    99,
    100,
    101,
    10**100 - 1,
    10**100,
]
for value in scalar_boundaries:
    expected_key = independent_digit_sum(value)
    actual_key = candidate.digit_sum(value)
    if actual_key != expected_key:
        mismatches.append(("digit_sum", value, expected_key, actual_key))

print(f"canonical={canonical_path}")
print(f"candidate={candidate_path}")
print(f"documented_boundary_cases={len(documented_and_boundary_cases)}")
print(
    "exhaustive_recipe="
    f"alphabet={alphabet}, lengths=0..4, cases={len(exhaustive_cases)}"
)
print(
    f"generated_recipe=seed={random_seed}, cases={len(generated_cases)}, "
    "lengths=0..30, integer magnitudes through 512 bits and 151 digits"
)
print(f"total_list_cases={len(all_cases)}")
print(f"input_stream_sha256={digest.hexdigest()}")
print(f"scalar_branch_boundary_cases={len(scalar_boundaries)}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
print("DIFFERENTIAL PASS")
