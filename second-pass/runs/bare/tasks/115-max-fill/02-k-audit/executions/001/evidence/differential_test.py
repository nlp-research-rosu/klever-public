#!/usr/bin/env python3
"""Independent deterministic differential test for HumanEval 115 max_fill."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_115")
generated = load_entry(Path("/tmp/audit-work/rebuild/solution.py"), "candidate_solution_115")

cases: list[tuple[str, list[list[int]], int, int | None]] = [
    ("prompt-example-1", [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1, 6),
    ("prompt-example-2", [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]], 2, 5),
    ("prompt-example-3", [[0, 0, 0], [0, 0, 0]], 5, 0),
    # Explicit out-of-contract empty boundaries requested by the audit.
    ("empty-grid", [], 1, 0),
    ("empty-row", [[]], 1, 0),
    # Minimum in-contract shape/capacity and both cell values.
    ("min-shape-zero", [[0]], 1, 0),
    ("min-shape-one", [[1]], 1, 1),
    # Ceiling boundaries around multiples of the capacity.
    ("water-c-minus-1", [[1, 1]], 3, 1),
    ("water-c", [[1, 1, 1]], 3, 1),
    ("water-c-plus-1", [[1, 1, 1, 1]], 3, 2),
    ("zero-water-cap-max", [[0] * 10], 10, 0),
    ("one-water-cap-max", [[1] + [0] * 9], 10, 1),
    ("full-row-cap-max", [[1] * 100], 10, 10),
    # Maximum documented dimensions with capacities at each endpoint.
    ("max-grid-cap-min", [[(r + c) % 2 for c in range(100)] for r in range(100)], 1, 5000),
    ("max-grid-cap-max", [[1 for _ in range(100)] for _ in range(100)], 10, 1000),
]

rng = random.Random(115_20260723)
for index in range(200):
    height = rng.randint(1, 30)
    width = rng.randint(1, 30)
    capacity = rng.randint(1, 10)
    grid = [[rng.randint(0, 1) for _ in range(width)] for _ in range(height)]
    cases.append((f"generated-{index:03d}", grid, capacity, None))

mismatches = 0
for name, grid, capacity, expected in cases:
    canonical_result = canonical(grid, capacity)
    generated_result = generated(grid, capacity)
    ok = canonical_result == generated_result and (
        expected is None or canonical_result == expected
    )
    if not ok:
        mismatches += 1
    print(
        json.dumps(
            {
                "name": name,
                "grid": grid,
                "capacity": capacity,
                "expected_if_fixed": expected,
                "canonical": canonical_result,
                "generated": generated_result,
                "ok": ok,
            },
            separators=(",", ":"),
        )
    )

print(
    json.dumps(
        {
            "summary": {
                "cases": len(cases),
                "generated_seed": 115_20260723,
                "mismatches": mismatches,
            }
        },
        separators=(",", ":"),
    )
)
raise SystemExit(1 if mismatches else 0)
