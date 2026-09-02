#!/usr/bin/env python3
"""Independent differential test for HumanEval 107."""

from __future__ import annotations

import ast
import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_palindrome


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)

source = Path("/tmp/audit-work/reconstruction/solution.py").read_text(
    encoding="utf-8"
)
tree = ast.parse(source)
thresholds: set[int] = set()
for node in ast.walk(tree):
    if (
        isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and isinstance(node.ops[0], ast.Lt)
        and isinstance(node.left, ast.Name)
        and node.left.id == "n"
        and len(node.comparators) == 1
        and isinstance(node.comparators[0], ast.Constant)
        and isinstance(node.comparators[0].value, int)
    ):
        thresholds.add(node.comparators[0].value)

examples = {3: (1, 2), 12: (4, 6)}
for n, expected in examples.items():
    assert canonical(n) == expected
    assert generated(n) == expected

boundary_values = {1, 1000}
for threshold in thresholds:
    for n in (threshold - 1, threshold):
        if 1 <= n <= 1000:
            boundary_values.add(n)

rng = random.Random(107)
generated_sample = sorted(rng.sample(range(1, 1001), 250))
intended_inputs = list(range(1, 1001))
mismatches = [
    (n, generated(n), canonical(n))
    for n in intended_inputs
    if generated(n) != canonical(n)
]

# There is no empty collection input: the contract accepts one positive scalar
# integer. Record adjacent excluded values without treating them as obligations.
excluded_observations = {
    n: {"generated": generated(n), "canonical": canonical(n)}
    for n in (0, 1001)
}

print(f"documented_examples={sorted(examples)}")
print("empty_case=not_applicable_to_positive_scalar_integer_contract")
print(f"threshold_count={len(thresholds)}")
print(f"threshold_min={min(thresholds)} threshold_max={max(thresholds)}")
print(f"branch_boundary_inputs={len(boundary_values)}")
print(f"representative_generated_inputs={len(generated_sample)} seed=107")
print(f"exhaustive_intended_inputs={len(intended_inputs)} domain=1..1000")
print(f"mismatches={len(mismatches)}")
print(f"excluded_adjacent_observations={excluded_observations}")
if mismatches:
    print(f"first_mismatches={mismatches[:20]}")
raise SystemExit(1 if mismatches else 0)
