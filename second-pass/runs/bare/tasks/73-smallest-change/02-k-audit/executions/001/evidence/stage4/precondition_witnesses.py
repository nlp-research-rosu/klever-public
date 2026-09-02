#!/usr/bin/env python3
"""Ground witnesses for each symbolic precondition family in spec.k."""

from __future__ import annotations

import importlib.util
from collections.abc import Callable


def load_entry(path: str, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


candidate = load_entry(
    "/tmp/audit-work/73-smallest-change/solution.py", "candidate_witness"
)
canonical = load_entry("/reference/canonical.py", "canonical_witness")

witnesses = [
    (
        "program-base / math-base",
        [],
        "size(L) <= 1",
        "program RHS finish(0); math RHS 0",
    ),
    (
        "program-equal / math-equal",
        [1, 9, 1],
        "size(L) > 1 and L[0] == L[-1]",
        "program RHS recur(body,[9],body); math RHS minimum([9])",
    ),
    (
        "program-unequal / math-unequal",
        [1, 9, 2],
        "size(L) > 1 and L[0] != L[-1]",
        "program RHS recur(body,[9],body) ~> addResult(1); "
        "math RHS 1 + minimum([9])",
    ),
]

for name, values, condition, formal_rhs in witnesses:
    print(f"CLAIM_FAMILY: {name}")
    print(f"WITNESS: {values!r}")
    print(f"PRECONDITION: {condition}")
    print(f"FORMAL_RHS: {formal_rhs}")
    print(f"CANDIDATE_PYTHON_FINAL: {candidate(values)}")
    print(f"CANONICAL_PYTHON_FINAL: {canonical(values)}")

examples = [
    [1, 2, 3, 5, 4, 7, 9, 6],
    [1, 2, 3, 4, 3, 2, 2],
    [1, 2, 3, 2, 1],
]
for index, values in enumerate(examples, 1):
    print(f"EXAMPLE_CLAIM_{index}: {values!r}")
    print(f"CANDIDATE_PYTHON_FINAL: {candidate(values)}")
    print(f"CANONICAL_PYTHON_FINAL: {canonical(values)}")
