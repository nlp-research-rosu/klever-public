#!/usr/bin/env python3
"""Independent differential test for HumanEval 126 is_sorted."""

from __future__ import annotations

from collections import Counter
import importlib.util
import itertools
from pathlib import Path
import random
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/candidate-fresh/solution.py"), "candidate_solution"
)


def contract_oracle(values: list[int]) -> bool:
    """Direct reading: nondecreasing and no value occurs over twice."""
    nondecreasing = all(
        values[index - 1] <= values[index] for index in range(1, len(values))
    )
    duplicate_bound = all(count <= 2 for count in Counter(values).values())
    return nondecreasing and duplicate_bound


documented_and_boundary_cases = [
    [],
    [5],
    [0],
    [1, 2, 3, 4, 5],
    [1, 3, 2, 4, 5],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6, 7],
    [1, 3, 2, 4, 5, 6, 7],
    [1, 2, 2, 3, 3, 4],
    [1, 2, 2, 2, 3, 4],
    [0, 0],
    [0, 0, 0],
    [0, 1, 1],
    [0, 1, 1, 1],
    [2, 1],
    [1, 2, 0],
    [2, 2, 1],
    [1, 1, 0],
    [10**100, 10**100],
    [0, 10**100],
    [10**100, 0],
]

cases: list[tuple[str, list[int]]] = [
    ("explicit", values) for values in documented_and_boundary_cases
]
for length in range(8):
    for values in itertools.product(range(4), repeat=length):
        cases.append(("exhaustive_0_to_3_len_0_to_7", list(values)))

random_source = random.Random(126_20260726)
for _ in range(10_000):
    length = random_source.randrange(0, 31)
    values = [random_source.randrange(0, 101) for _ in range(length)]
    cases.append(("deterministic_random", values))

mismatches: list[tuple[str, list[int], bool, bool, bool]] = []
scope_counts: Counter[str] = Counter()
for scope, values in cases:
    scope_counts[scope] += 1
    canonical_result = canonical(values.copy())
    candidate_result = candidate(values.copy())
    oracle_result = contract_oracle(values)
    if not (
        type(canonical_result) is bool
        and type(candidate_result) is bool
        and canonical_result == candidate_result == oracle_result
    ):
        mismatches.append(
            (
                scope,
                values,
                canonical_result,
                candidate_result,
                oracle_result,
            )
        )

print("ORACLE=direct nondecreasing-adjacent check plus Counter multiplicity <= 2")
print(f"SCOPE_COUNTS={dict(sorted(scope_counts.items()))}")
print(f"TOTAL_CASES={len(cases)}")
print(f"MISMATCH_COUNT={len(mismatches)}")
for record in mismatches[:20]:
    print(f"MISMATCH={record!r}")
for values in documented_and_boundary_cases:
    print(
        "EXPLICIT "
        f"{values!r} canonical={canonical(values.copy())!r} "
        f"candidate={candidate(values.copy())!r} oracle={contract_oracle(values)!r}"
    )

sys.exit(1 if mismatches else 0)
