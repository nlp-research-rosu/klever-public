#!/usr/bin/env python3
"""Concrete satisfying witnesses for both entry-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "canonical_witness")
generated = load(Path("/tmp/audit-work/candidate-src/solution.py"), "generated_witness")

cases = [
    ("first-strict", ["a"], ["bb"], "A"),
    ("first-tie", ["x"], ["y"], "A"),
    ("second-strict", ["ab"], ["x"], "B"),
]

for label, first, second, expected_side in cases:
    left_total = sum(len(value) for value in first)
    right_total = sum(len(value) for value in second)
    expected = first if expected_side == "A" else second
    canonical_result = canonical(first, second)
    generated_result = generated(first, second)
    assert canonical_result is expected
    assert generated_result is expected
    print(
        f"{label}: A={first!r} B={second!r} "
        f"totalChars(A)={left_total} totalChars(B)={right_total} "
        f"claimed={expected_side} canonical={canonical_result!r} "
        f"generated={generated_result!r}"
    )

print(
    "loop-precondition witness: I=7, OLD=str([122]), "
    "ITEMS=ssCons([97,98],ssCons([], .StrSeq)); "
    "claimed accumulator=7+2+0=9"
)
print("RESULT: PASS")
