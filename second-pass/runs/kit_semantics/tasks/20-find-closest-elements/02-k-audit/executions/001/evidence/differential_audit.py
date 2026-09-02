#!/usr/bin/env python3
"""Independent differential and contract checks for HumanEval 20."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from collections import Counter
from pathlib import Path
from typing import Callable


def load_entry(module_name: str, path: Path) -> Callable[[list[float]], tuple[float, float]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


def value_fingerprint(value: object) -> object:
    if isinstance(value, float):
        if math.isnan(value):
            return ("float", "nan", math.copysign(1.0, value))
        return ("float", value.hex())
    if isinstance(value, tuple):
        return ("tuple", tuple(value_fingerprint(item) for item in value))
    return (type(value).__name__, value)


def run(function: Callable, values: list[float]) -> tuple[str, object]:
    try:
        return ("return", value_fingerprint(function(list(values))))
    except Exception as err:  # diagnostic comparison includes out-of-contract calls
        return ("raise", type(err).__name__, str(err))


def intended_property(values: list[float], result: object) -> bool:
    if (
        len(values) < 2
        or not isinstance(result, tuple)
        or len(result) != 2
        or not all(isinstance(item, (int, float)) for item in result)
        or any(not math.isfinite(float(item)) for item in values)
    ):
        return False
    first, second = result
    if first > second:
        return False
    available = Counter(values)
    used = Counter(result)
    if any(used[key] > available[key] for key in used):
        return False
    minimum = min(abs(a - b) for a, b in itertools.combinations(values, 2))
    return abs(first - second) == minimum


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("generated_solution", Path("/candidate/solution.py"))

fixed_cases: list[tuple[str, str, list[float]]] = [
    ("out-of-contract", "empty", []),
    ("out-of-contract", "singleton", [1.0]),
    ("documented", "example-update", [1.0, 2.0, 3.0, 4.0, 5.0, 2.2]),
    ("documented", "example-duplicate", [1.0, 2.0, 3.0, 4.0, 5.0, 2.0]),
    ("branch", "two-ascending", [1.0, 2.0]),
    ("branch", "two-descending", [2.0, 1.0]),
    ("branch", "two-equal", [2.0, 2.0]),
    ("branch", "negative-order", [-1.0, -4.0]),
    ("branch", "later-update-ascending", [0.0, 10.0, 2.0]),
    ("branch", "later-update-descending", [10.0, 0.0, 8.0]),
    ("branch", "strict-tie-no-update", [0.0, 2.0, 4.0]),
    ("branch", "nonadjacent-closest", [0.0, 100.0, 1.0]),
    ("source-domain", "all-int-numbers", [1, 9, 3, 4]),
    ("source-domain", "mixed-int-float", [1, 2.5, 2, 10.0]),
    ("special-float", "signed-zero", [-0.0, 0.0]),
    ("special-float", "initial-nan", [float("nan"), 1.0]),
    ("special-float", "later-nan", [0.0, 2.0, float("nan")]),
    ("special-float", "infinities", [float("-inf"), 0.0, float("inf")]),
]

rng = random.Random(0x20C105E)
generated_finite: list[list[float]] = []
for _ in range(2000):
    length = rng.randint(2, 9)
    values = [rng.randint(-1000, 1000) / 8.0 for _ in range(length)]
    if rng.random() < 0.3:
        values[rng.randrange(length)] = values[rng.randrange(length)]
    generated_finite.append(values)

generated_numeric_tower: list[list[float]] = []
for _ in range(500):
    length = rng.randint(2, 9)
    values: list[float] = []
    for _index in range(length):
        integer = rng.randint(-100, 100)
        values.append(integer if rng.random() < 0.6 else integer + 0.5)
    generated_numeric_tower.append(values)

fixed_mismatches = 0
ordinary_mismatches = 0
ordinary_property_failures = 0
numeric_tower_mismatches = 0
numeric_tower_property_failures = 0

print("fixed_cases:")
for category, name, values in fixed_cases:
    canonical_outcome = run(canonical, values)
    generated_outcome = run(generated, values)
    mismatch = canonical_outcome != generated_outcome
    fixed_mismatches += int(mismatch)
    property_ok = False
    try:
        property_ok = intended_property(values, generated(list(values)))
    except Exception:
        pass
    print(
        f"  category={category} name={name} input={values!r} "
        f"canonical={canonical_outcome!r} generated={generated_outcome!r} "
        f"exact_mismatch={mismatch} intended_property={property_ok}"
    )

for values in generated_finite:
    ordinary_mismatches += int(run(canonical, values) != run(generated, values))
    ordinary_property_failures += int(not intended_property(values, generated(list(values))))

for values in generated_numeric_tower:
    numeric_tower_mismatches += int(run(canonical, values) != run(generated, values))
    numeric_tower_property_failures += int(
        not intended_property(values, generated(list(values)))
    )

print("generated_scope:")
print("  finite_seed=0x20C105E")
print("  finite_cases=2000 lengths=2..9 values=integer/8 in [-125,125]")
print("  numeric_tower_cases=500 lengths=2..9 values=ints-or-half-integers")
print("summary:")
print(f"  fixed_cases={len(fixed_cases)} fixed_exact_mismatches={fixed_mismatches}")
print(f"  ordinary_exact_mismatches={ordinary_mismatches}")
print(f"  ordinary_property_failures={ordinary_property_failures}")
print(f"  numeric_tower_exact_mismatches={numeric_tower_mismatches}")
print(f"  numeric_tower_property_failures={numeric_tower_property_failures}")

if ordinary_mismatches or ordinary_property_failures:
    raise SystemExit(1)
