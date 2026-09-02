#!/usr/bin/env python3
"""Ground witness for the entry precondition and its symbolic result."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def formal_summary(grid: list[list[int]], k: int) -> list[int]:
    one_row = 0
    one_col = 0
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == 1:
                one_row, one_col = row_index, col_index
    neighbor = len(grid) * len(grid)
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if abs(row_index - one_row) + abs(col_index - one_col) == 1:
                neighbor = min(neighbor, value)
    return [1 if index % 2 == 0 else neighbor for index in range(k)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()
    canonical = load("claim_canonical", args.canonical)
    generated = load("claim_generated", args.generated)

    witnesses = [
        ([[1, 2], [3, 4]], 1),
        ([[1, 2], [3, 4]], 3),
        ([[9, 8, 7], [6, 1, 5], [4, 3, 2]], 4),
    ]
    for grid, k in witnesses:
        n = len(grid)
        flat = [value for row in grid for value in row]
        precondition = (
            n >= 2
            and all(len(row) == n for row in grid)
            and sorted(flat) == list(range(1, n * n + 1))
            and k > 0
        )
        summary = formal_summary(grid, k)
        canon = canonical.minPath([row[:] for row in grid], k)
        actual = generated.minPath([row[:] for row in grid], k)
        print(
            {
                "grid": grid,
                "k": k,
                "entry_precondition": precondition,
                "formal_summary": summary,
                "canonical": canon,
                "generated": actual,
                "all_equal": summary == canon == actual,
            }
        )
        if not precondition or not (summary == canon == actual):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
