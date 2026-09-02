#!/usr/bin/env python3
"""Independent differential tests for trusted canonical.py vs solution.py."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import signal
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


CANONICAL_PATH = Path("/tmp/audit-work/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CallTimeout(Exception):
    pass


def alarm_handler(signum: int, frame: Any) -> None:
    del signum, frame
    raise CallTimeout("one-second per-call timeout")


def observe(function: Callable[[list], Any], xs: list) -> dict[str, Any]:
    signal.setitimer(signal.ITIMER_REAL, 1.0)
    try:
        value = function(xs.copy())
        if isinstance(value, float):
            value_repr = value.hex()
        else:
            value_repr = repr(value)
        return {
            "status": "return",
            "type": type(value).__name__,
            "repr": repr(value),
            "float_hex": value_repr,
            "numeric_value": value if isinstance(value, (int, float)) else None,
        }
    except Exception as error:  # Intentionally compare exception behavior too.
        return {
            "status": "exception",
            "type": type(error).__name__,
            "repr": repr(error),
        }
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)


def valid_polynomial(xs: list[int | float]) -> bool:
    return len(xs) % 2 == 0 and len(xs) > 0 and xs[-1] != 0


def build_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = [
        {"name": "prompt-linear", "xs": [1, 2], "class": "documented"},
        {
            "name": "prompt-cubic",
            "xs": [-6, 11, -6, 1],
            "class": "documented",
        },
        {"name": "empty-list", "xs": [], "class": "invalid-boundary"},
        {"name": "all-zero-pair", "xs": [0, 0], "class": "invalid-boundary"},
        {
            "name": "zero-leading-cubic-slot",
            "xs": [1, -1, 0, 0],
            "class": "invalid-boundary",
        },
        {"name": "root-at-minus-one", "xs": [1, 1], "class": "branch-boundary"},
        {"name": "root-at-plus-one", "xs": [-1, 1], "class": "branch-boundary"},
        {"name": "root-at-zero", "xs": [0, 1], "class": "branch-boundary"},
        {
            "name": "root-just-left-zero",
            "xs": [1e-10, 1.0],
            "class": "tolerance-boundary",
        },
        {
            "name": "root-just-right-zero",
            "xs": [-1e-10, 1.0],
            "class": "tolerance-boundary",
        },
        {"name": "one-expansion", "xs": [3, 2], "class": "expansion-boundary"},
        {
            "name": "many-expansions",
            "xs": [2**40, 1],
            "class": "expansion-boundary",
        },
        {
            "name": "small-float-slope",
            "xs": [0.125, -0.25],
            "class": "numeric-boundary",
        },
        {
            "name": "degree-five",
            "xs": [3, -5, 2, 0, -1, 1],
            "class": "degree-boundary",
        },
    ]
    rng = random.Random(320032)
    for degree in (1, 3, 5):
        for index in range(30):
            coefficients = [rng.randint(-7, 7) for _ in range(degree)]
            leading = 0
            while leading == 0:
                leading = rng.randint(-7, 7)
            coefficients.append(leading)
            cases.append(
                {
                    "name": f"generated-int-degree-{degree}-{index:02d}",
                    "xs": coefficients,
                    "class": "generated-valid-int",
                }
            )
    for index in range(20):
        coefficients = [rng.uniform(-3.0, 3.0) for _ in range(3)]
        leading = 0.0
        while abs(leading) < 0.25:
            leading = rng.uniform(-3.0, 3.0)
        coefficients.append(leading)
        cases.append(
            {
                "name": f"generated-float-degree-3-{index:02d}",
                "xs": coefficients,
                "class": "generated-valid-float",
            }
        )
    return cases


def material_match(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["status"] != right["status"]:
        return False
    if left["status"] == "exception":
        return left["type"] == right["type"] and left["repr"] == right["repr"]
    left_number = left.get("numeric_value")
    right_number = right.get("numeric_value")
    if left_number is not None and right_number is not None:
        if isinstance(left_number, float) and math.isnan(left_number):
            return isinstance(right_number, float) and math.isnan(right_number)
        return left_number == right_number
    return left["type"] == right["type"] and left["repr"] == right["repr"]


def main() -> int:
    canonical = load_module("trusted_canonical_32", CANONICAL_PATH)
    generated = load_module("candidate_generated_32", GENERATED_PATH)
    signal.signal(signal.SIGALRM, alarm_handler)
    cases = build_cases()
    exact_observation_differences = 0
    material_mismatches = 0
    valid_cases = 0
    results: list[dict[str, Any]] = []
    for case in cases:
        xs = case["xs"]
        is_valid = valid_polynomial(xs)
        valid_cases += int(is_valid)
        expected = observe(canonical.find_zero, xs)
        actual = observe(generated.find_zero, xs)
        exact_match = expected == actual
        matches = material_match(expected, actual)
        exact_observation_differences += int(not exact_match)
        material_mismatches += int(not matches)
        results.append(
            {
                **case,
                "source_contract_valid": is_valid,
                "canonical": expected,
                "candidate": actual,
                "exact_observation_match": exact_match,
                "material_numeric_match": matches,
            }
        )
    print(
        json.dumps(
            {
                "oracle": str(CANONICAL_PATH),
                "candidate": str(GENERATED_PATH),
                "seed": 320032,
                "case_count": len(cases),
                "source_contract_valid_cases": valid_cases,
                "invalid_boundary_cases": len(cases) - valid_cases,
                "exact_observation_differences": exact_observation_differences,
                "material_mismatches": material_mismatches,
                "cases": results,
            },
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )
    return 0 if material_mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
