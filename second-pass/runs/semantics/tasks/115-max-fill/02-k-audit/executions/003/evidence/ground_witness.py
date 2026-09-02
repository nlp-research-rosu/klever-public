#!/usr/bin/env python3
"""Evaluate a satisfying formal input in both trusted and generated Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


grid = [[1]]
capacity = 2
trusted = entry(Path("/reference/canonical.py"), "canonical_witness")
generated = entry(Path("/candidate/solution.py"), "generated_witness")
print(f"formal_GS=gCons(iCons(1, .IntSeq), .GridRows)")
print(f"formal_C={capacity}")
print(f"precondition_C_gt_0={capacity > 0}")
print(f"trusted_python_result={trusted(grid, capacity)}")
print(f"generated_python_result={generated(grid, capacity)}")
assert trusted(grid, capacity) == generated(grid, capacity) == 1
