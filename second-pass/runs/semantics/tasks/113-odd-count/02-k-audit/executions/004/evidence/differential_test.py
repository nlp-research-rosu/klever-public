#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 113 odd_count."""

from __future__ import annotations

import copy
import importlib.util
import itertools
from pathlib import Path
import random


ROOT = Path("/tmp/audit-work/rebuild")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", ROOT / "reference" / "canonical.py")
generated = load("candidate_solution", ROOT / "solution.py")

documented = [
    ["1234567"],
    ["3", "11111111"],
]
boundaries = [
    [],
    [""],
    ["0"],
    ["1"],
    ["2"],
    ["9"],
    ["02468"],
    ["13579"],
    ["1" * 9],
    ["1" * 10],
    ["1" * 11],
    ["0" * 10 + "1" * 10],
    ["0123456789" * 10],
    ["", "0", "1", "2468", "13579", ""],
    ["1" * 1000],
]
single_digit_branches = [[digit] for digit in "0123456789"]
two_digit_exhaustive = [
    ["".join(chars)] for chars in itertools.product("0123456789", repeat=2)
]

rng = random.Random(113)
generated_cases: list[list[str]] = []
for _ in range(1000):
    generated_cases.append(
        [
            "".join(rng.choice("0123456789") for _ in range(rng.randrange(0, 81)))
            for _ in range(rng.randrange(0, 13))
        ]
    )

cases = documented + boundaries + single_digit_branches + two_digit_exhaustive + generated_cases
mismatches: list[tuple[int, list[str], object, object]] = []
mutation_failures: list[tuple[int, list[str]]] = []
for index, case in enumerate(cases):
    canonical_input = copy.deepcopy(case)
    generated_input = copy.deepcopy(case)
    expected = canonical.odd_count(canonical_input)
    actual = generated.odd_count(generated_input)
    if expected != actual:
        mismatches.append((index, case, expected, actual))
    if canonical_input != case or generated_input != case:
        mutation_failures.append((index, case))

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"single_digit_branch_cases={len(single_digit_branches)}")
print(f"two_digit_exhaustive_cases={len(two_digit_exhaustive)}")
print(f"seeded_generated_cases={len(generated_cases)} seed=113")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
print(f"input_mutations={len(mutation_failures)}")
if mismatches:
    print(f"first_mismatch={mismatches[0]!r}")
if mutation_failures:
    print(f"first_input_mutation={mutation_failures[0]!r}")
raise SystemExit(1 if mismatches or mutation_failures else 0)
