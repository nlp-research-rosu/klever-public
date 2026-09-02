#!/usr/bin/env python3
"""Expose the generated implementation's CPython recursion-limit boundary."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strange_sort_list


canonical = load_function(Path("/reference/canonical.py"), "large_canonical")
candidate = load_function(Path("/candidate/solution.py"), "large_candidate")
values = list(range(2000))

canonical_result = canonical(list(values))
try:
    candidate_result: object = candidate(list(values))
except Exception as error:  # Deliberately record the observable divergence.
    candidate_result = f"{type(error).__name__}: {error}"

print(f"python_recursion_limit={sys.getrecursionlimit()}")
print(f"input_length={len(values)}")
print(f"canonical_result_length={len(canonical_result)}")
print(f"candidate_outcome={candidate_result}")
assert len(canonical_result) == 2000
assert isinstance(candidate_result, str)
assert candidate_result.startswith("RecursionError:")
print("LARGE-DOMAIN DIVERGENCE CONFIRMED")
