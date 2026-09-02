#!/usr/bin/env python3
"""Independent canonical-versus-submitted differential test.

The oracle and generated implementation are imported from distinct, explicit
paths.  Inputs cover the prompt examples; the empty-loop boundary; sign, parity,
and decimal-boundary cases; every integer in [-5000, 5000]; and a deterministic
sample of 1,000 integers with up to 30 decimal digits.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
generated = load_module(
    "submitted_solution",
    Path("/tmp/audit-work/rebuild/candidate-src/solution.py"),
)

documented_and_boundaries = [
    -12,
    123,
    0,
    -1,
    1,
    -2,
    2,
    -9,
    9,
    -10,
    10,
    -11,
    11,
    -19,
    19,
    -20,
    20,
    -99,
    99,
    -100,
    100,
    -101,
    101,
    -808,
    808,
    -999,
    999,
    -(10**30),
    10**30,
]

rng = random.Random(155)
generated_inputs = [rng.randint(-(10**30), 10**30) for _ in range(1000)]
inputs = sorted(set(documented_and_boundaries + list(range(-5000, 5001)) + generated_inputs))

mismatches = []
for value in inputs:
    oracle_result = canonical.even_odd_count(value)
    generated_result = generated.even_odd_count(value)
    if oracle_result != generated_result:
        mismatches.append((value, oracle_result, generated_result))

print("oracle=/reference/canonical.py:even_odd_count")
print("generated=/tmp/audit-work/rebuild/candidate-src/solution.py:even_odd_count")
print(f"documented_and_boundary_count={len(documented_and_boundaries)}")
print("exhaustive_interval=[-5000,5000]")
print("random_seed=155")
print("random_count=1000")
print("random_range=[-10**30,10**30]")
print(f"unique_input_count={len(inputs)}")
print(f"mismatch_count={len(mismatches)}")
for value, oracle_result, generated_result in mismatches[:20]:
    print(
        f"mismatch input={value} canonical={oracle_result!r} "
        f"generated={generated_result!r}"
    )

sys.exit(1 if mismatches else 0)
