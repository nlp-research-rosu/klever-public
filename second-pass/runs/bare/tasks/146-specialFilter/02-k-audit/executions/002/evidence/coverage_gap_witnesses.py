#!/usr/bin/env python3
"""Source-valid inputs outside every submitted claim's formal entry domain."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical", Path("/reference/canonical.py"))
submitted = load("submitted", Path("/tmp/audit-work/candidate-src/solution.py"))

ground_claim_inputs = {
    (15, -73, 14, -15),
    (33, -2, -3, 45, 21, 109),
    (),
    (-999, -11, 0, 1, 9, 10),
    (11, 12, 21, 22, 313, 314, 423, 424, 50005, 70008, 80007, 90009),
    (15, 15, 15, 20, 20),
}


def submitted_claim_covers(values: list[int]) -> bool:
    if tuple(values) in ground_claim_inputs:
        return True
    # The five symbolic claims all have exactly ListExpr(Int(N)).
    if len(values) != 1:
        return False
    value = values[0]
    return value <= 10 or 11 <= value <= 99 or 100 <= value <= 999


outside = [
    [1001],
    [11, 11],
    [90000000000000000000000000000000000000000000000009],
]

for values in outside:
    canonical_result = canonical.specialFilter(list(values))
    submitted_result = submitted.specialFilter(list(values))
    assert canonical_result == submitted_result
    assert not submitted_claim_covers(values)
    print(
        f"values={values!r} source_valid=True claim_covered=False "
        f"canonical={canonical_result} submitted={submitted_result}"
    )
