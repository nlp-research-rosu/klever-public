#!/usr/bin/env python3
"""Default-CPython recursion-limit boundary differential.

This records a language-model/totality limitation rather than treating it as a
counterexample to the normal-return partial-correctness theorem.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load_entry("trusted_recursion_boundary", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_recursion_boundary",
    Path("/tmp/audit-work/candidate-src/solution.py"),
)

recursion_limit = sys.getrecursionlimit()
ones = recursion_limit + 150
values = [0, *([1] * ones), -2, 2]

trusted_result = canonical(values)
try:
    candidate_result: object = candidate(values)
except Exception as error:  # record the exact observed exceptional outcome
    candidate_result = f"{type(error).__name__}: {error}"

print(f"recursion_limit={recursion_limit}")
print(f"input_shape=[0] + [1]*{ones} + [-2, 2]")
print(f"length={len(values)}")
print(f"trusted_result={trusted_result!r}")
print(f"candidate_result={candidate_result!r}")
print("mismatch=exception-vs-bool")

assert trusted_result is True
assert isinstance(candidate_result, str)
assert candidate_result.startswith("RecursionError:")
