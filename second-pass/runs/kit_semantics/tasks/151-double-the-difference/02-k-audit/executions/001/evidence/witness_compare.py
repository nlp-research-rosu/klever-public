#!/usr/bin/env python3
"""Concrete satisfying witnesses for both entry preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.double_the_difference


canonical = load(Path("/reference/canonical.py"), "witness_canonical")
candidate = load(
    Path("/tmp/audit-work/candidate-src/solution.py"), "witness_candidate"
)

witnesses = [
    ("empty", [], 0),
    ("examples-and-boundaries", [-3, -2, -1, 0, 1, 2, 3], 10),
    ("mixed-numeric", [1.5, 3, -5, 7.0, 5], 34),
]

for name, values, formal_dtd in witnesses:
    c = candidate(values)
    r = canonical(values)
    print(
        f"{name}: input={values!r} formal_dtd={formal_dtd} "
        f"candidate={c!r} canonical={r!r}"
    )
    assert c == formal_dtd
    assert r == formal_dtd

print("loop_precondition_witness: VS=.ValSeq INPUT=.ValSeq OLD=0 S=0")
print("whole_precondition_witness: VS=.ValSeq with exact initial cells")
