#!/usr/bin/env python3
"""Independent differential test of the trusted canonical and submitted Python."""

from __future__ import annotations

import importlib.util
import json
import math
import random
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/proof")
INPUT_RECORD = Path("/audit-output/evidence/differential_inputs.json")


def load_entry(module_name: str, path: Path) -> Callable[[list[float]], list[float]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def outcome(function: Callable[[list[float]], list[float]], values: list[float]) -> tuple[str, Any]:
    try:
        return ("return", function(deepcopy(values)))
    except Exception as error:  # deliberate parity check for boundary/error behavior
        return ("raise", type(error).__name__)


def float_equal(left: float, right: float) -> bool:
    if math.isnan(left) and math.isnan(right):
        return True
    return left == right


def equal(left: tuple[str, Any], right: tuple[str, Any]) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "raise":
        return left[1] == right[1]
    return len(left[1]) == len(right[1]) and all(
        float_equal(x, y) for x, y in zip(left[1], right[1])
    )


canonical = load_entry("trusted_canonical", SCRATCH / "canonical.py")
submitted = load_entry("submitted_solution", SCRATCH / "solution.py")

explicit: list[list[float]] = [
    [1.0, 2.0, 3.0, 4.0, 5.0],  # documented example
    [],                           # outside-domain empty boundary
    [7.0],                        # outside-domain singleton boundary
    [2.0, 2.0],                   # zero-range boundary
    [1.0, 2.0],                   # smallest valid ascending case
    [2.0, 1.0],                   # smallest valid descending case
    [-3.0, -2.0, 7.0],
    [-4.0, -4.0, 0.0, 9.0, 9.0],
    [-0.0, 0.0],
    [5e-324, 1e-323],
    [-1e308, 0.0, 1e308],
    [float("-inf"), 0.0, float("inf")],
    [float("nan"), 0.0, 1.0],
]

rng = random.Random(210029)
pool = [
    -1000.0,
    -10.5,
    -1.0,
    -0.0,
    0.0,
    0.125,
    1.0,
    2.5,
    10.0,
    1000.0,
]
generated: list[list[float]] = []
for index in range(2000):
    length = 2 + rng.randrange(24)
    if index % 2 == 0:
        values = [rng.choice(pool) for _ in range(length)]
    else:
        values = [rng.uniform(-1e6, 1e6) for _ in range(length)]
    generated.append(values)

cases = explicit + generated
INPUT_RECORD.write_text(
    json.dumps(
        {
            "generator": "random.Random(210029)",
            "explicit_cases": explicit,
            "generated_cases": generated,
        },
        allow_nan=True,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches: list[dict[str, Any]] = []
returns = 0
raises = 0
for index, values in enumerate(cases):
    expected = outcome(canonical, values)
    actual = outcome(submitted, values)
    returns += expected[0] == "return"
    raises += expected[0] == "raise"
    if not equal(expected, actual):
        mismatches.append(
            {
                "index": index,
                "input": values,
                "canonical": expected,
                "submitted": actual,
            }
        )

example_actual = submitted([1.0, 2.0, 3.0, 4.0, 5.0])
assert example_actual == [0.0, 0.25, 0.5, 0.75, 1.0]
overflow_boundary = submitted([-1e308, 0.0, 1e308])
assert not mismatches, json.dumps(mismatches[:10], allow_nan=True, indent=2)

print(f"cases={len(cases)} explicit={len(explicit)} generated={len(generated)}")
print(f"canonical_returns={returns} canonical_raises={raises}")
print(f"mismatches={len(mismatches)}")
print(f"documented_example={example_actual}")
print(f"overflow_boundary={overflow_boundary}")
print(f"inputs_record={INPUT_RECORD}")
