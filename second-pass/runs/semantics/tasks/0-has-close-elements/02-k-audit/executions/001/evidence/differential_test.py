#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test.

The finite generated domain is explicit and reproducible.  This script does not
import or reproduce any K proof equation.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import random
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/0-has-close-elements")
MANIFEST = Path("/audit-output/evidence/differential-input-manifest.json")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_module("candidate_solution", SCRATCH / "solution.py")

edge_cases = [
    ([1.0, 2.0, 3.0], 0.5, "documented false"),
    ([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3, "documented true"),
    ([], 1.0, "empty list"),
    ([1.0], 1.0, "singleton"),
    ([1.0, 1.0], 0.1, "duplicate"),
    ([1.0, 1.3], 0.3, "strict exact threshold"),
    ([1.0, 1.3], math.nextafter(0.3, math.inf), "just above threshold"),
    ([1.0, 1.3], math.nextafter(0.3, -math.inf), "just below threshold"),
    ([-3.0, -2.75, 9.0], 0.5, "negative values"),
    ([0.0, -0.0], 0.0, "signed zero and zero threshold"),
    ([0.0, -0.0], math.ulp(0.0), "signed zero and positive threshold"),
    ([2.0, 2.0], 0.0, "duplicate with strict zero threshold"),
    ([2.0, 2.0], -1.0, "negative threshold"),
    ([math.inf, math.inf], 1.0, "positive infinities"),
    ([-math.inf, math.inf], math.inf, "opposite infinities"),
    ([math.nan, 1.0, 1.0], 0.1, "NaN plus duplicate finite values"),
    ([math.nan, math.nan], math.inf, "NaN values"),
    ([1.0, 1.0], math.nan, "NaN threshold"),
    ([1.0, 2.0], math.inf, "infinite threshold with finite distance"),
    ([1e308, -1e308], math.inf, "overflowing subtraction"),
    ([1.0, 5.0, 1.25], 0.3, "true only against later nonadjacent position"),
    ([5.0, 1.0, 1.25], 0.3, "true in later outer iteration"),
]

small_values = (-2.0, -0.0, 0.25, 1.0, 2.0)
small_thresholds = (-1.0, 0.0, 0.25, 0.5, 3.0)
max_exhaustive_length = 5
random_seed = 20260724
random_case_count = 3000

manifest = {
    "edge_cases": [
        {"numbers": xs, "threshold": t, "description": description}
        for xs, t, description in edge_cases
    ],
    "exhaustive": {
        "values": small_values,
        "thresholds": small_thresholds,
        "lengths": list(range(max_exhaustive_length + 1)),
    },
    "random": {
        "seed": random_seed,
        "count": random_case_count,
        "list_length_range": [0, 10],
        "integer_numerator_range": [-100, 100],
        "number_denominator": 8,
        "integer_threshold_numerator_range": [-16, 80],
        "threshold_denominator": 8,
    },
}
MANIFEST.write_text(json.dumps(manifest, indent=2, allow_nan=True) + "\n")

mismatches = []
checked = 0


def check(numbers, threshold, provenance):
    global checked
    expected = canonical.has_close_elements(numbers, threshold)
    actual = candidate.has_close_elements(numbers, threshold)
    checked += 1
    if type(actual) is not bool or actual != expected:
        mismatches.append(
            {
                "numbers": numbers,
                "threshold": threshold,
                "canonical": expected,
                "candidate": actual,
                "provenance": provenance,
            }
        )


for numbers, threshold, description in edge_cases:
    check(numbers, threshold, f"edge:{description}")

exhaustive_count = 0
for length in range(max_exhaustive_length + 1):
    for values in itertools.product(small_values, repeat=length):
        for threshold in small_thresholds:
            check(list(values), threshold, "exhaustive-small")
            exhaustive_count += 1

rng = random.Random(random_seed)
for _ in range(random_case_count):
    length = rng.randint(0, 10)
    numbers = [rng.randint(-100, 100) / 8.0 for _ in range(length)]
    threshold = rng.randint(-16, 80) / 8.0
    check(numbers, threshold, "deterministic-random")

print(f"edge_cases={len(edge_cases)}")
print(f"exhaustive_cases={exhaustive_count}")
print(f"random_cases={random_case_count}")
print(f"total_cases={checked}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], indent=2, allow_nan=True))
    sys.exit(1)
