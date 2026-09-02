#!/usr/bin/env python3
"""Independent canonical/generated/oracle differential for HumanEval 114."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


def load_function(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical_114")
generated = load_function(
    Path("/tmp/audit-work/114-minSubArraySum/solution.py"),
    "candidate_generated_114",
)


def oracle(nums: list[int]) -> int:
    if not nums:
        raise ValueError("the source contract admits no non-empty sub-array")
    return min(
        sum(nums[start:end])
        for start in range(len(nums))
        for end in range(start + 1, len(nums) + 1)
    )


documented_and_boundaries = [
    ("prompt-positive", [2, 3, 4, 1, 2, 4]),
    ("prompt-negative", [-1, -2, -3]),
    ("singleton-positive", [5]),
    ("singleton-negative", [-5]),
    ("singleton-zero", [0]),
    ("two-positive", [1, 2]),
    ("two-negative", [-1, -2]),
    ("zero-boundary", [0, 0]),
    ("restart-boundary", [3, -4, 2, -3, -1, 7, -5]),
    ("tie-boundary", [2, -2, 2, -2]),
    ("canonical-reset", [4, -1, 2]),
    ("canonical-nonzero-max", [-4, 1, -2]),
    ("large-positive", [10**80, 10**81]),
    ("large-negative", [-(10**80), 10**79, -(10**81)]),
]

checked = 0
for label, values in documented_and_boundaries:
    c = canonical(values.copy())
    g = generated(values.copy())
    o = oracle(values.copy())
    print(f"CASE {label}: canonical={c} generated={g} oracle={o}")
    if not (c == g == o):
        raise AssertionError((label, values, c, g, o))
    checked += 1

empty_observations = []
for name, function in (("canonical", canonical), ("generated", generated), ("oracle", oracle)):
    try:
        value = function([])
    except Exception as error:  # record the out-of-domain boundary precisely
        empty_observations.append((name, type(error).__name__, str(error)))
    else:
        empty_observations.append((name, "RETURN", repr(value)))
print("EMPTY_OUT_OF_DOMAIN:", empty_observations)

# Complete small domain: all non-empty lists of lengths 1..5 over -3..3.
for length in range(1, 6):
    for values_tuple in itertools.product(range(-3, 4), repeat=length):
        values = list(values_tuple)
        c = canonical(values.copy())
        g = generated(values.copy())
        o = oracle(values)
        if not (c == g == o):
            raise AssertionError(("exhaustive", values, c, g, o))
        checked += 1

# Deterministic broader representatives with longer lists and larger magnitudes.
rng = random.Random(114)
for _ in range(1000):
    length = rng.randint(1, 30)
    values = [rng.randint(-1000, 1000) for _ in range(length)]
    c = canonical(values.copy())
    g = generated(values.copy())
    o = oracle(values)
    if not (c == g == o):
        raise AssertionError(("random", values, c, g, o))
    checked += 1

print(f"SUMMARY intended_domain_cases={checked} mismatches=0")
