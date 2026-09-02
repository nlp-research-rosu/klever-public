#!/usr/bin/env python3
"""Independent Python differential test for HumanEval 55."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib


canonical_fib = load_entry("trusted_humaneval_55", Path("/reference/canonical.py"))
candidate_fib = load_entry("submitted_humaneval_55", Path("/candidate/solution.py"))

documented = [10, 1, 8]
boundaries = [0, 1, 2, 3]
rng = random.Random(550055)
generated = [rng.randint(0, 25) for _ in range(64)]
inputs = list(dict.fromkeys(documented + boundaries + generated))

print(f"DOCUMENTED={documented}")
print(f"BOUNDARIES={boundaries}")
print("EMPTY_CASE=not_applicable_scalar_integer_input; n=0 is the zero-iteration case")
print("GENERATED_SEED=550055")
print(f"GENERATED={generated}")
print(f"UNIQUE_TEST_INPUTS={inputs}")

mismatches = []
for n in inputs:
    expected = canonical_fib(n)
    actual = candidate_fib(n)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"n={n} canonical={expected} candidate={actual} {status}")
    if actual != expected:
        mismatches.append((n, expected, actual))

try:
    outside_canonical = canonical_fib(-1)
except BaseException as err:  # Record the behavior outside the audited n >= 0 domain.
    outside_canonical = type(err).__name__
outside_candidate = candidate_fib(-1)
print(
    "OUTSIDE_DOMAIN n=-1 "
    f"canonical={outside_canonical} candidate={outside_candidate}"
)

print(f"MISMATCH_COUNT={len(mismatches)}")
raise SystemExit(1 if mismatches else 0)
