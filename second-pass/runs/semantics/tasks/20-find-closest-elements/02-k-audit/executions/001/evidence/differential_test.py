#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[float]], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


def invoke(fn: Callable[[list[float]], Any], values: list[float]) -> tuple[str, Any]:
    try:
        return ("return", fn(list(values)))
    except Exception as err:  # Deliberately compares boundary exception behavior.
        return ("exception", type(err).__name__)


def scalar_equal(left: Any, right: Any) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        if math.isnan(left) and math.isnan(right):
            return True
    return left == right


def outcome_equal(left: tuple[str, Any], right: tuple[str, Any]) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "exception":
        return left[1] == right[1]
    left_value, right_value = left[1], right[1]
    if left_value is None or right_value is None:
        return left_value is right_value
    if not isinstance(left_value, tuple) or not isinstance(right_value, tuple):
        return scalar_equal(left_value, right_value)
    return len(left_value) == len(right_value) and all(
        scalar_equal(a, b) for a, b in zip(left_value, right_value)
    )


def jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        if value == 0.0 and math.copysign(1.0, value) < 0:
            return "-0.0"
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "audit_trusted_canonical")
    candidate = load_entry(args.candidate, "audit_generated_candidate")

    named: list[tuple[str, list[float], bool]] = [
        ("empty-outside-contract", [], False),
        ("singleton-outside-contract", [1.0], False),
        ("documented-example-update", [1.0, 2.0, 3.0, 4.0, 5.0, 2.2], True),
        ("documented-example-duplicate", [1.0, 2.0, 3.0, 4.0, 5.0, 2.0], True),
        ("minimum-length-no-swap", [1.0, 2.0], True),
        ("minimum-length-initial-swap", [2.0, 1.0], True),
        ("later-pair-swap-and-update", [10.0, 0.0, 9.0], True),
        ("later-pair-no-swap-and-update", [0.0, 10.0, 1.0], True),
        ("strict-tie-preserves-earlier", [0.0, 2.0, 4.0], True),
        ("negative-values", [-10.0, -2.0, -3.0, 7.0], True),
        ("fractional-values", [0.25, 0.2, -0.125, 0.3], True),
        ("signed-zero", [-0.0, 0.0, 1.0], True),
        ("positive-infinity", [1.0, math.inf, 2.0], True),
        ("negative-infinity", [-math.inf, -1.0, 0.0], True),
        ("nan-first", [math.nan, 1.0, 2.0], True),
        ("nan-later", [1.0, math.nan, 2.0], True),
    ]

    cases: list[dict[str, Any]] = []
    for name, values, intended in named:
        cases.append({"kind": "named", "name": name, "intended": intended, "values": values})

    finite_alphabet = [-3.0, -1.0, 0.0, 1.0, 3.0]
    for length in range(2, 7):
        for values in itertools.product(finite_alphabet, repeat=length):
            cases.append(
                {
                    "kind": "exhaustive",
                    "name": f"finite-alphabet-length-{length}",
                    "intended": True,
                    "values": list(values),
                }
            )

    rng = random.Random(20260724)
    for index in range(1500):
        length = rng.randint(2, 12)
        values = [
            rng.randint(-10000, 10000) / rng.choice((1.0, 2.0, 4.0, 10.0))
            for _ in range(length)
        ]
        cases.append(
            {
                "kind": "generated",
                "name": f"seed-20260724-case-{index}",
                "intended": True,
                "values": values,
            }
        )

    serializable_cases = [
        {
            "index": index,
            "kind": case["kind"],
            "name": case["name"],
            "intended": case["intended"],
            "values": jsonable(case["values"]),
        }
        for index, case in enumerate(cases)
    ]
    args.inputs_out.write_text(
        json.dumps(
            {
                "canonical": str(args.canonical),
                "candidate": str(args.candidate),
                "random_seed": 20260724,
                "finite_alphabet": finite_alphabet,
                "cases": serializable_cases,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    intended_mismatches: list[dict[str, Any]] = []
    outside_observations: list[dict[str, Any]] = []
    intended_count = 0
    for index, case in enumerate(cases):
        values = case["values"]
        expected = invoke(canonical, values)
        actual = invoke(candidate, values)
        record = {
            "index": index,
            "name": case["name"],
            "values": jsonable(values),
            "canonical": jsonable(expected),
            "candidate": jsonable(actual),
        }
        if case["intended"]:
            intended_count += 1
            if not outcome_equal(expected, actual):
                intended_mismatches.append(record)
        else:
            outside_observations.append(record)

    print(f"total_cases={len(cases)}")
    print(f"intended_domain_cases={intended_count}")
    print(f"intended_domain_mismatches={len(intended_mismatches)}")
    print(f"outside_contract_cases={len(outside_observations)}")
    print("outside_contract_observations=" + json.dumps(outside_observations, sort_keys=True))
    print("intended_mismatches=" + json.dumps(intended_mismatches[:20], sort_keys=True))
    print(f"complete_inputs={args.inputs_out}")
    return 1 if intended_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
