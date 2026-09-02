#!/usr/bin/env python3
"""Independent differential audit for 127-intersection.

The oracle is the trusted mounted canonical implementation.  The system under
test is the candidate's generated solution.py copied into the scratch tree.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


ROOT = Path("/tmp/audit-work/127-intersection")
canonical = load_entry(ROOT / "trusted" / "canonical.py", "trusted_canonical")
candidate = load_entry(ROOT / "run" / "solution.py", "candidate_solution")

# Named cases cover all source branch boundaries and the documented examples.
named_cases = [
    ("example_touch", (1, 2), (2, 3)),
    ("example_length_one", (-1, 1), (0, 4)),
    ("example_prime_two", (-3, -1), (-5, 5)),
    ("disjoint_gap", (0, 1), (3, 4)),
    ("both_singletons", (0, 0), (0, 0)),
    ("equal_left_boundary", (0, 8), (0, 5)),
    ("second_left_wins", (0, 8), (2, 8)),
    ("first_left_wins", (2, 8), (0, 8)),
    ("equal_right_boundary", (0, 8), (2, 8)),
    ("second_right_wins", (0, 8), (2, 7)),
    ("first_right_wins", (0, 7), (2, 8)),
    ("length_one", (0, 1), (0, 1)),
    ("length_two", (0, 2), (0, 2)),
    ("length_three", (0, 3), (0, 3)),
    ("length_four_factor_two", (0, 4), (0, 4)),
    ("length_five_loop_increment", (0, 5), (0, 5)),
    ("length_six_factor_two", (0, 6), (0, 6)),
    ("length_nine_factor_three", (0, 9), (0, 9)),
    ("length_97_prime", (-50, 47), (-100, 100)),
    ("length_121_factor_11", (-60, 61), (-100, 100)),
    ("large_integer_prime_two", (10**30, 10**30 + 2), (0, 10**31)),
]

mismatches = []
for label, first, second in named_cases:
    expected = canonical(first, second)
    actual = candidate(first, second)
    print(f"NAMED {label}: {first} {second} -> canonical={expected} candidate={actual}")
    if actual != expected:
        mismatches.append((label, first, second, expected, actual))

# Exhaust every valid closed interval whose endpoints lie in [-6, 6].
small_intervals = [(a, b) for a in range(-6, 7) for b in range(a, 7)]
small_count = 0
for first, second in itertools.product(small_intervals, repeat=2):
    small_count += 1
    expected = canonical(first, second)
    actual = candidate(first, second)
    if actual != expected:
        mismatches.append(("exhaustive", first, second, expected, actual))

# Deterministic generated intervals exercise a broader integer range.
rng = random.Random(127)
generated_count = 2_000
for index in range(generated_count):
    endpoints = sorted((rng.randint(-10_000, 10_000), rng.randint(-10_000, 10_000)))
    other_endpoints = sorted(
        (rng.randint(-10_000, 10_000), rng.randint(-10_000, 10_000))
    )
    first = (endpoints[0], endpoints[1])
    second = (other_endpoints[0], other_endpoints[1])
    expected = canonical(first, second)
    actual = candidate(first, second)
    if actual != expected:
        mismatches.append((f"generated-{index}", first, second, expected, actual))

print(f"NAMED_CASES={len(named_cases)}")
print(f"EXHAUSTIVE_VALID_INTERVAL_PAIRS={small_count}")
print(f"DETERMINISTIC_GENERATED_PAIRS={generated_count}")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch}")
    raise SystemExit(1)
