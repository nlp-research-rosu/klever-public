#!/usr/bin/env python3
"""Independent differential audit for HumanEval 92-any-int."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/92-any-int/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/92-any-int/src/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


canonical = load_function("trusted_canonical_92", TRUSTED)
generated = load_function("generated_solution_92", GENERATED)


class IntSubclass(int):
    def __repr__(self):
        return f"IntSubclass({int(self)})"


named_cases = [
    ("documented-first-sum", (5, 2, 7)),
    ("documented-no-sum", (3, 2, 2)),
    ("documented-negative", (3, -2, 1)),
    ("documented-floats", (3.6, -2.2, 2)),
    ("zero-empty-boundary", (0, 0, 0)),
    ("first-sum-only", (4, 6, 10)),
    ("second-sum-only", (4, 10, 6)),
    ("third-sum-only", (10, 4, 6)),
    ("none-near-first-boundary", (4, 6, 11)),
    ("negative-first-sum", (-5, 2, -3)),
    ("large-integers", (10**100, -(10**100), 0)),
    ("non-int-first", (1.0, 2, 3)),
    ("non-int-second", (1, 2.0, 3)),
    ("non-int-third", (1, 2, 3.0)),
    ("none-empty-like", (None, None, None)),
    ("strings-empty-like", ("", "", "")),
    ("bool-canonical-divergence", (True, 1, 2)),
    ("bool-zero-divergence", (False, 0, 0)),
    ("int-subclass-divergence", (IntSubclass(1), 1, 2)),
]


def outcome(function, args):
    try:
        return ("return", function(*args))
    except Exception as error:  # comparisons include exception type and message
        return ("raise", type(error).__name__, str(error))


mismatches = []
total = 0

print("NAMED_CASES")
for name, args in named_cases:
    expected = outcome(canonical, args)
    actual = outcome(generated, args)
    total += 1
    matches = expected == actual
    print(
        f"{name}: args={args!r} canonical={expected!r} "
        f"generated={actual!r} match={matches}"
    )
    if not matches:
        mismatches.append((name, args, expected, actual))

print("EXHAUSTIVE_INTEGER_CUBE")
integer_cube_mismatches = 0
for args in itertools.product(range(-5, 6), repeat=3):
    expected = outcome(canonical, args)
    actual = outcome(generated, args)
    total += 1
    if expected != actual:
        integer_cube_mismatches += 1
        mismatches.append(("integer-cube", args, expected, actual))
print("domain=[-5,5]^3 count=1331")
print(f"mismatches={integer_cube_mismatches}")

print("SEEDED_REPRESENTATIVE_NUMERIC_SAMPLE")
rng = random.Random(920092)
sample_values = [
    -10**30,
    -100,
    -2,
    -1,
    0,
    1,
    2,
    100,
    10**30,
    -2.5,
    -0.0,
    0.5,
    2.5,
    False,
    True,
    IntSubclass(-1),
    IntSubclass(0),
    IntSubclass(1),
]
sample_mismatches = 0
for _ in range(2000):
    args = tuple(rng.choice(sample_values) for _ in range(3))
    expected = outcome(canonical, args)
    actual = outcome(generated, args)
    total += 1
    if expected != actual:
        sample_mismatches += 1
        mismatches.append(("seeded-numeric", args, expected, actual))
print("seed=920092 draws=2000 value-pool=18")
print(f"mismatches={sample_mismatches}")

print("SUMMARY")
print(f"total_cases={total}")
print(f"total_mismatches={len(mismatches)}")
for index, mismatch in enumerate(mismatches[:40], 1):
    print(f"mismatch_{index}={mismatch!r}")

if integer_cube_mismatches:
    raise SystemExit("unexpected divergence for ordinary integer cube")
