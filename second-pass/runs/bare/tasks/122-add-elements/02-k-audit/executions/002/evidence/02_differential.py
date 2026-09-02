#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs scratch candidate."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/122-add-elements")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", SCRATCH / "canonical.py")
candidate = load("scratch_candidate", SCRATCH / "solution.py")

fixed_cases = [
    ("documented-example", [111, 21, 3, 4000, 5, 6, 7, 8, 9], 4, True),
    ("empty-outside-contract", [], 0, False),
    ("single-zero", [0], 1, True),
    ("single-minus-one", [-1], 1, True),
    ("single-minus-nine", [-9], 1, True),
    ("single-minus-ten", [-10], 1, True),
    ("single-minus-ninety-nine", [-99], 1, True),
    ("single-minus-one-hundred", [-100], 1, True),
    ("single-nine", [9], 1, True),
    ("single-ten", [10], 1, True),
    ("single-ninety-nine", [99], 1, True),
    ("single-one-hundred", [100], 1, True),
    (
        "all-branch-boundaries",
        [-101, -100, -99, -10, -9, -1, 0, 9, 10, 99, 100, 101],
        12,
        True,
    ),
    ("prefix-boundary-k-one", [-99, 99, 100], 1, True),
    ("prefix-boundary-k-len", [-99, 99, 100], 3, True),
    ("length-100", list(range(-50, 50)), 100, True),
]

rng = random.Random(122)
random_cases = []
pool = [
    -1000,
    -101,
    -100,
    -99,
    -50,
    -10,
    -9,
    -1,
    0,
    1,
    9,
    10,
    50,
    99,
    100,
    101,
    1000,
]
for index in range(500):
    length = rng.randint(1, 100)
    arr = [rng.choice(pool) if rng.random() < 0.7 else rng.randint(-10000, 10000)
           for _ in range(length)]
    k = rng.randint(1, length)
    random_cases.append((f"generated-{index:03d}", arr, k, True))

all_cases = fixed_cases + random_cases
mismatches = []
in_domain = 0
for name, arr, k, is_in_domain in all_cases:
    expected = canonical.add_elements(arr, k)
    actual = candidate.add_elements(arr, k)
    if is_in_domain:
        in_domain += 1
    if name.startswith("generated"):
        if expected != actual:
            mismatches.append((name, arr, k, expected, actual, is_in_domain))
    else:
        print(
            f"fixed {name}: arr={arr!r} k={k} "
            f"canonical={expected} candidate={actual} in_domain={is_in_domain} "
            f"match={expected == actual}"
        )
        if expected != actual:
            mismatches.append((name, arr, k, expected, actual, is_in_domain))

generated_mismatches = [m for m in mismatches if m[0].startswith("generated")]
print(f"cases_total={len(all_cases)}")
print(f"cases_in_domain={in_domain}")
print(f"mismatches_total={len(mismatches)}")
print(f"generated_mismatches={len(generated_mismatches)}")
for name, arr, k, expected, actual, is_in_domain in mismatches[:20]:
    print(
        f"mismatch {name}: arr={arr!r} k={k} canonical={expected} "
        f"candidate={actual} in_domain={is_in_domain}"
    )

raise SystemExit(1 if mismatches else 0)
