#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for task 157."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/reconstruction")


def load_function(path: Path, module_name: str) -> Callable[[object, object, object], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


canonical = load_function(ROOT / "canonical.py", "trusted_canonical")
generated = load_function(ROOT / "solution.py", "generated_solution")

documented = [(3, 4, 5), (1, 2, 3)]
branch_and_order_boundaries = [
    (3, 4, 5),
    (3, 5, 4),
    (5, 3, 4),
    (5, 4, 3),
    (4, 3, 5),
    (4, 5, 3),
    (6, 8, 10),
    (7, 24, 25),
    (9, 40, 41),
    (2, 2, 2),
    (1, 1, 1),
    (1, 1, 2),
    (1, 2, 2),
    (2, 3, 4),
]
zero_and_sign_boundaries = [
    (0, 0, 0),
    (0, 3, 3),
    (0, 3, 4),
    (-3, 4, 5),
    (3, -4, 5),
    (3, 4, -5),
    (-3, -4, -5),
]
numeric_boundaries = [
    (10**25, 10**25, 10**25),
    (3.0, 4.0, 5.0),
    (0.3, 0.4, 0.5),
]

rng = random.Random(157)
generated_positive = [
    tuple(rng.randint(1, 10_000) for _ in range(3)) for _ in range(5000)
]
generated_signed = [
    tuple(rng.randint(-1000, 1000) for _ in range(3)) for _ in range(5000)
]
exhaustive_small_positive = list(itertools.product(range(1, 26), repeat=3))

categories = {
    "documented": documented,
    "branch_and_order_boundaries": branch_and_order_boundaries,
    "positive_exhaustive_1_to_25": exhaustive_small_positive,
    "positive_random_seed_157": generated_positive,
    "zero_and_sign_boundaries": zero_and_sign_boundaries,
    "signed_random_seed_157": generated_signed,
    "numeric_boundaries": numeric_boundaries,
}

total = 0
positive_mismatches: list[tuple[object, object, object, bool, bool]] = []
extended_mismatches: list[tuple[object, object, object, bool, bool]] = []

for category, cases in categories.items():
    mismatches = []
    for a, b, c in cases:
        expected = canonical(a, b, c)
        actual = generated(a, b, c)
        total += 1
        if expected != actual:
            mismatches.append((a, b, c, expected, actual))
    positive_category = category in {
        "documented",
        "branch_and_order_boundaries",
        "positive_exhaustive_1_to_25",
        "positive_random_seed_157",
    }
    if positive_category:
        positive_mismatches.extend(mismatches)
    else:
        extended_mismatches.extend(mismatches)
    print(
        f"{category}: cases={len(cases)} mismatches={len(mismatches)}"
        + (f" first={mismatches[:5]}" if mismatches else "")
    )

print(f"total_cases={total}")
print(f"positive_length_mismatches={len(positive_mismatches)}")
print(f"extended_numeric_mismatches={len(extended_mismatches)}")

# Empty/omitted arguments are inapplicable to a three-scalar-argument contract;
# nevertheless, verify that both implementations reject an arity-0 call alike.
for name, function in (("canonical", canonical), ("generated", generated)):
    try:
        function()
    except TypeError as error:
        print(f"{name}_arity0=TypeError:{error}")
    else:
        raise AssertionError(f"{name} unexpectedly accepted an arity-0 call")

if positive_mismatches:
    raise SystemExit(1)
