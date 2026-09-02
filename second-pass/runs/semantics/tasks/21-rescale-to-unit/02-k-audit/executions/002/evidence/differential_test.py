#!/usr/bin/env python3
"""Independent differential check of canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[float]], list[float]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def run(function: Callable[[list[float]], list[float]], values: list[float]) -> Any:
    try:
        return ("return", function(values.copy()))
    except Exception as error:  # Differentially compare behavior at boundaries.
        return ("raise", type(error).__name__, str(error))


def float_equal(left: float, right: float) -> bool:
    return left == right or (math.isnan(left) and math.isnan(right))


def result_equal(left: Any, right: Any) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "raise":
        return left[1] == right[1]
    left_values, right_values = left[1], right[1]
    return len(left_values) == len(right_values) and all(
        float_equal(x, y) for x, y in zip(left_values, right_values)
    )


scratch = Path("/tmp/audit-work/21-rescale-to-unit-audit")
canonical = load_entry(scratch / "canonical.py", "trusted_canonical")
candidate = load_entry(scratch / "solution.py", "generated_solution")

named_cases = [
    ("documented example", [1.0, 2.0, 3.0, 4.0, 5.0]),
    ("empty boundary (outside stated at-least-two domain)", []),
    ("singleton boundary (outside stated at-least-two domain)", [3.0]),
    ("two ascending", [0.0, 1.0]),
    ("two descending", [5.0, 1.0]),
    ("two negative", [-3.0, -1.0]),
    ("duplicates at extrema", [2.0, -2.0, 2.0, 0.0, -2.0]),
    ("mixed signs and repeated interior", [-10.0, -1.5, 0.0, -1.5, 7.25]),
    ("equal pair: denominator-zero boundary", [4.0, 4.0]),
    ("large finite magnitudes", [-1.0e150, 0.0, 1.0e150]),
    ("positive infinity", [1.0, float("inf")]),
    ("NaN first", [float("nan"), 1.0, 2.0]),
    ("NaN last", [1.0, 2.0, float("nan")]),
]

mismatches = 0
print("NAMED CASES")
for name, values in named_cases:
    expected = run(canonical, values)
    actual = run(candidate, values)
    match = result_equal(expected, actual)
    mismatches += not match
    print(f"{name}: input={values!r}")
    print(f"  canonical={expected!r}")
    print(f"  candidate={actual!r}")
    print(f"  match={match}")

rng = random.Random(210026)
generated_cases: list[list[float]] = []
for _ in range(2000):
    length = rng.randint(2, 25)
    values = [rng.randint(-100000, 100000) / 16.0 for _ in range(length)]
    if min(values) == max(values):
        values[-1] += 1.0
    generated_cases.append(values)

input_record = {
    "named_cases": [{"name": name, "values_repr": repr(values)} for name, values in named_cases],
    "generated_seed": 210026,
    "generated_cases": generated_cases,
}
input_path = Path("/audit-output/evidence/differential_inputs.json")
input_path.write_text(json.dumps(input_record, indent=2, allow_nan=True) + "\n")

for index, values in enumerate(generated_cases):
    expected = run(canonical, values)
    actual = run(candidate, values)
    if not result_equal(expected, actual):
        mismatches += 1
        print(
            f"GENERATED MISMATCH {index}: input={values!r} "
            f"canonical={expected!r} candidate={actual!r}"
        )

print(
    f"SUMMARY: named={len(named_cases)} generated={len(generated_cases)} "
    f"mismatches={mismatches}"
)
print(f"INPUT_CORPUS: {input_path}")
raise SystemExit(1 if mismatches else 0)
