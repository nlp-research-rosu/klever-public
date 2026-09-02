#!/usr/bin/env python3
"""Ground substitutions for the two positive claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/122-add-elements")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contribution(value: int) -> int:
    return value if -100 < value and value < 100 else 0


def sum_range(arr: list[int], start: int, end: int) -> int:
    if start >= end:
        return 0
    return contribution(arr[start]) + sum_range(arr, start + 1, end)


canonical = load("trusted_canonical_witness", SCRATCH / "canonical.py")
candidate = load("candidate_witness", SCRATCH / "solution.py")

# Entry claim witness.  Its precondition is 1 <= K <= len(A) <= 100.
entry_arr = [-99]
entry_k = 1
entry_precondition = 1 <= entry_k <= len(entry_arr) <= 100
entry_formal = sum_range(entry_arr, 0, entry_k)
print(
    "entry witness:",
    {
        "A": entry_arr,
        "K": entry_k,
        "precondition": entry_precondition,
        "formal_post": entry_formal,
        "candidate_python": candidate.add_elements(entry_arr, entry_k),
        "canonical_python": canonical.add_elements(entry_arr, entry_k),
    },
)

# Loop claim witness.  It represents the state after processing A[0] = 21.
loop_arr = [21, 3]
loop_k = 2
loop_i = 1
loop_total = 21
loop_value = 21
loop_precondition = 0 <= loop_i <= loop_k <= len(loop_arr)
loop_formal = loop_total + sum_range(loop_arr, loop_i, loop_k)
print(
    "loop witness:",
    {
        "A": loop_arr,
        "K": loop_k,
        "I": loop_i,
        "T": loop_total,
        "V": loop_value,
        "precondition": loop_precondition,
        "formal_post": loop_formal,
        "candidate_python_from_entry": candidate.add_elements(loop_arr, loop_k),
        "canonical_python_from_entry": canonical.add_elements(loop_arr, loop_k),
    },
)

assert entry_precondition and loop_precondition
assert entry_formal == candidate.add_elements(entry_arr, entry_k)
assert loop_formal == candidate.add_elements(loop_arr, loop_k)
raise SystemExit(0)
