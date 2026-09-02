#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 19."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/19-sort-numbers/solution.py")
)

WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)

named_cases = [
    "",
    "three one five",
    *WORDS,
    "zero zero",
    "nine nine nine",
    "zero one two three four five six seven eight nine",
    "nine eight seven six five four three two one zero",
    "one nine one zero nine",
    " one",
    "one ",
    "one  zero",
    "  nine   zero  ",
]

cases = list(named_cases)
for size in range(5):
    cases.extend(" ".join(parts) for parts in itertools.product(WORDS, repeat=size))

rng = random.Random(190026)
for size in (5, 10, 25, 100, 1000):
    for _ in range(20):
        cases.append(" ".join(rng.choice(WORDS) for _ in range(size)))

mismatches = []
for case in cases:
    expected = canonical(case)
    actual = generated(case)
    if actual != expected:
        mismatches.append((case, expected, actual))
        if len(mismatches) >= 10:
            break

print(f"named_cases={len(named_cases)}")
print("exhaustive_valid_sizes=0..4")
print("random_seed=190026 random_sizes=5,10,25,100,1000 samples_per_size=20")
print(f"total_comparisons={len(cases) if not mismatches else 'stopped-early'}")
print(f"mismatch_count={len(mismatches)}")
for case, expected, actual in mismatches:
    print(f"MISMATCH input={case!r} canonical={expected!r} generated={actual!r}")

raise SystemExit(1 if mismatches else 0)
