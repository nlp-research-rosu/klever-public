#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(path: Path, module_name: str) -> Callable[[list], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


def observe(function: Callable[[list], Any], values: list) -> dict[str, Any]:
    argument = list(values)
    try:
        result = function(argument)
        if isinstance(result, float) and math.isnan(result):
            result = "NaN"
        observation = {
            "kind": "return",
            "type": type(result).__name__,
            "value": result,
        }
    except Exception as err:  # The exception class is observable for boundary cases.
        observation = {
            "kind": "raise",
            "type": type(err).__name__,
        }
    observation["input_unchanged"] = argument == values
    return observation


def main() -> int:
    canonical = load_entry(SCRATCH / "canonical.py", "trusted_canonical")
    candidate = load_entry(SCRATCH / "solution.py", "submitted_solution")

    cases: list[tuple[str, list]] = [
        ("prompt_odd_example", [3, 1, 2, 4, 5]),
        ("prompt_even_example", [-10, 4, 6, 1000, 10, 20]),
        ("empty_boundary", []),
        ("one_element_boundary", [7]),
        ("two_element_even_boundary", [2, 1]),
        ("three_element_odd_boundary", [9, -1, 4]),
        ("four_element_even_boundary", [4, 1, 3, 2]),
        ("odd_duplicates", [5, 5, 1, 5, 2]),
        ("even_duplicates", [5, 5, 5, 5]),
        ("odd_floats", [2.5, -1.0, 7.25]),
        ("even_floats", [8.0, 1.5, -3.25, 2.0]),
        ("mixed_numeric_even", [1, 2.5, -4, 9.0, 3, 7]),
    ]

    rng = random.Random(470047)
    for length in range(1, 13):
        for sample in range(8):
            values = [rng.randint(-50, 50) for _ in range(length)]
            cases.append((f"generated_int_n{length}_s{sample}", values))
        for sample in range(4):
            values = [rng.randint(-80, 80) / 4.0 for _ in range(length)]
            cases.append((f"generated_float_n{length}_s{sample}", values))

    mismatches = 0
    for index, (name, values) in enumerate(cases):
        expected = observe(canonical, values)
        actual = observe(candidate, values)
        same = expected == actual
        if not same:
            mismatches += 1
        record = {
            "index": index,
            "name": name,
            "input": values,
            "canonical": expected,
            "candidate": actual,
            "same": same,
        }
        print(json.dumps(record, sort_keys=True))

    print(
        json.dumps(
            {
                "summary": {
                    "cases": len(cases),
                    "mismatches": mismatches,
                    "matches": len(cases) - mismatches,
                    "seed": 470047,
                }
            },
            sort_keys=True,
        )
    )
    if mismatches:
        print("RESULT FAIL: candidate diverged from trusted canonical")
        return 1
    print("RESULT PASS: no divergence")
    return 0


if __name__ == "__main__":
    sys.exit(main())
