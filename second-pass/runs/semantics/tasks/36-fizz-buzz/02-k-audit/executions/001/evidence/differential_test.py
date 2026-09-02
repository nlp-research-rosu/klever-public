#!/usr/bin/env python3
"""Independent differential test for HumanEval/36 fizz_buzz."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/fizz-buzz-audit/solution.py"), "generated_solution"
)

# Explicitly cover documented examples, empty/negative behavior, loop entry,
# first divisibility decisions, both divisors, their overlap, and thresholds
# around selected values containing a digit seven.
named_cases = {
    "negative": [-20, -5, -1],
    "empty_and_outer_loop": [0, 1, 2],
    "divisor_11_boundary": [10, 11, 12],
    "divisor_13_boundary": [12, 13, 14],
    "first_selected_digit_7": [76, 77, 78],
    "documented_examples": [50, 78, 79],
    "second_selected_digit_7": [78, 79, 80],
    "overlap_11x13": [142, 143, 144],
    "multi_digit_sevens": [777, 778, 779],
    "representative_large": [1000, 2000, 9999, 10000],
}

rng = random.Random(360036)
random_cases = [rng.randint(-100, 5000) for _ in range(128)]
all_inputs = sorted(
    set(range(-20, 301))
    | {n for values in named_cases.values() for n in values}
    | set(random_cases)
)

mismatches: list[tuple[int, object, object]] = []
for n in all_inputs:
    expected = canonical(n)
    actual = generated(n)
    if actual != expected or type(actual) is not type(expected):
        mismatches.append((n, expected, actual))

for group, values in named_cases.items():
    rendered = ", ".join(
        f"{n}:{canonical(n)}" for n in values
    )
    print(f"{group}=[{rendered}]")
print("oracle=/reference/canonical.py:fizz_buzz")
print("subject=/tmp/audit-work/fizz-buzz-audit/solution.py:fizz_buzz")
print("exhaustive_integer_interval=-20..300")
print("seed=360036")
print("seeded_random_count=128 range=-100..5000")
print(f"unique_inputs={len(all_inputs)}")
print(f"mismatch_count={len(mismatches)}")
for item in mismatches[:20]:
    print(f"MISMATCH n={item[0]} canonical={item[1]!r} generated={item[2]!r}")

sys.exit(1 if mismatches else 0)
