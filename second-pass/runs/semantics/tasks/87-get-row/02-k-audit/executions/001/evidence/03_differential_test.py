#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


canonical = load_entry("trusted_canonical_87", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated_87", Path("/tmp/audit-work/87-get-row/solution.py")
)

documented_and_boundaries = [
    (
        [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 1, 6],
            [1, 2, 3, 4, 5, 1],
        ],
        1,
        "documented_multirow",
    ),
    ([], 1, "documented_empty_outer"),
    ([[], [1], [1, 2, 3]], 3, "documented_ragged"),
    ([[]], 0, "single_empty_row"),
    ([[], [], []], -1, "several_empty_rows"),
    ([[0]], 1, "single_element_no_match"),
    ([[0]], 0, "single_element_match"),
    ([[9, 8, 7]], 9, "first_column_match"),
    ([[9, 8, 7]], 8, "middle_column_match"),
    ([[9, 8, 7]], 7, "last_column_match"),
    ([[4, 4, 4]], 4, "all_columns_match_descending"),
    ([[2, 3], [], [3], [3, 2, 3]], 3, "ragged_and_empty_rows"),
    ([[-2, -1, -2], [0, -2]], -2, "negative_target_and_values"),
    ([[10**30, -(10**30)]], 10**30, "unbounded_integer_boundary"),
]

count = 0
for matrix, target, label in documented_and_boundaries:
    expected = canonical(matrix, target)
    actual = generated(matrix, target)
    if actual != expected:
        raise AssertionError(
            f"{label}: matrix={matrix!r} target={target!r} "
            f"canonical={expected!r} generated={actual!r}"
        )
    count += 1

# Exhaust the small ragged domain: zero to three rows; each row has zero, one,
# or two elements from {-1, 0, 1}; target includes present and absent values.
value_domain = (-1, 0, 1)
row_pool: list[list[int]] = []
for row_len in range(3):
    row_pool.extend([list(row) for row in itertools.product(value_domain, repeat=row_len)])

exhaustive_count = 0
for outer_len in range(4):
    for matrix_rows in itertools.product(row_pool, repeat=outer_len):
        matrix = [list(row) for row in matrix_rows]
        for target in (-2, -1, 0, 1, 2):
            expected = canonical(matrix, target)
            actual = generated(matrix, target)
            if actual != expected:
                raise AssertionError(
                    "exhaustive mismatch: "
                    f"matrix={matrix!r} target={target!r} "
                    f"canonical={expected!r} generated={actual!r}"
                )
            exhaustive_count += 1
            count += 1

# Deterministic representative larger ragged inputs.
rng = random.Random(870087)
random_count = 2000
for case_index in range(random_count):
    matrix = [
        [rng.randint(-5, 5) for _ in range(rng.randint(0, 8))]
        for _ in range(rng.randint(0, 6))
    ]
    target = rng.randint(-6, 6)
    expected = canonical(matrix, target)
    actual = generated(matrix, target)
    if actual != expected:
        raise AssertionError(
            f"random case {case_index}: matrix={matrix!r} target={target!r} "
            f"canonical={expected!r} generated={actual!r}"
        )
    count += 1

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print(f"exhaustive_small_ragged_cases={exhaustive_count}")
print(f"deterministic_random_cases={random_count}")
print(f"total_cases={count}")
print("mismatches=0")
