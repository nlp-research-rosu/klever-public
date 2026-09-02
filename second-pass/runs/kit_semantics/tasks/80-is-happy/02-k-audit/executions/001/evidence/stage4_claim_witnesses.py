#!/usr/bin/env python3
"""Ground substitutions for the entry postcondition and loop precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


def scan_happy(codes: tuple[int, ...], index: int, previous2: int, previous1: int) -> bool:
    if not codes:
        return True
    current, *rest = codes
    if index < 2:
        return scan_happy(tuple(rest), index + 1, previous1, current)
    return (
        current != previous1
        and current != previous2
        and previous1 != previous2
        and scan_happy(tuple(rest), index + 1, previous1, current)
    )


canonical = load_entry(Path("/reference/canonical.py"), "witness_canonical")
candidate = load_entry(Path("/candidate/solution.py"), "witness_candidate")

for text in ("", "a", "aa", "abc", "aba", "abca", "abac"):
    codes = tuple(map(ord, text))
    claimed = len(codes) >= 3 and scan_happy(codes, 0, -1, -1)
    canonical_value = canonical(text)
    candidate_value = candidate(text)
    assert claimed is canonical_value is candidate_value
    print(
        f"input={text!r} codes={codes!r} "
        f"entry_post={claimed} canonical={canonical_value} candidate={candidate_value}"
    )

# Satisfiable loop-head state: after concrete prefix "ab", one character remains.
remaining = (ord("c"),)
index = 2
previous2 = ord("a")
previous1 = ord("b")
happy = True
loop_summary = happy and scan_happy(remaining, index, previous2, previous1)
assert loop_summary is True
print(
    "loop_witness="
    f"IS={remaining!r},I={index},P2={previous2},P1={previous1},H={happy}; "
    f"requires_I_ge_2={index >= 2}; final_happy={loop_summary}"
)
