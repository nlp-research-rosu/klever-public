#!/usr/bin/env python3
"""Independent differential test for HumanEval/102 over positive integers."""

import importlib.util
import random
from pathlib import Path


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


canonical = load_entry("/reference/canonical.py", "trusted_canonical_102")
generated = load_entry("/tmp/audit-work/solution.py", "generated_solution_102")

# Prompt examples, smallest positive endpoint, singleton intervals, reversed
# intervals, and every implementation branch boundary.
documented_and_boundaries = [
    (12, 15),
    (13, 12),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 3),
    (2, 3),
    (3, 4),
    (4, 3),
    (4, 4),
    (5, 6),
    (6, 5),
    (999_999, 1_000_000),
    (1_000_000, 999_999),
]

inputs = list(documented_and_boundaries)
inputs.extend((x, y) for x in range(1, 201) for y in range(1, 201))
rng = random.Random(102)
inputs.extend(
    (rng.randint(1, 10**12), rng.randint(1, 10**12))
    for _ in range(5_000)
)

mismatches = []
branch_counts = {
    "even_y_in_range": 0,
    "even_y_before_range": 0,
    "odd_predecessor_in_range": 0,
    "odd_no_even_in_range": 0,
}
for x, y in inputs:
    expected = canonical(x, y)
    actual = generated(x, y)
    if y % 2 == 0 and y >= x:
        branch_counts["even_y_in_range"] += 1
    elif y % 2 == 0:
        branch_counts["even_y_before_range"] += 1
    elif y - 1 >= x:
        branch_counts["odd_predecessor_in_range"] += 1
    else:
        branch_counts["odd_no_even_in_range"] += 1
    if actual != expected:
        mismatches.append((x, y, expected, actual))

print("documented_and_boundary_inputs", documented_and_boundaries)
print("total_inputs", len(inputs))
print("branch_counts", branch_counts)
print("mismatch_count", len(mismatches))
if mismatches:
    print("first_mismatches", mismatches[:20])
    raise SystemExit(1)
