#!/usr/bin/env python3
"""Independent differential audit for HumanEval 115 max_fill."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


def independent_oracle(grid: list[list[int]], capacity: int) -> int:
    total = 0
    for row in grid:
        units = sum(row)
        quotient, remainder = divmod(units, capacity)
        total += quotient + (1 if remainder else 0)
    return total


ROOT = Path("/tmp/audit-work/115-max-fill")
canonical = load_entry(ROOT / "trusted/canonical.py", "trusted_canonical")
generated = load_entry(ROOT / "solution.py", "generated_solution")

cases: list[tuple[str, list[list[int]], int]] = [
    ("example-1", [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1),
    ("example-2", [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]], 2),
    ("example-3", [[0, 0, 0], [0, 0, 0]], 5),
    ("empty-grid-outside-contract", [], 1),
    ("empty-row-outside-contract", [[]], 10),
    ("minimum-zero", [[0]], 1),
    ("minimum-one", [[1]], 1),
    ("capacity-upper-bound", [[1]], 10),
    ("max-zero-grid", [[0] * 100 for _ in range(100)], 10),
    ("max-one-grid-cap-1", [[1] * 100 for _ in range(100)], 1),
    ("max-one-grid-cap-10", [[1] * 100 for _ in range(100)], 10),
]

# Exhaust every bit row through width 8 at every legal capacity.  This covers
# zero, exact multiples, and both sides of every reachable ceil boundary.
for width in range(0, 9):
    for bits in itertools.product((0, 1), repeat=width):
        for capacity in range(1, 11):
            cases.append((f"row-w{width}", [list(bits)], capacity))

# Exhaust representative multi-row combinations (three rows, widths 1..3).
small_rows = [list(bits) for width in range(1, 4)
              for bits in itertools.product((0, 1), repeat=width)]
for rows in itertools.product(small_rows, repeat=3):
    for capacity in (1, 2, 3, 10):
        cases.append(("three-row-exhaustive", [list(r) for r in rows], capacity))

# Deterministic broader samples across the full documented dimensions.
rng = random.Random(115)
for _ in range(1000):
    height = rng.randint(1, 100)
    width = rng.randint(1, 100)
    grid = [[rng.randrange(2) for _ in range(width)] for _ in range(height)]
    cases.append(("random-full-domain", grid, rng.randint(1, 10)))

mismatches = []
category_counts: dict[str, int] = {}
for label, grid, capacity in cases:
    category_counts[label] = category_counts.get(label, 0) + 1
    expected = canonical(grid, capacity)
    actual = generated(grid, capacity)
    oracle = independent_oracle(grid, capacity)
    if expected != actual or expected != oracle:
        mismatches.append({
            "label": label,
            "grid": grid,
            "capacity": capacity,
            "canonical": expected,
            "generated": actual,
            "oracle": oracle,
        })

print(json.dumps({
    "seed": 115,
    "total_cases": len(cases),
    "category_counts": category_counts,
    "mismatch_count": len(mismatches),
    "first_mismatches": mismatches[:10],
}, sort_keys=True, indent=2))
raise SystemExit(1 if mismatches else 0)
