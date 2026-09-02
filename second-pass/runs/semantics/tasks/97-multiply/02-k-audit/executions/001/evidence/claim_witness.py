#!/usr/bin/env python3
"""Concrete substitutions into the formal unitDigitProduct result."""

import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


canonical = load("/reference/canonical.py", "canonical_witness")
submitted = load("/tmp/audit-work/candidate-src/solution.py", "submitted_witness")

for a, b in [(14, -15), (-14, -15), (0, 0), (9, 9), (-11, 9)]:
    formal_result = (a % 10) * (b % 10)
    expected = canonical(a, b)
    actual = submitted(a, b)
    print(
        f"A={a} B={b} unitDigitProduct={formal_result} "
        f"canonical={expected} submitted={actual}"
    )
    assert formal_result == expected == actual
