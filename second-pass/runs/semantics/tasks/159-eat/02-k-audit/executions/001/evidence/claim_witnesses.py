#!/usr/bin/env python3
"""Ground witnesses for both entry-claim preconditions and postconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.eat


canonical = load("claim_witness_canonical", "/reference/canonical.py")
candidate = load("claim_witness_candidate", "/candidate/solution.py")

witnesses = [
    ("NEED_LE_REMAINING", (5, 6, 10), [5 + 6, 10 - 6]),
    ("REMAINING_LT_NEED", (2, 11, 5), [2 + 5, 0]),
]

for branch, values, claimed_result in witnesses:
    number, need, remaining = values
    domain = all(0 <= value <= 1000 for value in values)
    branch_condition = (
        need <= remaining
        if branch == "NEED_LE_REMAINING"
        else remaining < need
    )
    canonical_result = canonical(*values)
    candidate_result = candidate(*values)
    print(
        f"{branch}: input={values} domain={domain} "
        f"branch_condition={branch_condition} claimed={claimed_result} "
        f"canonical={canonical_result} candidate={candidate_result}"
    )
    assert domain and branch_condition
    assert claimed_result == canonical_result == candidate_result
