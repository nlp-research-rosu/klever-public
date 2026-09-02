#!/usr/bin/env python3
"""Differentially compare the trusted canonical and submitted Python entry points."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
submitted = load_function(
    "submitted_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)

documented = [
    [],
    [5],
    [2, 4, 3, 0, 1, 5],
    [2, 4, 3, 0, 1, 5, 6],
]
boundaries = [
    [0],
    [10**100],
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 2],
    [2, 0],
    [2, 1],
    [3, 0],
    [5, 5, 5],
    [2, 1, 2],
    [3, 2, 2],
    [10**100, 0, 10**100 - 1],
    [10**100, 7, 10**100],
]
exhaustive = [
    list(values)
    for length in range(5)
    for values in itertools.product(range(6), repeat=length)
]
rng = random.Random(880088)
generated = [
    [rng.randrange(0, 10**18) for _ in range(rng.randrange(0, 31))]
    for _ in range(500)
]

cases: list[list[int]] = []
seen: set[tuple[int, ...]] = set()
for case in documented + boundaries + exhaustive + generated:
    key = tuple(case)
    if key not in seen:
        cases.append(case)
        seen.add(key)

branch_counts = {"empty": 0, "ascending": 0, "descending": 0}
for index, case in enumerate(cases):
    canonical_input = list(case)
    submitted_input = list(case)
    canonical_before = list(canonical_input)
    submitted_before = list(submitted_input)
    expected = canonical(canonical_input)
    actual = submitted(submitted_input)
    direct = (
        []
        if not case
        else sorted(case, reverse=(case[0] + case[-1]) % 2 == 0)
    )
    if not case:
        branch_counts["empty"] += 1
    elif (case[0] + case[-1]) % 2 == 0:
        branch_counts["descending"] += 1
    else:
        branch_counts["ascending"] += 1
    assert expected == direct, (index, case, expected, direct)
    assert actual == expected, (index, case, actual, expected)
    assert canonical_input == canonical_before, (index, case, "canonical mutated")
    assert submitted_input == submitted_before, (index, case, "submitted mutated")
    assert expected is not canonical_input, (index, case, "canonical alias")
    assert actual is not submitted_input, (index, case, "submitted alias")

Path("/audit-output/evidence/differential-inputs.json").write_text(
    json.dumps(cases, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_generation=values[0..5],length[0..4],raw={len(exhaustive)}")
print("random_generation=seed=880088,length[0..30],values[0..10^18),raw=500")
print(f"unique_cases={len(cases)}")
print(f"branch_counts={branch_counts}")
print("mutation_or_alias_failures=0")
print("result_mismatches=0")
