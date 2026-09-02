#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs scratch solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.eat


canonical_eat = load_entry("trusted_canonical_159", Path("/reference/canonical.py"))
generated_eat = load_entry(
    "scratch_generated_159", Path("/tmp/audit-work/159-eat/solution.py")
)

examples = [
    (5, 6, 10),
    (4, 8, 9),
    (1, 10, 10),
    (2, 11, 5),
]

# Includes all-zero, each coordinate boundary, and all eight 0/1000 corners.
boundary_values = (0, 1, 999, 1000)
boundaries = [
    (number, need, remaining)
    for number in boundary_values
    for need in boundary_values
    for remaining in boundary_values
]

# Exercise the exact branch edge need == remaining and its neighbors where valid.
branch_edges = []
for number in boundary_values:
    for remaining in range(0, 1001):
        for need in (remaining - 1, remaining, remaining + 1):
            if 0 <= need <= 1000:
                branch_edges.append((number, need, remaining))

# Exhaustive small cube covers every combination in [0, 20]^3.
small_exhaustive = [
    (number, need, remaining)
    for number in range(21)
    for need in range(21)
    for remaining in range(21)
]

generator = random.Random(159_20260729)
generated = [
    (
        generator.randint(0, 1000),
        generator.randint(0, 1000),
        generator.randint(0, 1000),
    )
    for _ in range(20_000)
]

cases = examples + boundaries + branch_edges + small_exhaustive + generated
serialized = json.dumps(cases, separators=(",", ":")).encode()
Path("/audit-output/evidence/differential-inputs.json").write_bytes(serialized)

mismatches = []
shape_failures = []
formula_failures = []
branch_counts = {"need<=remaining": 0, "need>remaining": 0}
for args in cases:
    expected = canonical_eat(*args)
    actual = generated_eat(*args)
    if args[1] <= args[2]:
        branch_counts["need<=remaining"] += 1
        formula = [args[0] + args[1], args[2] - args[1]]
    else:
        branch_counts["need>remaining"] += 1
        formula = [args[0] + args[2], 0]
    if actual != expected:
        mismatches.append((args, actual, expected))
    if type(actual) is not list or len(actual) != 2:
        shape_failures.append((args, type(actual).__name__, actual))
    if actual != formula or expected != formula:
        formula_failures.append((args, actual, expected, formula))

print("contract_domain=integer triples with each coordinate in [0,1000]")
print(f"examples={len(examples)}")
print(f"boundaries={len(boundaries)}")
print(f"branch_edges={len(branch_edges)}")
print(f"small_exhaustive={len(small_exhaustive)}")
print("random_seed=15920260729")
print(f"generated={len(generated)}")
print(f"total_cases={len(cases)}")
print(f"branch_counts={branch_counts}")
print(f"inputs_sha256={hashlib.sha256(serialized).hexdigest()}")
print(f"mismatches={len(mismatches)}")
print(f"shape_failures={len(shape_failures)}")
print(f"formula_failures={len(formula_failures)}")
if mismatches or shape_failures or formula_failures:
    print(f"first_mismatch={mismatches[:1]}")
    print(f"first_shape_failure={shape_failures[:1]}")
    print(f"first_formula_failure={formula_failures[:1]}")
    raise SystemExit(1)
