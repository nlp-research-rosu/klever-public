#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/8."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module("generated_solution", Path("/candidate/solution.py"))

# The fixed cases cover both documented examples; the zero-iteration/one-iteration/
# multi-iteration loop boundaries; sign and zero behavior; cancellation; repeated
# values; and Python's unbounded integer arithmetic.
fixed_cases = [
    [],
    [1, 2, 3, 4],
    [0],
    [1],
    [-1],
    [2],
    [0, 7],
    [7, 0],
    [-2, 3],
    [-2, -3],
    [-5, 0, 7],
    [1, -1, 1, -1],
    [10**100],
    [10**100, -(10**90), 3],
    [-(10**200), 0, 10**200],
    [2] * 128,
    list(range(-25, 26)),
]

# Exhaust all lists through length five over a sign/zero-sensitive small domain.
exhaustive_cases = [
    list(values)
    for length in range(0, 6)
    for values in itertools.product(range(-3, 4), repeat=length)
]

# Add a documented deterministic representative sample of longer lists and much
# larger magnitudes. The seed and generation bounds are part of the preserved input.
rng = random.Random(0x8A11D17)
random_cases = []
for _ in range(512):
    length = rng.randrange(0, 65)
    values = []
    for _ in range(length):
        if rng.randrange(8) == 0:
            magnitude = rng.randrange(0, 10**6)
            exponent = rng.randrange(0, 30)
            value = magnitude * (10**exponent)
            if rng.randrange(2):
                value = -value
        else:
            value = rng.randrange(-10**6, 10**6 + 1)
        values.append(value)
    random_cases.append(values)

cases = fixed_cases + exhaustive_cases + random_cases
encoded_cases = json.dumps(cases, separators=(",", ":")).encode()
print("entry_point=sum_product")
print("intended_domain=arbitrary finite lists of Python integers")
print("random_seed=0x8A11D17")
print("random_length_range=0..64")
print("random_value_policy=mixed [-1000000,1000000] and scaled big integers")
print(f"fixed_cases={len(fixed_cases)}")
print(f"exhaustive_cases={len(exhaustive_cases)} domain=-3..3 lengths=0..5")
print(f"random_cases={len(random_cases)}")
print(f"total_cases={len(cases)}")
print(f"cases_sha256={hashlib.sha256(encoded_cases).hexdigest()}")

mismatches = []
for index, values in enumerate(cases):
    expected = canonical.sum_product(list(values))
    actual = candidate.sum_product(list(values))
    if actual != expected:
        mismatches.append(
            {"index": index, "input": values, "canonical": expected, "candidate": actual}
        )
        if len(mismatches) >= 20:
            break

for index, values in enumerate(fixed_cases):
    print(
        f"fixed[{index}]={values!r} canonical={canonical.sum_product(list(values))!r} "
        f"candidate={candidate.sum_product(list(values))!r}"
    )
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
