#!/usr/bin/env python3
"""Differential test: trusted HumanEval implementation versus candidate."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_function(
    "scratch_candidate", Path("/tmp/audit-work/string-sequence/solution.py")
)

# Examples; the negative/zero/one branch boundaries; decimal-width boundaries;
# and representative larger empty/nonempty ranges.
fixed_inputs = [
    -1000,
    -100,
    -10,
    -2,
    -1,
    0,
    1,
    2,
    5,
    9,
    10,
    11,
    99,
    100,
    101,
    999,
    1000,
]
rng = random.Random(15015)
generated_inputs = [rng.randint(-200, 1000) for _ in range(250)]
inputs = fixed_inputs + generated_inputs

mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected or type(actual) is not str:
        mismatches.append((n, expected, actual, type(actual).__name__))

assert canonical(0) == "0"
assert canonical(5) == "0 1 2 3 4 5"
assert candidate(0) == "0"
assert candidate(5) == "0 1 2 3 4 5"
assert canonical(-1) == candidate(-1) == ""
assert not mismatches, mismatches[:10]

print(f"fixed_inputs={fixed_inputs}")
print("generated_seed=15015 generated_range=[-200,1000] generated_count=250")
print(f"comparisons={len(inputs)} mismatches={len(mismatches)}")
print("examples_and_branch_boundaries=pass")
