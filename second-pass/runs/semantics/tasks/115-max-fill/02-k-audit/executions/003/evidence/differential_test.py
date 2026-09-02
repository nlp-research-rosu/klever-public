#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/candidate/solution.py"), "candidate_solution")

examples = [
    ([[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1, 6),
    (
        [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]],
        2,
        5,
    ),
    ([[0, 0, 0], [0, 0, 0]], 5, 0),
]

tests: list[tuple[str, list[list[int]], int, int | None]] = []
for index, (grid, capacity, expected) in enumerate(examples, 1):
    tests.append((f"documented-example-{index}", grid, capacity, expected))

# Requested empty/boundary cases, including two useful out-of-contract empty shapes.
tests.extend(
    [
        ("empty-grid-extra", [], 1, 0),
        ("empty-row-extra", [[]], 10, 0),
        ("minimum-all-zero", [[0]], 1, 0),
        ("minimum-all-one", [[1]], 1, 1),
        ("capacity-upper-bound", [[1]], 10, 1),
        ("ceil-below-boundary", [[1] * 9], 10, 1),
        ("ceil-at-boundary", [[1] * 10], 10, 1),
        ("ceil-above-boundary", [[1] * 11], 10, 2),
        ("max-shape-all-zero", [[0] * 100 for _ in range(100)], 10, 0),
        ("max-shape-all-one-cap1", [[1] * 100 for _ in range(100)], 1, 10000),
        ("max-shape-all-one-cap10", [[1] * 100 for _ in range(100)], 10, 1000),
    ]
)

# Exhaust every valid binary rectangular grid through 3x3 for every allowed capacity.
for rows in range(1, 4):
    for cols in range(1, 4):
        for bits in itertools.product((0, 1), repeat=rows * cols):
            grid = [list(bits[row * cols : (row + 1) * cols]) for row in range(rows)]
            for capacity in range(1, 11):
                tests.append(("exhaustive-small", grid, capacity, None))

# Deterministic representative samples across the full documented dimensions.
rng = random.Random(115)
for _ in range(1000):
    rows = rng.randint(1, 100)
    cols = rng.randint(1, 100)
    grid = [[rng.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    capacity = rng.randint(1, 10)
    tests.append(("random-valid", grid, capacity, None))

mismatches = []
label_counts: dict[str, int] = {}
for label, grid, capacity, expected in tests:
    label_counts[label] = label_counts.get(label, 0) + 1
    trusted = canonical(grid, capacity)
    generated = candidate(grid, capacity)
    if trusted != generated or (expected is not None and trusted != expected):
        mismatches.append(
            {
                "label": label,
                "grid": grid,
                "capacity": capacity,
                "trusted": trusted,
                "generated": generated,
                "expected": expected,
            }
        )
        if len(mismatches) >= 20:
            break

print(f"total_cases={len(tests)}")
print(f"category_counts={label_counts}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch}")

assert not mismatches
