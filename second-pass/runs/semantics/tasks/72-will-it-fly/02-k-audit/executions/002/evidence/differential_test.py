#!/usr/bin/env python3
"""Independent differential test for HumanEval/72.

Oracle: the trusted /reference/canonical.py copied into scratch.
Subject: the submitted /candidate/solution.py copied into scratch.
The test does not import any candidate proof equation or K artifact.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


canonical = load_entry(SCRATCH / "trusted" / "canonical.py", "trusted_canonical")
generated = load_entry(SCRATCH / "solution.py", "submitted_solution")

documented = [
    ([1, 2], 5, False),
    ([3, 2, 3], 1, False),
    ([3, 2, 3], 9, True),
    ([3], 5, True),
]

named_boundaries = [
    ([], 0),
    ([], -1),
    ([0], 0),
    ([0], -1),
    ([1], 1),
    ([1], 0),
    ([1, 2], 3),
    ([1, 2], 2),
    ([1, 2, 1], 4),
    ([1, 2, 1], 3),
    ([1, 2, 1], 2),
    ([1, 2, 2, 1], 6),
    ([1, 2, 2, 1], 5),
    ([-4, 9, -4], 1),
    ([-4, 9, -4], 0),
    ([10**100, 0, 10**100], 2 * 10**100),
    ([10**100, 0, 10**100], 2 * 10**100 - 1),
]

integer_cases: list[tuple[list[int], int]] = []
integer_cases.extend((q, w) for q, w, _ in documented)
integer_cases.extend(named_boundaries)

# Exhaust all list shapes through length five over a small signed alphabet,
# with thresholds spanning below, at, and above attainable sums.
for length in range(6):
    for values in itertools.product(range(-2, 3), repeat=length):
        q = list(values)
        integer_cases.extend((q, w) for w in range(-8, 9))

# Broader deterministic sample, emphasizing the exact sum branch boundary.
rng = random.Random(720026)
for _ in range(5000):
    q = [rng.randint(-10**6, 10**6) for _ in range(rng.randint(0, 30))]
    total = sum(q)
    integer_cases.extend(
        [(q, total - 1), (q, total), (q, total + 1), (q, rng.randint(-10**7, 10**7))]
    )

# The unannotated Python source also executes over ordinary numeric mixtures.
# These are reported separately because the K entry claims restrict elements
# and the weight to K Int.
extended_numeric_cases = [
    ([], 0.0),
    ([0.5], 0.5),
    ([0.5], 0),
    ([1.5, -2.0, 1.5], 1.0),
    ([1.5, -2.0, 1.5], 0.0),
    ([True, False, True], 2),
    ([True, False], 2),
]

mismatches: list[tuple[object, object, object, object]] = []
for q, w in integer_cases + extended_numeric_cases:
    expected = canonical(list(q), w)
    actual = generated(list(q), w)
    if expected != actual or type(expected) is not type(actual):
        mismatches.append((q, w, expected, actual))

for q, w, expected in documented:
    assert canonical(q, w) is expected
    assert generated(q, w) is expected

print(f"documented_examples={len(documented)}")
print(f"integer_cases={len(integer_cases)}")
print(f"extended_numeric_cases={len(extended_numeric_cases)}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
print("RESULT: zero mismatches")
