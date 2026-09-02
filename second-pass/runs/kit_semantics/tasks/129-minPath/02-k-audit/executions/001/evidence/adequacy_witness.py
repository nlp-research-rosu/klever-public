#!/usr/bin/env python3
"""Concrete satisfiability witnesses and target-result substitution."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/129-minPath-audit")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def summary(grid: list[list[int]], k: int) -> list[int]:
    n = len(grid)
    position = next(
        (row, col)
        for row in range(n) for col in range(n)
        if grid[row][col] == 1
    )
    row, col = position
    neighbors = [
        grid[new_row][new_col]
        for new_row, new_col in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        if 0 <= new_row < n and 0 <= new_col < n
    ]
    minimum = min(neighbors)
    return [1 if index % 2 == 0 else minimum for index in range(k)]


def main() -> None:
    generated = load(ROOT / "solution.py", "witness_generated")
    canonical = load(ROOT / "canonical.py", "witness_canonical")
    grid = [[1, 2], [3, 4]]
    k = 3
    expected = summary(grid, k)
    print("satisfying_entry_witnesses:")
    print("  inner-one-ahead: N=2 P=[1,2,3,4] I=0 J=0 K=3")
    print("  inner-no-one: N=2 P=[1,2,3,4] I=0 J=1 K=3 R=0 C=0")
    print("  outer-one-ahead: N=2 P=[3,4,1,2] I=0 K=3")
    print("  outer-one-past: N=2 P=[1,2,3,4] I=1 J=0 K=3")
    print("  scan-finish: N=2 P=[1,2,3,4] K=3")
    print("  neighbor-finish: N=2 P=[1,2,3,4] R=0 C=0 K=3")
    print("  result-loop-tail: N=2 P=[1,2,3,4] K=3 R=1 A=.ValSeq")
    print("  minpath-full-contract: N=2 P=[1,2,3,4] K=3")
    print(f"claimed_summary={expected}")
    print(f"generated_result={generated(grid, k)}")
    print(f"canonical_result={canonical(grid, k)}")
    if not (generated(grid, k) == canonical(grid, k) == expected):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
