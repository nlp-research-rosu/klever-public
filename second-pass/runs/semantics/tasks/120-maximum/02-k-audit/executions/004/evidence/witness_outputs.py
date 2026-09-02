#!/usr/bin/env python3
"""Concrete satisfying witnesses for both formal entry preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/maximum-120-audit")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.maximum


canonical = load(ROOT / "canonical.py", "canonical_witness")
generated = load(ROOT / "solution.py", "generated_witness")

witnesses = [
    ("k-zero", [-3, 5], 0, []),
    ("k-positive", [-3, 5], 1, [5]),
    ("k-equals-length", [-3, 5], 2, [-3, 5]),
]

for name, arr, k, formal_expected in witnesses:
    precondition = k == 0 or (0 < k <= len(arr))
    canonical_result = canonical(arr.copy(), k)
    generated_result = generated(arr.copy(), k)
    print(
        f"{name}: arr={arr}, k={k}, precondition={precondition}, "
        f"formal_expected={formal_expected}, canonical={canonical_result}, "
        f"generated={generated_result}"
    )
    assert precondition
    assert canonical_result == formal_expected
    assert generated_result == formal_expected
