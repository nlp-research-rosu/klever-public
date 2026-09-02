#!/usr/bin/env python3
"""Concrete satisfying witnesses for all three formal entry preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.circular_shift


canonical = load_entry("witness_canonical", Path("/reference/canonical.py"))
candidate = load_entry(
    "witness_candidate", Path("/tmp/audit-work/65-circular-shift/solution.py")
)

witnesses = [
    ("reverse", 12, 3, lambda n, shift: shift > n, "21"),
    (
        "negative",
        12,
        -1,
        lambda n, shift: not (shift > n) and shift < 0,
        "12",
    ),
    (
        "rotate",
        12,
        1,
        lambda n, shift: not (shift > n) and not (shift < 0),
        "21",
    ),
]

for branch, x, shift, precondition, claimed in witnesses:
    length = len(str(x))
    assert precondition(length, shift)
    canonical_result = canonical(x, shift)
    candidate_result = candidate(x, shift)
    print(
        f"{branch}: X={x} SHIFT={shift} len(str(X))={length} "
        f"precondition=True claimed={claimed!r} "
        f"canonical={canonical_result!r} candidate={candidate_result!r}"
    )
    assert claimed == canonical_result == candidate_result

print("PYTHON_WITNESSES: PASS")
