#!/usr/bin/env python3
"""Exhibit ground entry states and compare both Python implementations."""

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
candidate = load(
    "candidate", Path("/tmp/audit-work/reconstruction/solution.py")
)

states = [
    # label, X, SHIFT, LEN, expected branch
    ("normal", 12, 1, 2, "SHIFT <= LEN"),
    ("normal-boundary", 12, 2, 2, "SHIFT <= LEN"),
    ("oversize", 12, 3, 2, "SHIFT > LEN"),
    ("negative-x-normal", -123, 1, 4, "SHIFT <= LEN"),
    ("negative-x-boundary", -123, 4, 4, "SHIFT <= LEN"),
    ("negative-x-oversize", -123, 5, 4, "SHIFT > LEN"),
]

for label, x, shift, length, branch in states:
    actual_length = len(str(x))
    precondition = (
        length == actual_length
        and shift >= 0
        and (
            (shift <= length and branch == "SHIFT <= LEN")
            or (shift > length and branch == "SHIFT > LEN")
        )
    )
    canonical_value = canonical.circular_shift(x, shift)
    candidate_value = candidate.circular_shift(x, shift)
    print(
        f"{label}: X={x} SHIFT={shift} LEN={length} "
        f"precondition={precondition} canonical={canonical_value!r} "
        f"candidate={candidate_value!r}"
    )
    assert precondition
    assert canonical_value == candidate_value
