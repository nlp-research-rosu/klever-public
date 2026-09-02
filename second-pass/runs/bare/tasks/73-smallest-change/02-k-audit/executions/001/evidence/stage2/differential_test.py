#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 73."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Callable


def load_entry(path: str, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


def independent_oracle(values: list[int]) -> int:
    return sum(
        values[index] != values[-index - 1]
        for index in range(len(values) // 2)
    )


canonical = load_entry("/reference/canonical.py", "trusted_canonical")
candidate = load_entry(
    "/tmp/audit-work/73-smallest-change/solution.py", "candidate_solution"
)

documented = [
    [1, 2, 3, 5, 4, 7, 9, 6],
    [1, 2, 3, 4, 3, 2, 2],
    [1, 2, 3, 2, 1],
]

branch_boundaries = [
    [],
    [7],
    [1, 1],
    [1, 2],
    [1, 0, 1],
    [1, 0, 2],
    [1, 2, 2, 1],
    [1, 2, 3, 1],
    [1, 2, 3, 4],
    [-(2**63), 0, 2**63 - 1],
    [-(2**63), 0, -(2**63)],
]

exhaustive = [
    list(items)
    for length in range(9)
    for items in itertools.product((-1, 0, 1), repeat=length)
]

rng = random.Random(730073)
random_cases = [
    [
        rng.choice((-(2**63), -7, -1, 0, 1, 7, 2**63 - 1))
        for _ in range(rng.randrange(0, 129))
    ]
    for _ in range(2000)
]

# The prompt states no length restriction. These stay within ordinary list
# memory but cross CPython's default recursion depth for the recursive rewrite.
long_boundaries = [
    list(range(2501)),
    list(range(1250)) + [999999] + list(reversed(range(1250))),
]

groups = [
    ("documented", documented),
    ("branch-boundary", branch_boundaries),
    ("exhaustive-small", exhaustive),
    ("seeded-random", random_cases),
    ("length-boundary", long_boundaries),
]

digest = hashlib.sha256()
total = 0
mismatches: list[dict[str, object]] = []

print(f"PYTHON_VERSION: {sys.version.split()[0]}")
print(f"RECURSION_LIMIT: {sys.getrecursionlimit()}")
print("INPUT_SCOPE:")
for group_name, cases in groups:
    print(f"  {group_name}: {len(cases)}")
    for case_index, values in enumerate(cases):
        total += 1
        digest.update(
            json.dumps(values, separators=(",", ":")).encode("utf-8") + b"\n"
        )
        expected = independent_oracle(values)
        canonical_value = canonical(values)
        if canonical_value != expected:
            raise AssertionError(
                f"trusted canonical disagrees with independent oracle: "
                f"{group_name}[{case_index}]"
            )
        try:
            candidate_value: object = candidate(values)
        except Exception as error:  # deliberate: exception is a divergence
            candidate_value = f"{type(error).__name__}: {error}"
        if candidate_value != expected:
            mismatch = {
                "group": group_name,
                "index": case_index,
                "length": len(values),
                "expected": expected,
                "canonical": canonical_value,
                "candidate": candidate_value,
                "input_prefix": values[:12],
                "input_suffix": values[-12:],
            }
            mismatches.append(mismatch)

print(f"TOTAL_CASES: {total}")
print(f"ORDERED_INPUT_SHA256: {digest.hexdigest()}")
print(f"MISMATCH_COUNT: {len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH:", json.dumps(mismatch, sort_keys=True))

raise SystemExit(1 if mismatches else 0)
