#!/usr/bin/env python3
"""Concrete satisfying witnesses for all six submitted entry claims."""

import importlib.util
from pathlib import Path


scratch = Path("/tmp/audit-work/closest-audit")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.find_closest_elements


canonical = load("claim_oracle", scratch / "canonical.py")
candidate = load("claim_candidate", scratch / "solution.py")

# (claim number, satisfying input, formal postcondition value)
witnesses = [
    (1, [1.0, 2.0, 3.0, 4.0, 5.0, 2.2], (2.0, 2.2)),
    (2, [1.0, 2.0, 3.0, 4.0, 5.0, 2.0], (2.0, 2.0)),
    (3, [1.0, 2.0], (1.0, 2.0)),  # A=1, B=2, A < B
    (4, [2.0, 1.0], (1.0, 2.0)),  # A=2, B=1, B < A
    (5, [2.0, 2.0], (2.0, 2.0)),  # A=B=2
    (6, [-10.0, -3.0, -3.5, 9.0], (-3.5, -3.0)),
]

for claim, values, formal_result in witnesses:
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    print(
        f"CLAIM {claim}: input={values!r} formal={formal_result!r} "
        f"canonical={canonical_result!r} candidate={candidate_result!r}"
    )
    assert canonical_result == formal_result
    assert candidate_result == formal_result

print(f"SATISFYING_WITNESSES={len(witnesses)}")
