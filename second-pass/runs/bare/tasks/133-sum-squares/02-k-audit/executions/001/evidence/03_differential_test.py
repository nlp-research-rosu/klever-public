#!/usr/bin/env python3
"""Independent candidate-vs-trusted differential test for HumanEval 133."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from itertools import product
from pathlib import Path
import random
from typing import Callable


SCRATCH = Path("/tmp/audit-work/133-sum-squares")


def load_entry(path: Path, module_name: str) -> Callable[[list[object]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_entry(SCRATCH / "trusted/canonical.py", "trusted_canonical")
candidate = load_entry(SCRATCH / "solution.py", "candidate_solution")

documented = [
    ([1, 2, 3], 14),
    ([1, 4, 9], 98),
    ([1, 3, 5, 7], 84),
    ([1.4, 4.2, 0], 29),
    ([-2.4, 1, 1], 6),
]

boundary = [
    [],
    [0],
    [1],
    [-1],
    [1.0],
    [0.999999999999],
    [1.000000000001],
    [-0.999999999999],
    [-1.000000000001],
    [Fraction(1, 10)],
    [Fraction(-1, 10)],
    [Fraction(10, 10)],
    [Fraction(-10, 10)],
    [True, False],
    [10**50, -(10**50)],
]

# Exhaust all sequences through length three over values chosen on, immediately
# below, and immediately above positive, zero, and negative integer boundaries.
pool = [
    -3.2,
    -3,
    -2.5,
    -2,
    -1.1,
    -1,
    -0.1,
    0,
    0.1,
    0.9,
    1,
    1.1,
    2.5,
    3,
]
exhaustive = [
    list(values)
    for length in range(4)
    for values in product(pool, repeat=length)
]

rng = random.Random(133)
generated = []
for _ in range(500):
    length = rng.randrange(0, 21)
    generated.append(
        [
            (
                rng.randrange(-1000, 1001)
                if rng.randrange(3) == 0
                else Fraction(rng.randrange(-1000, 1001), rng.randrange(1, 31))
            )
            for _ in range(length)
        ]
    )

tested = 0
mismatches: list[tuple[str, list[object], object, object]] = []


def compare(label: str, values: list[object]) -> None:
    global tested
    expected = canonical(values)
    actual = candidate(values)
    tested += 1
    if expected != actual:
        mismatches.append((label, values, expected, actual))


print("DOCUMENTED_EXAMPLES")
for values, stated in documented:
    oracle = canonical(values)
    actual = candidate(values)
    print(
        f"input={values!r} stated={stated!r} "
        f"canonical={oracle!r} candidate={actual!r}"
    )
    if oracle != stated or actual != stated:
        mismatches.append(("documented", values, oracle, actual))
    tested += 1

print("BOUNDARY_CASES")
for values in boundary:
    oracle = canonical(values)
    actual = candidate(values)
    print(f"input={values!r} canonical={oracle!r} candidate={actual!r}")
    if oracle != actual:
        mismatches.append(("boundary", values, oracle, actual))
    tested += 1

for values in exhaustive:
    compare("exhaustive", values)
for values in generated:
    compare("generated", values)

print(
    "SUMMARY "
    f"documented={len(documented)} boundary={len(boundary)} "
    f"exhaustive={len(exhaustive)} generated={len(generated)} "
    f"total={tested} mismatches={len(mismatches)}"
)
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
