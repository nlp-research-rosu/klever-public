#!/usr/bin/env python3
"""Concrete satisfying witnesses for every candidate claim shape."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/74-total-match")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match


canonical = load("trusted_canonical_witness", ROOT / "canonical.py")
generated = load("candidate_solution_witness", ROOT / "solution.py")

witnesses = [
    ("entry-left-empty-tie", [], []),
    ("entry-left-nonempty-tie", ["ab"], ["c", "d"]),
    ("entry-right", ["ab"], [""]),
]
for label, left, right in witnesses:
    total_left = sum(map(len, left))
    total_right = sum(map(len, right))
    can = canonical(left, right)
    gen = generated(left, right)
    branch = "LEFT" if total_left <= total_right else "RIGHT"
    expected = left if branch == "LEFT" else right
    print(
        f"{label} totals=({total_left},{total_right}) branch={branch} "
        f"canonical={can!r} generated={gen!r} "
        f"canonical_identity={can is expected} generated_identity={gen is expected}"
    )
    assert can is expected and gen is expected

# The loop claim has no explicit side condition. This ground state instantiates
# I=7, OLD=int(99), and remaining strings ["ab", ""], so its claimed result is 9.
print(
    "loop-ground "
    "I=7 OLD=int(99) "
    "ITEMS=ssCons(iCons(97,iCons(98,.IntSeq)),"
    "ssCons(.IntSeq,.StrSeq)) "
    "claimed_result=7+2+0=9"
)
print("CLAIM_WITNESS_RESULT OK")
