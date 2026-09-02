#!/usr/bin/env python3
"""Independent differential check for HumanEval 52.

The tested implementations are imported from the clean scratch copy.  The case
set is deterministic: explicit examples and branch boundaries, an exhaustive
small integer grid, deterministic generated integer cases, and a separately
reported extended-numeric sample outside the K claim's IntSeq domain.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


canonical_module = load_module("trusted_canonical", SCRATCH / "canonical.py")
generated_module = load_module("generated_solution", SCRATCH / "solution.py")
canonical = canonical_module.below_threshold
generated = generated_module.below_threshold

groups: dict[str, list[tuple[list, int]]] = {}

groups["documented_examples"] = [
    ([1, 2, 4, 10], 100),
    ([1, 20, 4, 10], 5),
]

groups["empty_and_integer_boundaries"] = [
    ([], 0),
    ([], -1),
    ([], 1),
    ([], -(10**100)),
    ([], 10**100),
    ([-1], 0),
    ([0], 0),
    ([1], 0),
    ([10**100 - 1], 10**100),
    ([10**100], 10**100),
    ([-(10**100)], -(10**100)),
    ([-(10**100) - 1], -(10**100)),
]

branch_cases: list[tuple[list[int], int]] = []
for threshold in (-10, 0, 10):
    branch_cases.extend(
        [
            ([threshold - 1, threshold - 2, threshold - 3], threshold),
            ([threshold], threshold),
            ([threshold + 1], threshold),
        ]
    )
    for position in range(4):
        equal_case = [threshold - 1] * 4
        equal_case[position] = threshold
        branch_cases.append((equal_case, threshold))

        greater_case = [threshold - 1] * 4
        greater_case[position] = threshold + 1
        branch_cases.append((greater_case, threshold))
groups["all_branch_boundaries"] = branch_cases

small_grid: list[tuple[list[int], int]] = []
for length in range(5):
    for values in itertools.product(range(-3, 4), repeat=length):
        for threshold in range(-3, 4):
            small_grid.append((list(values), threshold))
groups["exhaustive_small_integer_grid"] = small_grid

rng = random.Random(520052)
generated_cases: list[tuple[list[int], int]] = []
for _ in range(5000):
    length = rng.randrange(0, 31)
    values = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
    threshold = rng.randrange(-(10**12), 10**12 + 1)
    generated_cases.append((values, threshold))
groups["deterministic_generated_integers"] = generated_cases

# These cases test source-program fidelity but are outside the formal K theorem,
# whose entry claim accepts only IntSeq elements and an Int threshold.
groups["extended_numeric_outside_k_claim"] = [
    ([1.5, 2.25], 3),
    ([1.5, 3.0], 3),
    ([True, False], 2),
    ([float("-inf"), -1.0], 0),
    ([float("inf")], 0),
]

mismatches = []
exceptions = []
total = 0
for group_name, cases in groups.items():
    for index, (values, threshold) in enumerate(cases):
        total += 1
        try:
            expected = canonical(list(values), threshold)
            actual = generated(list(values), threshold)
        except Exception as error:  # Any unexpected divergence remains visible.
            exceptions.append(
                {
                    "group": group_name,
                    "index": index,
                    "input": repr((values, threshold)),
                    "exception": repr(error),
                }
            )
            continue
        if type(expected) is not type(actual) or expected != actual:
            mismatches.append(
                {
                    "group": group_name,
                    "index": index,
                    "input": repr((values, threshold)),
                    "canonical": repr(expected),
                    "generated": repr(actual),
                }
            )

summary = {
    "oracle": str(SCRATCH / "canonical.py"),
    "implementation": str(SCRATCH / "solution.py"),
    "oracle_sha256": sha256(SCRATCH / "canonical.py"),
    "implementation_sha256": sha256(SCRATCH / "solution.py"),
    "generated_seed": 520052,
    "groups": {name: len(cases) for name, cases in groups.items()},
    "explicit_inputs": {
        "documented_examples": repr(groups["documented_examples"]),
        "empty_and_integer_boundaries": repr(groups["empty_and_integer_boundaries"]),
        "all_branch_boundaries": repr(groups["all_branch_boundaries"]),
        "extended_numeric_outside_k_claim": repr(
            groups["extended_numeric_outside_k_claim"]
        ),
    },
    "exhaustive_grid_formula": {
        "lengths": "0..4",
        "element_values": "-3..3",
        "thresholds": "-3..3",
    },
    "generated_integer_formula": {
        "case_count": 5000,
        "list_lengths": "0..30",
        "elements": "uniform integers in [-10^12, 10^12]",
        "thresholds": "uniform integers in [-10^12, 10^12]",
    },
    "total_cases": total,
    "mismatch_count": len(mismatches),
    "exception_count": len(exceptions),
    "first_mismatches": mismatches[:20],
    "first_exceptions": exceptions[:20],
}
print(json.dumps(summary, indent=2, sort_keys=True))
sys.exit(1 if mismatches or exceptions else 0)
