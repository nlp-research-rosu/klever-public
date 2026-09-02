#!/usr/bin/env python3
"""Differentially compare the trusted canonical and submitted implementation."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/rebuild")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


canonical = load_function("trusted_canonical", ROOT / "canonical.py")
generated = load_function("generated_solution", ROOT / "solution.py")

documented = [1, 5, 8]
boundaries = [0, 1, 2, 3, 4]
representative = [6, 7, 9, 10, 12, 15, 18, 20]
rng = random.Random(63063)
generated_inputs = [rng.randrange(0, 26) for _ in range(24)]
all_inputs = sorted(
    set(documented + boundaries + representative + generated_inputs + list(range(26)))
)

print(f"documented={documented}")
print(f"boundaries={boundaries}")
print("empty_case=N/A (the contract input is an integer, not a collection)")
print(f"representative={representative}")
print(f"seed=63063 generated_inputs={generated_inputs}")
print("bounded_exhaustive_domain=0..25")
print(f"tested_inputs={all_inputs}")

mismatches = []
for n in all_inputs:
    expected = canonical(n)
    actual = generated(n)
    print(f"n={n} canonical={expected} generated={actual} equal={expected == actual}")
    if expected != actual:
        mismatches.append((n, expected, actual))

try:
    canonical_negative = canonical(-1)
except BaseException as error:  # Record the canonical's non-normal behavior.
    canonical_negative = f"{type(error).__name__}: {error}"
try:
    generated_negative = generated(-1)
except BaseException as error:
    generated_negative = f"{type(error).__name__}: {error}"
print(
    "out_of_domain_probe_n=-1 "
    f"canonical={canonical_negative!r} generated={generated_negative!r}"
)
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(f"mismatches={mismatches}")
    sys.exit(1)
