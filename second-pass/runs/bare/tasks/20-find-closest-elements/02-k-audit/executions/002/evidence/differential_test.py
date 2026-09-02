#!/usr/bin/env python3
"""Independent differential test for HumanEval/20.

The oracle and candidate are imported from isolated scratch copies.  Inputs of
length at least two are the documented domain.  Empty and singleton lists are
also exercised and reported separately without counting their differing
out-of-contract behavior as an in-domain mismatch.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/closest-audit")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_function("candidate_solution", SCRATCH / "solution.py")


named_cases = [
    ("example_1", [1.0, 2.0, 3.0, 4.0, 5.0, 2.2]),
    ("example_2_duplicate", [1.0, 2.0, 3.0, 4.0, 5.0, 2.0]),
    ("length_2_ascending", [1.0, 2.0]),
    ("length_2_descending", [2.0, 1.0]),
    ("length_2_equal", [2.0, 2.0]),
    ("later_update", [0.0, 10.0, 1.0]),
    ("no_later_update", [0.0, 1.0, 10.0]),
    ("inner_swap_and_update", [3.0, 1.0, 2.0]),
    ("equal_gap_tie", [0.0, 2.0, 4.0]),
    ("negative_values", [-10.0, -3.0, -3.5, 9.0]),
    ("signed_zero", [-0.0, 0.0, 3.0]),
    ("large_magnitudes", [-1.0e100, 1.0e100, 1.0e100 + 1.0e85]),
    ("out_of_domain_empty", []),
    ("out_of_domain_singleton", [1.0]),
]


def outcome(function, values):
    try:
        return ("return", function(list(values)))
    except Exception as error:  # boundary behavior is intentionally recorded
        return ("raise", type(error).__name__, str(error))


in_domain_mismatches = []
out_of_domain_observations = []

for name, values in named_cases:
    expected = outcome(canonical, values)
    actual = outcome(candidate, values)
    if len(values) >= 2:
        if actual != expected:
            in_domain_mismatches.append((name, values, expected, actual))
    else:
        out_of_domain_observations.append((name, expected, actual))
    print(f"NAMED {name}: canonical={expected!r} candidate={actual!r}")

pool = (-2.0, -0.5, 0.0, 1.25, 3.0)
exhaustive_count = 0
for length in range(2, 6):
    for values in itertools.product(pool, repeat=length):
        exhaustive_count += 1
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        if actual != expected:
            in_domain_mismatches.append(
                (f"exhaustive_n{length}", list(values), expected, actual)
            )

rng = random.Random(20260726)
random_count = 2500
for index in range(random_count):
    length = rng.randint(2, 30)
    values = [
        rng.randint(-10000, 10000) / rng.choice((1.0, 2.0, 4.0, 10.0))
        for _ in range(length)
    ]
    expected = outcome(canonical, values)
    actual = outcome(candidate, values)
    if actual != expected:
        in_domain_mismatches.append(
            (f"random_{index}_n{length}", values, expected, actual)
        )

print(f"EXHAUSTIVE_INPUTS={exhaustive_count}")
print(f"RANDOM_INPUTS={random_count}")
print(f"IN_DOMAIN_MISMATCHES={len(in_domain_mismatches)}")
print(f"OUT_OF_DOMAIN_OBSERVATIONS={out_of_domain_observations!r}")
if in_domain_mismatches:
    for mismatch in in_domain_mismatches[:10]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
