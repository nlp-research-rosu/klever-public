#!/usr/bin/env python3
"""Concrete substitutions into the formal scanSorted result expression."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/126-is-sorted")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def scan_sorted(result: bool, prev: int, duplicates: int, values: list[int]) -> bool:
    for value in values:
        next_duplicates = duplicates + 1 if value == prev else 0
        result = result and not (value < prev) and not (next_duplicates > 1)
        prev = value
        duplicates = next_duplicates
    return result


canonical = load_entry("witness_canonical", ROOT / "canonical.py")
generated = load_entry("witness_generated", ROOT / "solution.py")

cases = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [0, 2, 1],
    [0, 1, 1, 2, 2],
    [0, 1, 1, 1, 2],
    [10**100],
]

for case in cases:
    assert all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in case)
    claimed = scan_sorted(True, -1, 0, case)
    trusted = canonical(case.copy())
    candidate = generated(case.copy())
    print(f"input={case!r} precondition=true claimed={claimed} canonical={trusted} generated={candidate}")
    if not (type(claimed) is bool and claimed == trusted == candidate):
        raise SystemExit(1)

print("entry_witness=[] satisfies nonNegativeInts")
print("loop_witness=input_[0,0], state_after_first: IS=[0], RESULT=true, PREV=0, DUPLICATES=0")
