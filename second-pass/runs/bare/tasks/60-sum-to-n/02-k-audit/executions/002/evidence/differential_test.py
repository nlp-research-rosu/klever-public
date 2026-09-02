#!/usr/bin/env python3
"""Independent differential test for HumanEval/60.

Oracle: the trusted mounted canonical implementation, copied to scratch.
Subject: the submitted solution.py, copied to scratch.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


canonical = load_module(
    "trusted_canonical",
    Path("/tmp/audit-work/reconstruction/trusted/canonical.py"),
)
candidate = load_module(
    "submitted_solution",
    Path("/tmp/audit-work/reconstruction/candidate/solution.py"),
)

documented_examples = [30, 100, 5, 10, 1]
empty_and_boundaries = [-100, -3, -2, -1, 0, 1, 2, 3]
exhaustive_small = list(range(-2000, 2001))
rng = random.Random(60060)
generated = [rng.randint(-10_000, 10_000) for _ in range(256)]
larger = [-100_000, -10_000, 10_000, 100_000]

inputs: list[int] = []
seen: set[int] = set()
for value in documented_examples + empty_and_boundaries + exhaustive_small + generated + larger:
    if value not in seen:
        seen.add(value)
        inputs.append(value)

mismatches: list[tuple[int, int, int]] = []
positive_mismatches = 0
negative_mismatches = 0
for n in inputs:
    expected = canonical.sum_to_n(n)
    actual = candidate.sum_to_n(n)
    if expected != actual:
        mismatches.append((n, expected, actual))
        if n >= 0:
            positive_mismatches += 1
        else:
            negative_mismatches += 1

print("oracle=/tmp/audit-work/reconstruction/trusted/canonical.py:sum_to_n")
print("subject=/tmp/audit-work/reconstruction/candidate/solution.py:sum_to_n")
print(f"documented_examples={documented_examples}")
print(f"empty_and_boundaries={empty_and_boundaries}")
print("exhaustive_small=[-2000,2000]")
print("generated_count=256 generated_seed=60060 generated_range=[-10000,10000]")
print(f"larger={larger}")
print(f"unique_input_count={len(inputs)}")
print(
    f"mismatch_count={len(mismatches)} "
    f"negative_mismatches={negative_mismatches} "
    f"nonnegative_mismatches={positive_mismatches}"
)
for n, expected, actual in mismatches[:20]:
    print(f"MISMATCH n={n} canonical={expected} candidate={actual}")
if len(mismatches) > 20:
    print(f"... {len(mismatches) - 20} additional mismatches omitted")

if mismatches:
    sys.exit(1)
