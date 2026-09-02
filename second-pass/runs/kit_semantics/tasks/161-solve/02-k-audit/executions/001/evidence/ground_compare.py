#!/usr/bin/env python3
"""Compare concrete substitutions of solveResult with both Python programs."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_solve(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


candidate = load_solve(
    "ground_candidate", "/tmp/audit-work/161-solve/scratch/solution.py"
)
canonical = load_solve(
    "ground_canonical", "/tmp/audit-work/161-solve/scratch/canonical.py"
)

ascii_cases = {
    "": "",
    "a1": "A1",
    "1#2": "2#1",
    "AzZa": "aZzA",
}

for input_string, claimed_model_result in ascii_cases.items():
    candidate_result = candidate(input_string)
    canonical_result = canonical(input_string)
    assert candidate_result == claimed_model_result
    assert canonical_result == claimed_model_result
    print(
        "GROUND_ASCII",
        repr(input_string),
        "CLAIM=",
        repr(claimed_model_result),
        "CANDIDATE=",
        repr(candidate_result),
        "CANONICAL=",
        repr(canonical_result),
    )

unicode_input = "é1"
claimed_model_result = "1é"
candidate_result = candidate(unicode_input)
canonical_result = canonical(unicode_input)
assert candidate_result == "É1"
assert canonical_result == "É1"
assert candidate_result != claimed_model_result
print(
    "GROUND_MODEL_BOUNDARY",
    repr(unicode_input),
    "FORMAL_CLAIM=",
    repr(claimed_model_result),
    "CANDIDATE_CPYTHON=",
    repr(candidate_result),
    "CANONICAL_CPYTHON=",
    repr(canonical_result),
)
print("GROUND_COMPARISON_PASS")
