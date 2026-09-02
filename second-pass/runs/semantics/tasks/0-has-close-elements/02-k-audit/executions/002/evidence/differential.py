#!/usr/bin/env python3
"""Independent canonical/generated/property differential for HumanEval/0."""
from __future__ import annotations

import importlib.util
import itertools
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: str, module_name: str) -> Callable[[list[float], float], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


def independent_property(numbers: list[float], threshold: float) -> bool:
    """A position-pair oracle, independent of either source loop structure."""
    return any(math.fabs(left - right) < threshold
               for left, right in itertools.combinations(numbers, 2))


canonical = load_function("/tmp/audit-work/case/canonical.py", "trusted_canonical")
generated = load_function("/tmp/audit-work/case/solution.py", "candidate_solution")

named_cases: list[tuple[str, list[float], float]] = [
    ("example_false", [1.0, 2.0, 3.0], 0.5),
    ("example_true", [1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
    ("empty", [], 1.0),
    ("singleton", [1.0], 1.0),
    ("strict_equal_boundary", [1.0, 1.5], 0.5),
    ("strict_just_inside", [1.0, 1.5], 0.5000000000000001),
    ("strict_just_outside", [1.0, 1.5], 0.49999999999999994),
    ("duplicate_positive_threshold", [7.0, 7.0], 1e-12),
    ("duplicate_zero_threshold", [7.0, 7.0], 0.0),
    ("negative_threshold", [1.0, 1.0], -0.1),
    ("negative_values", [-4.0, -4.25, 10.0], 0.3),
    ("early_break", [1.0, 1.1, 100.0, 200.0], 0.2),
    ("last_pair_only", [0.0, 10.0, 20.0, 20.1], 0.2),
    ("nonadjacent_pair", [1.0, 100.0, 1.1], 0.2),
    ("large_finite", [1e308, 1e308, -1e308], 1.0),
    ("subnormal", [0.0, 5e-324], 1e-323),
    ("signed_zero", [-0.0, 0.0], 5e-324),
    ("positive_infinities", [math.inf, math.inf], 1.0),
    ("opposite_infinities", [-math.inf, math.inf], math.inf),
    ("nan_element", [math.nan, 0.0, 0.1], 0.2),
    ("nan_threshold", [0.0, 0.0], math.nan),
]

rng = random.Random(0xC105E)
pool = [
    -1000.0, -10.0, -1.0, -0.0, 0.0, 5e-324, 0.1, 0.25, 0.5,
    0.75, 1.0, 1.5, 2.0, 10.0, 1000.0,
]
threshold_pool = [-2.0, -0.0, 0.0, 5e-324, 1e-12, 0.1, 0.25, 0.5, 1.0, 10.0]
generated_cases: list[tuple[str, list[float], float]] = []
for index in range(2000):
    length = rng.randrange(0, 13)
    numbers = [
        (rng.choice(pool) if rng.random() < 0.55 else rng.uniform(-1000.0, 1000.0))
        for _ in range(length)
    ]
    threshold = rng.choice(threshold_pool) if rng.random() < 0.7 else rng.uniform(-2.0, 50.0)
    generated_cases.append((f"generated_{index:04d}", numbers, threshold))

all_cases = named_cases + generated_cases
Path("/audit-output/evidence/differential-inputs.json").write_text(
    json.dumps(
        [{"name": name, "numbers": numbers, "threshold": threshold}
         for name, numbers, threshold in all_cases],
        indent=2,
        allow_nan=True,
    )
    + "\n",
    encoding="utf-8",
)

mismatches: list[dict[str, Any]] = []
true_count = 0
false_count = 0
for name, numbers, threshold in all_cases:
    c_result = canonical(list(numbers), threshold)
    g_result = generated(list(numbers), threshold)
    p_result = independent_property(list(numbers), threshold)
    true_count += int(p_result)
    false_count += int(not p_result)
    if not (c_result == g_result == p_result):
        mismatches.append(
            {
                "name": name,
                "numbers": numbers,
                "threshold": threshold,
                "canonical": c_result,
                "generated": g_result,
                "property": p_result,
            }
        )

print("oracle=itertools.combinations + math.fabs(distance) < threshold")
print(f"seed=0xC105E named_cases={len(named_cases)} generated_cases={len(generated_cases)} total={len(all_cases)}")
print(f"property_true={true_count} property_false={false_count} mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(json.dumps(mismatch, allow_nan=True, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
