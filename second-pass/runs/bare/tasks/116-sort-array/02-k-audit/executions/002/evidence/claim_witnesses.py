#!/usr/bin/env python3
"""Concrete satisfiability/result witnesses for every candidate claim."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


root = Path("/tmp/audit-work")
canonical = load("canonical_witness", root / "reference/canonical.py")
candidate = load("candidate_witness", root / "candidate/solution.py")


def key(value: int) -> tuple[int, int]:
    return value.bit_count(), value


def before_eq(left: int, right: int) -> bool:
    return key(left) <= key(right)


def expected(values: list[int]) -> list[int]:
    return sorted(values, key=key)


helper_witnesses = [
    ("count-correct", "N=-5", (-5).bit_count() == 2),
    (
        "comparator-correct",
        "A=1, B=3; A>=0 and B>=0",
        candidate.comes_before(1, 3) == before_eq(1, 3),
    ),
    (
        "insert-empty",
        "X=3, values=[]",
        candidate.insert_sorted(3, []) == [3],
    ),
    (
        "insert-at-front",
        "X=1, Y=3, YS=[]; beforeEq(1,3)",
        before_eq(1, 3) and candidate.insert_sorted(1, [3]) == [1, 3],
    ),
]

entry_witnesses = [
    ("sort-empty-symbolic", [], True),
    ("sort-singleton-symbolic", [5], True),
    ("sort-pair-before", [1, 3], before_eq(1, 3)),
    ("sort-pair-after", [3, 1], not before_eq(3, 1)),
    (
        "sort-triple-abc",
        [0, 1, 3],
        before_eq(1, 3) and before_eq(0, 1),
    ),
    (
        "sort-triple-bac",
        [1, 0, 3],
        before_eq(0, 3) and not before_eq(1, 0) and before_eq(1, 3),
    ),
    (
        "sort-triple-bca",
        [3, 0, 1],
        before_eq(0, 1) and not before_eq(3, 0) and not before_eq(3, 1),
    ),
    (
        "sort-triple-acb",
        [0, 3, 1],
        not before_eq(3, 1) and before_eq(0, 1),
    ),
    (
        "sort-triple-cab",
        [1, 3, 0],
        not before_eq(3, 0) and not before_eq(1, 0) and before_eq(1, 3),
    ),
    (
        "sort-triple-cba",
        [3, 1, 0],
        not before_eq(1, 0) and not before_eq(3, 0) and not before_eq(3, 1),
    ),
    ("example-one", [1, 5, 2, 3, 4], True),
    ("example-three", [1, 0, 2, 3, 4], True),
    ("empty", [], True),
    ("duplicates", [3, 1, 3, 0, 1], True),
    ("wide-popcounts", [7, 8, 3, 2, 1, 0], True),
    ("negative-extension", [-2, -3, -4, -5, -6], True),
]

failures = 0
for claim, witness, satisfied in helper_witnesses:
    print(f"CLAIM {claim}: witness={witness}; obligation_satisfied={satisfied}")
    failures += not satisfied

for claim, values, precondition in entry_witnesses:
    model = expected(values)
    canonical_result = canonical.sort_array(list(values))
    candidate_result = candidate.sort_array(list(values))
    match = precondition and model == canonical_result == candidate_result
    print(
        f"CLAIM {claim}: input={values!r}; precondition={precondition}; model={model!r}; "
        f"canonical={canonical_result!r}; candidate={candidate_result!r}; match={match}"
    )
    failures += not match

example = [1, 5, 2, 3, 4]
example_result = expected(example)
ordered = all(
    before_eq(example_result[index], example_result[index + 1])
    for index in range(len(example_result) - 1)
)
same_multiplicity = Counter(example) == Counter(example_result)
print(
    "CLAIM example-ordered: "
    f"input={example!r}; output={example_result!r}; ordered={ordered}"
)
print(
    "CLAIM example-permutation: "
    f"input={example!r}; output={example_result!r}; "
    f"same_multiplicity={same_multiplicity}"
)
failures += not ordered
failures += not same_multiplicity

print(f"TOTAL_CLAIMS_WITNESSED={len(helper_witnesses) + len(entry_witnesses) + 2}")
print(f"FAILED_WITNESSES={failures}")
raise SystemExit(1 if failures else 0)
