#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval/60."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_to_n


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)

documented = [30, 100, 5, 10, 1]
boundaries = [-1000, -100, -3, -2, -1, 0, 1, 2, 3, 1000]
exhaustive_small = list(range(-50, 201))
rng = random.Random(600060)
representative_generated = [rng.randint(-1000, 5000) for _ in range(200)]
inputs = list(dict.fromkeys(documented + boundaries + exhaustive_small + representative_generated))

mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = generated(n)
    if actual != expected:
        mismatches.append({"n": n, "canonical": expected, "generated": actual})

print("oracle=/reference/canonical.py:sum_to_n")
print("candidate=/tmp/audit-work/reconstruction/solution.py:sum_to_n")
print("documented_examples=" + json.dumps(documented))
print("boundary_inputs=" + json.dumps(boundaries))
print("exhaustive_small=range(-50,201)")
print("generated_seed=600060 generated_count=200 generated_range=[-1000,5000]")
print("complete_inputs=" + json.dumps(inputs))
print(f"tested={len(inputs)} mismatches={len(mismatches)}")
print("mismatch_records=" + json.dumps(mismatches, sort_keys=True))
sys.exit(0 if not mismatches else 1)
