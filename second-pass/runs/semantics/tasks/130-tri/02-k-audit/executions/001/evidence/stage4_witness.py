#!/usr/bin/env python3
"""Concrete witnesses for both entry preconditions and the intended recurrence."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.tri


def tri_at(index: int) -> int:
    if index == 0:
        return 1
    if index == 1:
        return 3
    if index % 2 == 0:
        return 1 + index // 2
    return tri_at(index - 1) + tri_at(index - 2) + 1 + (index + 1) // 2


canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
candidate = load_entry(
    "scratch_candidate_witness",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)

# Loop witness: I=2, R=0, H=0, and VS=[1,3].
# Hence n=I+R-1=1, a=triAt(0)=1, b=value=triAt(1)=3,
# i=2, heapLoc=1, scopeLoc=2, and prefixIndex(VS)=1=I-1.
loop_witness = {
    "I": 2,
    "R": 0,
    "H": 0,
    "n": 1,
    "VS": [1, 3],
    "a": tri_at(0),
    "b": tri_at(1),
    "value": tri_at(1),
    "i": 2,
    "prefixIndex(VS)": 1,
}
loop_requires = (
    loop_witness["I"] >= 2
    and loop_witness["R"] >= 0
    and loop_witness["prefixIndex(VS)"] == loop_witness["I"] - 1
)
print(f"loop_witness={loop_witness}")
print(f"loop_precondition_satisfied={loop_requires}")

for n in [0, 1, 2, 3, 4, 10]:
    formal_prefix = [tri_at(index) for index in range(n + 1)]
    canonical_result = canonical(n)
    candidate_result = candidate(n)
    print(
        f"N={n}; entry_requires={n >= 0}; formal_triPrefix={formal_prefix!r}; "
        f"canonical={canonical_result!r}; candidate={candidate_result!r}; "
        f"numeric_equal={formal_prefix == canonical_result == candidate_result}"
    )

entry_witness_n = 3
print(f"entry_witness_N={entry_witness_n}")
print(f"entry_precondition_satisfied={entry_witness_n >= 0}")
print(
    "claimed_index_constraint="
    f"prefixIndex(result)=={entry_witness_n}"
)
