#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path("/tmp/audit-work/candidate-src")


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observe(function: Any, value: list[Any]) -> dict[str, Any]:
    try:
        result = function(list(value))
        if isinstance(result, float) and math.isnan(result):
            rendered: Any = "NaN"
        else:
            rendered = result
        return {"kind": "return", "type": type(result).__name__, "value": rendered}
    except Exception as error:  # The exception type is observable behavior here.
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}


canonical = load("trusted_canonical", ROOT / "trusted-canonical.py")
candidate = load("submitted_solution", ROOT / "solution.py")

cases: list[tuple[str, list[Any]]] = [
    ("documented_odd", [3, 1, 2, 4, 5]),
    ("documented_even", [-10, 4, 6, 1000, 10, 20]),
    ("empty", []),
    ("singleton", [7]),
    ("smallest_even", [2, 10]),
    ("smallest_odd_gt_one", [9, 1, 5]),
    ("even_four_sorted", [1, 2, 3, 4]),
    ("even_four_reverse", [4, 3, 2, 1]),
    ("even_duplicates", [5, 5, 5, 5]),
    ("negative_odd", [-8, -1, -4]),
    ("mixed_float_odd", [1.5, -2.0, 8]),
    ("mixed_float_even", [1.5, -2.0, 8, 4.25]),
]

rng = random.Random(470047)
for length in range(1, 13):
    for sample in range(10):
        values = [rng.randint(-100, 100) for _ in range(length)]
        cases.append((f"generated_int_n{length}_s{sample}", values))

for length in range(1, 9):
    for sample in range(4):
        values = [rng.randint(-40, 40) / 4.0 for _ in range(length)]
        cases.append((f"generated_float_n{length}_s{sample}", values))

mismatches = 0
for name, values in cases:
    left = observe(canonical.median, values)
    right = observe(candidate.median, values)
    same = left == right
    mismatches += not same
    print(
        json.dumps(
            {
                "case": name,
                "input": values,
                "canonical": left,
                "candidate": right,
                "match": same,
            },
            sort_keys=True,
        )
    )

print(json.dumps({"cases": len(cases), "mismatches": mismatches}, sort_keys=True))
raise SystemExit(0 if mismatches == 0 else 1)
