#!/usr/bin/env python3
"""Independent differential audit for HumanEval 90."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/tmp/audit-work/proof/solution.py"), "candidate_solution")

# The named cases exercise every program branch, equality boundaries, the
# prompt examples, and Python's unbounded-integer behavior.
named_cases = [
    ("example_ascending", [1, 2, 3, 4, 5]),
    ("example_permuted", [5, 1, 4, 3, 2]),
    ("example_empty", []),
    ("example_duplicate_only", [1, 1]),
    ("singleton", [7]),
    ("two_ascending", [1, 2]),
    ("two_descending", [2, 1]),
    ("equal_then_greater", [1, 1, 2]),
    ("greater_then_equal_min", [1, 2, 1]),
    ("new_min_after_one_distinct", [3, 1]),
    ("new_min_after_two_distinct", [3, 5, 1]),
    ("between_min_and_second", [1, 9, 4]),
    ("equal_second", [1, 4, 4]),
    ("greater_than_second", [1, 4, 9]),
    ("several_new_minima", [8, 6, 4, 2, 0]),
    ("zeros_and_negative", [0, -1, 0]),
    ("negative_duplicates", [-1, -3, -2, -3]),
    ("all_equal_negative", [-9, -9, -9]),
    ("large_positive", [10**200, 10**199, 10**201]),
    ("large_negative", [-(10**200), -(10**199), -(10**201)]),
]

rng = random.Random(9000260726)
generated_cases: list[list[int]] = []
for _ in range(20_000):
    length = rng.randrange(0, 65)
    mode = rng.randrange(4)
    if mode == 0:
        values = [rng.randrange(-4, 5) for _ in range(length)]
    elif mode == 1:
        values = [rng.randrange(-10**12, 10**12 + 1) for _ in range(length)]
    elif mode == 2:
        pool = [rng.randrange(-100, 101) for _ in range(rng.randrange(1, 8))]
        values = [rng.choice(pool) for _ in range(length)]
    else:
        values = [
            rng.choice((-1, 1)) * rng.randrange(0, 10**80)
            for _ in range(length)
        ]
    generated_cases.append(values)

all_cases = [values for _, values in named_cases] + generated_cases
encoded = json.dumps(all_cases, separators=(",", ":")).encode()

mismatches = []
mutation_failures = []
for index, values in enumerate(all_cases):
    before = list(values)
    expected = canonical(list(values))
    actual = generated(values)
    if actual != expected:
        mismatches.append((index, values, expected, actual))
    if values != before:
        mutation_failures.append((index, before, values))

for name, values in named_cases:
    print(
        f"NAMED {name}: input={values!r} "
        f"canonical={canonical(list(values))!r} generated={generated(list(values))!r}"
    )
print(f"INPUT_COUNT: {len(all_cases)}")
print(f"INPUT_SHA256: {hashlib.sha256(encoded).hexdigest()}")
print(f"MISMATCH_COUNT: {len(mismatches)}")
print(f"INPUT_MUTATION_COUNT: {len(mutation_failures)}")
if mismatches:
    print(f"FIRST_MISMATCH: {mismatches[0]!r}")
if mutation_failures:
    print(f"FIRST_INPUT_MUTATION: {mutation_failures[0]!r}")
raise SystemExit(1 if mismatches or mutation_failures else 0)
