#!/usr/bin/env python3
"""Independent, deterministic differential test for HumanEval/136."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_smallest_integers


canonical = load_entry("trusted_canonical_136", SCRATCH / "canonical.py")
generated = load_entry("candidate_solution_136", SCRATCH / "solution.py")

documented_and_boundary = [
    [2, 4, 1, 3, 5, 7],
    [],
    [0],
    [-1],
    [1],
    [-5, -2, -9],
    [-1, 8, -3, 2, 0],
    [0, 0, 0],
    [-1, 0, 1],
    [1, 0, -1],
    [-2, -1],
    [2, 1],
    [-1, -1, -1],
    [1, 1, 1],
    [-(10**100), -2, -3, 10**100, 2, 3],
    [-(10**100), 0, 10**100],
    [True, False, -1, 2],
]

alphabet = [-5, -1, 0, 1, 5]
exhaustive = [
    list(values)
    for length in range(0, 7)
    for values in itertools.product(alphabet, repeat=length)
]

rng = random.Random(136_20260726)
random_cases = []
for _ in range(2_000):
    length = rng.randrange(0, 51)
    values = []
    for _ in range(length):
        selector = rng.randrange(0, 8)
        if selector == 0:
            values.append(0)
        elif selector == 1:
            values.append(1)
        elif selector == 2:
            values.append(-1)
        else:
            values.append(rng.randint(-(10**30), 10**30))
    random_cases.append(values)

cases = documented_and_boundary + exhaustive + random_cases
encoded = json.dumps(cases, separators=(",", ":"), sort_keys=False).encode()
print("oracle=/tmp/audit-work/reconstruction/canonical.py:largest_smallest_integers")
print("candidate=/tmp/audit-work/reconstruction/solution.py:largest_smallest_integers")
print(f"explicit_cases={len(documented_and_boundary)}")
print(f"exhaustive_domain=alphabet{alphabet}, lengths=0..6, cases={len(exhaustive)}")
print("random_seed=13620260726")
print(f"random_cases={len(random_cases)}, random_lengths=0..50")
print(f"all_input_cases_sha256={hashlib.sha256(encoded).hexdigest()}")

mismatches = []
for index, values in enumerate(cases):
    try:
        expected = canonical(values.copy())
    except Exception as error:
        expected = ("EXCEPTION", type(error).__name__, str(error))
    try:
        actual = generated(values.copy())
    except Exception as error:
        actual = ("EXCEPTION", type(error).__name__, str(error))
    if actual != expected:
        mismatches.append((index, values, expected, actual))
        if len(mismatches) <= 10:
            print(f"MISMATCH index={index} input={values!r} canonical={expected!r} candidate={actual!r}")

print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
raise SystemExit(1 if mismatches else 0)
