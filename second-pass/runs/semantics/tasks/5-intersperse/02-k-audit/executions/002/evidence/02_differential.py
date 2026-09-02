#!/usr/bin/env python3
"""Independent differential test for HumanEval/5 intersperse."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/5-intersperse")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersperse


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
generated = load_function("generated_solution", SCRATCH / "solution.py")

explicit_cases = [
    ([], 4),
    ([1, 2, 3], 4),
    ([7], -2),
    ([0, 0], 0),
    ([-1, 0], 9),
    ([1, 2], -5),
    ([5, 5, 5], 5),
    ([0, -1, 2, -3], 0),
    ([10**80, -(10**80)], 10**100),
]

cases: list[tuple[list[int], int, str]] = [
    (numbers, delimiter, "explicit") for numbers, delimiter in explicit_cases
]

small_values = (-2, -1, 0, 1, 2)
small_delimiters = (-10, -1, 0, 1, 10)
for length in range(0, 6):
    for items in itertools.product(small_values, repeat=length):
        for delimiter in small_delimiters:
            cases.append((list(items), delimiter, "exhaustive-small"))

rng = random.Random(5005)
for _ in range(2000):
    length = rng.randrange(0, 41)
    numbers = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
    delimiter = rng.randrange(-(10**15), 10**15 + 1)
    cases.append((numbers, delimiter, "seeded-generated"))

mismatches = []
mutations = []
for index, (numbers, delimiter, source) in enumerate(cases):
    canonical_input = list(numbers)
    generated_input = list(numbers)
    canonical_result = canonical(canonical_input, delimiter)
    generated_result = generated(generated_input, delimiter)
    direct_oracle = [
        item
        for position, number in enumerate(numbers)
        for item in ((delimiter, number) if position else (number,))
    ]
    if canonical_input != numbers or generated_input != numbers:
        mutations.append((index, source, numbers, delimiter))
    if not (
        canonical_result == generated_result == direct_oracle
        and type(generated_result) is list
    ):
        mismatches.append(
            (
                index,
                source,
                numbers,
                delimiter,
                canonical_result,
                generated_result,
                direct_oracle,
            )
        )
        if len(mismatches) >= 10:
            break

print("oracle=trusted canonical.py plus independent direct construction")
print("explicit_cases=9")
print("exhaustive_small_lengths=0..5")
print("exhaustive_small_values=-2,-1,0,1,2")
print("exhaustive_small_delimiters=-10,-1,0,1,10")
print("seeded_generated_seed=5005 count=2000 lengths=0..40")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
print(f"input_mutation_count={len(mutations)}")
if mismatches:
    print(f"first_mismatches={mismatches!r}")
if mutations:
    print(f"first_input_mutations={mutations[:10]!r}")
raise SystemExit(1 if mismatches or mutations else 0)
