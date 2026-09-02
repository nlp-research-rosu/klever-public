#!/usr/bin/env python3
"""Ground witnesses for all four entry claims and their formal result summaries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_witness", Path("/reference/canonical.py"))
candidate = load("candidate_solution_witness", Path("/tmp/audit-work/88-sort-array/solution.py"))

witnesses = [
    ("empty", [], "fresh list(.ValSeq)", None),
    ("singleton", [5], "fresh list(condRev(sortVS([5]), true))", 0),
    (
        "odd",
        [2, 4, 3, 0, 1, 5],
        "fresh list(sortVS([2,4,3,0,1,5]))",
        1,
    ),
    (
        "even",
        [2, 4, 3, 0, 1, 5, 6],
        "fresh list(condRev(sortVS([2,4,3,0,1,5,6]), true))",
        0,
    ),
]

for name, values, formal_result, expected_parity in witnesses:
    assert all(isinstance(value, int) and value >= 0 for value in values)
    if expected_parity is not None:
        assert values
        parity = (values[0] + values[-1]) % 2
        assert parity == expected_parity
    else:
        parity = "n/a"

    canonical_input = list(values)
    candidate_input = list(values)
    canonical_result = canonical.sort_array(canonical_input)
    candidate_result = candidate.sort_array(candidate_input)
    assert canonical_result == candidate_result
    assert canonical_input == values and candidate_input == values
    assert canonical_result is not canonical_input
    assert candidate_result is not candidate_input

    print(
        f"{name}: input={values} parity={parity} "
        f"formal_post={formal_result} python_result={candidate_result}"
    )

print("preconditions_satisfiable=4/4")
print("canonical_candidate_ground_agreement=4/4")
print("CLAIM_WITNESSES=PASS")
