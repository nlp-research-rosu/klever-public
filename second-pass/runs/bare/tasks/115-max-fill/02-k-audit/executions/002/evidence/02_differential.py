#!/usr/bin/env python3
"""Differentially compare trusted HumanEval/115 with the candidate Python."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import random


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


canonical = load_entry(
    Path("/tmp/audit-work/reconstruction/reference/canonical.py"),
    "audit_canonical",
)
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"),
    "audit_candidate",
)

mismatches: list[tuple[list[list[int]], int, object, object]] = []
case_count = 0


def check(grid: list[list[int]], capacity: int) -> None:
    global case_count
    case_count += 1
    expected = canonical(grid, capacity)
    actual = candidate(grid, capacity)
    if actual != expected:
        mismatches.append((grid, capacity, expected, actual))


named_cases = [
    ("example-1", [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1),
    (
        "example-2",
        [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]],
        2,
    ),
    ("example-3", [[0, 0, 0], [0, 0, 0]], 5),
    ("empty-grid-outside-contract", [], 1),
    ("empty-row-outside-contract", [[]], 1),
    ("minimum-zero", [[0]], 1),
    ("minimum-one", [[1]], 1),
    ("maximum-capacity", [[1]], 10),
    ("ceil-below-boundary", [[1, 1]], 3),
    ("ceil-at-boundary", [[1, 1, 1]], 3),
    ("ceil-above-boundary", [[1, 1, 1, 1]], 3),
    ("per-row-not-global-ceil", [[1], [1]], 2),
    ("maximum-all-zero", [[0] * 100 for _ in range(100)], 10),
    ("maximum-all-one-capacity-1", [[1] * 100 for _ in range(100)], 1),
    ("maximum-all-one-capacity-10", [[1] * 100 for _ in range(100)], 10),
]

print("NAMED CASES")
for name, grid, capacity in named_cases:
    expected = canonical(grid, capacity)
    actual = candidate(grid, capacity)
    print(
        f"{name}: rows={len(grid)} cols={len(grid[0]) if grid else 0} "
        f"capacity={capacity} canonical={expected} candidate={actual}"
    )
    check(grid, capacity)

exhaustive_count = 0
for rows in range(1, 4):
    for columns in range(1, 5):
        for bits in itertools.product((0, 1), repeat=rows * columns):
            grid = [
                list(bits[row * columns : (row + 1) * columns])
                for row in range(rows)
            ]
            for capacity in range(1, 11):
                check(grid, capacity)
                exhaustive_count += 1

random_generator = random.Random(115_20260726)
random_count = 0
for _ in range(500):
    rows = random_generator.randint(1, 100)
    columns = random_generator.randint(1, 100)
    grid = [
        [random_generator.randint(0, 1) for _ in range(columns)]
        for _ in range(rows)
    ]
    capacity = random_generator.randint(1, 10)
    check(grid, capacity)
    random_count += 1

print("SCOPE")
print(
    "exhaustive rectangular binary grids: rows=1..3, columns=1..4, "
    f"capacity=1..10; cases={exhaustive_count}"
)
print(
    "deterministic random rectangular binary grids: rows=1..100, "
    f"columns=1..100, capacity=1..10, seed=11520260726; cases={random_count}"
)
print(f"total_cases={case_count}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

if mismatches:
    raise SystemExit(1)
