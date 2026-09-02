#!/usr/bin/env python3
"""Ground witnesses for every submitted entry claim."""

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

witnesses = [
    ("c01", [15, -73, 14, -15], 1, "ground claim"),
    ("c02", [33, -2, -3, 45, 21, 109], 2, "ground claim"),
    ("c03", [], 0, "ground claim"),
    ("c04", [-999, -11, 0, 1, 9, 10], 0, "ground claim"),
    (
        "c05",
        [11, 12, 21, 22, 313, 314, 423, 424, 50005, 70008, 80007, 90009],
        4,
        "ground claim",
    ),
    ("c06", [15, 15, 15, 20, 20], 3, "ground claim"),
    ("c07", [10], 0, "N=10 satisfies N<=10"),
    (
        "c08",
        [11],
        1,
        "N=11 satisfies 11<=N<=99 and both parity conjuncts",
    ),
    (
        "c09",
        [12],
        0,
        "N=12 satisfies 11<=N<=99 and the negated parity conjunction",
    ),
    (
        "c10",
        [111],
        1,
        "N=111 satisfies 100<=N<=999 and both parity conjuncts",
    ),
    (
        "c11",
        [112],
        0,
        "N=112 satisfies 100<=N<=999 and the negated parity conjunction",
    ),
]

for label, values, claimed, reason in witnesses:
    canonical_result = canonical.specialFilter(list(values))
    submitted_result = submitted.specialFilter(list(values))
    assert canonical_result == submitted_result == claimed
    print(
        f"{label} values={values!r} claimed={claimed} "
        f"canonical={canonical_result} submitted={submitted_result} "
        f"satisfiable_reason={reason}"
    )
