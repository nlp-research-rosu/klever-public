#!/usr/bin/env python3
"""Ground the symbolic entry precondition and compare every asserted result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


canonical = load(Path("/reference/canonical.py"), "claim_canonical")
generated = load(Path("/tmp/audit-work/129-minPath/solution.py"), "claim_generated")

A, B, C = 2, 3, 4
print(
    "PRECONDITION_WITNESS "
    f"A={A} B={B} C={C} "
    f"in_range={all(2 <= value <= 4 for value in (A, B, C))} "
    f"pairwise_distinct={len({A, B, C}) == 3}"
)

claim_calls = [
    (
        "prompt-example-1",
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        3,
        [1, 2, 1],
    ),
    (
        "prompt-example-2",
        [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
        1,
        [1],
    ),
    ("symbolic-one-top-left", [[1, A], [B, C]], 4, [1, min(A, B), 1, min(A, B)]),
    ("symbolic-one-top-right", [[A, 1], [B, C]], 4, [1, min(A, C), 1, min(A, C)]),
    ("symbolic-one-bottom-left", [[A, B], [1, C]], 4, [1, min(A, C), 1, min(A, C)]),
    ("symbolic-one-bottom-right", [[A, B], [C, 1]], 4, [1, min(B, C), 1, min(B, C)]),
]

for label, grid, k, expected in claim_calls:
    canonical_result = canonical(grid, k)
    generated_result = generated(grid, k)
    print(
        f"{label}: grid={grid} k={k} expected={expected} "
        f"canonical={canonical_result} generated={generated_result}"
    )
    assert canonical_result == expected
    assert generated_result == expected
