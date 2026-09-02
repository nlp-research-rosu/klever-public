#!/usr/bin/env python3
"""Concrete satisfiability/result witnesses for all three candidate claims."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


trusted = load_module("trusted_ground", Path("/reference/canonical.py"))
candidate = load_module(
    "candidate_ground", Path("/tmp/audit-work/candidate-src/solution.py")
)


def independent_math(values: list[int]) -> bool:
    return any(
        values[i] + values[j] + values[k] == 0
        for i, j, k in itertools.combinations(range(len(values)), 3)
    )


entry_cases = [
    ([1, 1, -2], True),
    ([1, 2, 3, 7], False),
]

for values, expected in entry_cases:
    math_value = independent_math(values)
    trusted_value = trusted.triples_sum_to_zero(values)
    candidate_value = candidate.triples_sum_to_zero(values)
    print(
        "program/triples witness "
        f"IS={values!r} "
        f"hasZeroTriple={math_value} "
        f"trusted={trusted_value} candidate={candidate_value}"
    )
    assert math_value is expected
    assert trusted_value is expected
    assert candidate_value is expected

pair_cases = [
    (1, [1, -2], True),
    (1, [2, 3], False),
]

for first, rest, expected in pair_cases:
    pair_math = any(
        first + rest[j] + rest[k] == 0
        for j, k in itertools.combinations(range(len(rest)), 2)
    )
    helper_value = candidate._has_pair_sum(first, rest)
    trusted_entry_value = trusted.triples_sum_to_zero([first, *rest])
    candidate_entry_value = candidate.triples_sum_to_zero([first, *rest])
    print(
        "pair witness "
        f"FIRST={first} IS={rest!r} "
        f"hasPairWith={pair_math} helper={helper_value} "
        f"trusted_entry={trusted_entry_value} "
        f"candidate_entry={candidate_entry_value}"
    )
    assert pair_math is expected
    assert helper_value is expected
    assert trusted_entry_value is expected
    assert candidate_entry_value is expected

print("witnesses=4")
print("mismatches=0")
