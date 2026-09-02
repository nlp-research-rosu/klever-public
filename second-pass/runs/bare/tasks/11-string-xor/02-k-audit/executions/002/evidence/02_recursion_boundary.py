#!/usr/bin/env python3
"""Expose the candidate/canonical divergence at CPython's recursion boundary."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_entry(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load_entry("canonical_boundary", "/reference/canonical.py")
candidate = load_entry("candidate_boundary", "/candidate/solution.py")

print(f"python_recursion_limit={sys.getrecursionlimit()}")
mismatches = 0
for length in (997, 998, 1000, 1100):
    a = "0" * length
    b = "0" * length
    canonical_result = canonical(a, b)
    canonical_outcome = f"return:length={len(canonical_result)}"
    try:
        candidate_result = candidate(a, b)
        candidate_outcome = f"return:length={len(candidate_result)}"
    except Exception as error:  # Deliberately record the actual observable class.
        candidate_outcome = f"raise:{type(error).__name__}"
    differs = canonical_outcome != candidate_outcome
    mismatches += int(differs)
    print(
        f"length={length} canonical={canonical_outcome} "
        f"candidate={candidate_outcome} mismatch={str(differs).lower()}"
    )

assert mismatches >= 1
print(f"boundary_mismatches={mismatches}")
print("material_divergence_observed=true")
