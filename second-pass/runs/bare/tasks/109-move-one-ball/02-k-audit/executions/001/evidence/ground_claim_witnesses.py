#!/usr/bin/env python3
"""Ground substitutions for both entry claims, compared with both Python entries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


canonical = load(Path("/reference/canonical.py"), "ground_canonical")
generated = load(Path("/tmp/audit-work/source/solution.py"), "ground_generated")


def cyclic_drops(values: list[int]) -> int:
    if not values:
        return 0
    previous = values[-1]
    drops = 0
    for value in values:
        if previous > value:
            drops += 1
        previous = value
    return drops


cases = [
    ("empty-claim", []),
    ("nonempty-true", [3, 4, 5, 1, 2]),
    ("nonempty-false", [2, 1, 3]),
]

for label, values in cases:
    drops = cyclic_drops(values)
    claimed = True if not values else drops <= 1
    can = canonical(values.copy())
    gen = generated(values.copy())
    print(
        f"{label}: input={values}; cyclicDrops={drops}; "
        f"claimed_result={claimed}; canonical={can}; generated={gen}"
    )
    if claimed != can or claimed != gen:
        raise SystemExit(1)

print("ENTRY_PRECONDITION_WITNESSES=empty .IList; nonempty 3 :: 4 :: 5 :: 1 :: 2 :: .IList")
print("MISMATCH_COUNT=0")

