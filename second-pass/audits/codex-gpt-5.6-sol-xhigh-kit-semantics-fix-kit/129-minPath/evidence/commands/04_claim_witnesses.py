#!/usr/bin/env python3
"""Concrete satisfying witnesses for every submitted claim family."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


canonical = load(Path("/reference/canonical.py"), "claim_witness_canonical")
generated = load(Path("/tmp/audit-work/129-minpath/solution.py"), "claim_witness_generated")


def neighbor2(a: int, b: int, c: int, d: int) -> int:
    if a == 1:
        return min(b, c)
    if b == 1:
        return min(a, d)
    if c == 1:
        return min(a, d)
    return min(b, c)


def suffix(i: int, k: int, neighbor: int) -> list[int]:
    return [1 if index % 2 == 0 else neighbor for index in range(i, k)]


def actual_neighbor(grid: list[list[int]]) -> int:
    n = len(grid)
    row, col = next(
        (row, col)
        for row in range(n)
        for col in range(n)
        if grid[row][col] == 1
    )
    values = []
    for drow, dcol in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        next_row, next_col = row + drow, col + dcol
        if 0 <= next_row < n and 0 <= next_col < n:
            values.append(grid[next_row][next_col])
    return min(values)


# Auxiliary answer-loop witness: I=2,K=5,M=4,prefix=[8,9].
prefix = [8, 9]
loop_actual = prefix[:]
for index in range(2, 5):
    loop_actual.append(1 if index % 2 == 0 else 4)
loop_claimed = prefix + suffix(2, 5, 4)
assert loop_actual == loop_claimed == [8, 9, 1, 4, 1]

whole_witnesses = [
    ("all-valid-2x2-A1", [[1, 2], [3, 4]], 3),
    ("all-valid-2x2-D1", [[4, 3], [2, 1]], 3),
    ("example-one", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3),
    ("example-two", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1),
]

rows = []
for label, grid, k in whole_witnesses:
    expected = suffix(0, k, actual_neighbor(grid))
    canonical_result = canonical(grid, k)
    generated_result = generated(grid, k)
    assert canonical_result == generated_result == expected
    rows.append(
        {
            "claim": label,
            "grid": grid,
            "k": k,
            "claimed_result": expected,
            "canonical": canonical_result,
            "generated": generated_result,
        }
    )

neighbor_equation_mismatches = []
for permutation in itertools.permutations(range(1, 5)):
    a, b, c, d = permutation
    grid = [[a, b], [c, d]]
    if neighbor2(a, b, c, d) != actual_neighbor(grid):
        neighbor_equation_mismatches.append(grid)

assert not neighbor_equation_mismatches
print("answer_loop_witness=" + json.dumps({"I": 2, "K": 5, "M": 4, "prefix": prefix, "result": loop_actual}))
print("entry_witnesses=" + json.dumps(rows, sort_keys=True))
print("neighbor2_valid_domain_cases=24")
print("neighbor2_valid_domain_mismatches=0")
