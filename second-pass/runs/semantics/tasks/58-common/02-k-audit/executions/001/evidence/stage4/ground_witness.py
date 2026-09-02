#!/usr/bin/env python3
"""Evaluate a satisfying ground instance in both Python implementations."""

import importlib.util
from pathlib import Path


def load_common(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


first = [2, 2, 1, 1]
second = [1, 2, 2]
algorithm_accumulator = [2, 1]
claimed_sorted_result = [1, 2]

canonical = load_common("canonical_ground_58", Path("/reference/canonical.py"))
candidate = load_common(
    "candidate_ground_58", Path("/tmp/audit-work/case58/solution.py")
)

canonical_result = canonical(first.copy(), second.copy())
candidate_result = candidate(first.copy(), second.copy())

print(f"FIRST={first}")
print(f"SECOND={second}")
print(f"commonSpec(FIRST,SECOND)={algorithm_accumulator}")
print(f"sortVS(commonSpec(FIRST,SECOND))={claimed_sorted_result}")
print(f"canonical.common={canonical_result}")
print(f"solution.common={candidate_result}")

assert canonical_result == claimed_sorted_result
assert candidate_result == claimed_sorted_result
