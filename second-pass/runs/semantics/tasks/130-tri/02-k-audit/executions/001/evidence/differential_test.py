#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval 130."""

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
    return module.tri


def typed_shape(value):
    if isinstance(value, list):
        return ("list", tuple(typed_shape(item) for item in value))
    return (type(value).__name__, value)


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry(
    "scratch_candidate", Path("/tmp/audit-work/reconstruction/solution.py")
)

documented = [0, 3]
branch_boundaries = [1, 2, 3, 4, 5, 6]
small_exhaustive = list(range(0, 65))
rng = random.Random(130)
generated = [rng.randrange(0, 501) for _ in range(200)]
inputs = sorted(set(documented + branch_boundaries + small_exhaustive + generated))

print("oracle=/reference/canonical.py:tri")
print("candidate=/tmp/audit-work/reconstruction/solution.py:tri")
print("formal/intended input domain sampled: non-negative integers")
print(f"documented_inputs={documented}")
print(f"branch_boundaries={branch_boundaries}")
print("small_exhaustive=range(0,65)")
print("generated=random.Random(130), 200 draws from range(0,501)")
print(f"complete_inputs={inputs}")

value_mismatches = []
typed_mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected:
        value_mismatches.append((n, expected, actual))
    if typed_shape(actual) != typed_shape(expected):
        typed_mismatches.append(
            (n, typed_shape(expected[:5]), typed_shape(actual[:5]))
        )

for n in [0, 1, 2, 3, 4, 10]:
    expected = canonical(n)
    actual = candidate(n)
    print(
        f"sample n={n}: canonical={expected!r}; candidate={actual!r}; "
        f"equal={actual == expected}"
    )

print(f"tested_input_count={len(inputs)}")
print(f"value_mismatch_count={len(value_mismatches)}")
print(f"value_mismatches={value_mismatches}")
print(f"strict_recursive_type_mismatch_count={len(typed_mismatches)}")
print(f"strict_type_mismatch_inputs={[item[0] for item in typed_mismatches]}")
if typed_mismatches:
    print(f"first_strict_type_mismatch={typed_mismatches[0]}")

raise SystemExit(1 if value_mismatches else 0)
