#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for HumanEval/0."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


EntryPoint = Callable[[list[float], float], bool]


@dataclass(frozen=True)
class Case:
    label: str
    numbers: tuple[float, ...]
    threshold: float


def load_entry(path: Path, module_name: str) -> EntryPoint:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "has_close_elements")
    return entry


def encoded_float(value: float) -> dict[str, str]:
    return {"repr": repr(value), "hex": value.hex()}


def build_cases() -> list[Case]:
    cases = [
        Case("prompt_false", (1.0, 2.0, 3.0), 0.5),
        Case("prompt_true", (1.0, 2.8, 3.0, 4.0, 5.0, 2.0), 0.3),
        Case("empty_outer_base", (), 0.5),
        Case("singleton_self_pair_excluded", (1.0,), 100.0),
        Case("equal_values_positive_threshold", (1.0, 1.0), 0.1),
        Case("equal_values_zero_threshold", (1.0, 1.0), 0.0),
        Case("strict_boundary_equal", (1.0, 1.5), 0.5),
        Case("strict_boundary_just_above", (1.0, 1.5), math.nextafter(0.5, math.inf)),
        Case("negative_threshold", (-2.0, -1.9, 10.0), -1.0),
        Case("signed_zero", (-0.0, 0.0), math.ulp(0.0)),
        Case("true_then_continue", (0.0, 0.01, 100.0, 200.0), 0.02),
        Case("true_on_last_ordered_pair", (100.0, 3.0, 3.01), 0.02),
        Case("infinite_threshold_finite_distance", (-1.0, 1.0), math.inf),
        Case("infinite_distance_strict_inf", (-math.inf, math.inf), math.inf),
        Case("same_positive_infinity", (math.inf, math.inf), 1.0),
        Case("nan_element", (math.nan, 0.0, 0.0), 0.1),
        Case("nan_threshold", (0.0, 0.0), math.nan),
        Case("subnormal_neighbors", (0.0, math.ulp(0.0)), math.nextafter(math.ulp(0.0), math.inf)),
    ]

    grid_values = (-2.0, -0.0, 0.5, 2.0)
    grid_thresholds = (-1.0, 0.0, 0.5, 2.0, math.inf)
    for length in range(5):
        count = len(grid_values) ** length
        for ordinal in range(count):
            cursor = ordinal
            values: list[float] = []
            for _ in range(length):
                values.append(grid_values[cursor % len(grid_values)])
                cursor //= len(grid_values)
            for threshold in grid_thresholds:
                cases.append(Case(f"grid_n{length}_{ordinal}_{threshold!r}", tuple(values), threshold))

    rng = random.Random(20260722)
    boundary_pool = (-math.inf, -100.0, -1.0, -0.0, 0.0, 1.0, 100.0, math.inf, math.nan)
    for index in range(750):
        length = rng.randrange(0, 11)
        values = []
        for _ in range(length):
            if rng.random() < 0.20:
                values.append(rng.choice(boundary_pool))
            else:
                values.append(rng.uniform(-1.0e6, 1.0e6))
        threshold = rng.choice(boundary_pool) if rng.random() < 0.20 else rng.uniform(-100.0, 1.0e6)
        cases.append(Case(f"random_{index}", tuple(values), threshold))
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--cases-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_humaneval_0_canonical")
    generated = load_entry(args.generated, "audited_generated_solution")
    cases = build_cases()

    serialized = [
        {
            "label": case.label,
            "numbers": [encoded_float(value) for value in case.numbers],
            "threshold": encoded_float(case.threshold),
        }
        for case in cases
    ]
    args.cases_out.write_text(json.dumps(serialized, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    mismatches = []
    non_bool_results = []
    true_count = 0
    false_count = 0
    for case in cases:
        numbers = list(case.numbers)
        expected = canonical(numbers, case.threshold)
        actual = generated(numbers, case.threshold)
        if type(expected) is not bool or type(actual) is not bool:
            non_bool_results.append((case.label, type(expected).__name__, type(actual).__name__))
        if expected:
            true_count += 1
        else:
            false_count += 1
        if actual != expected:
            mismatches.append((case.label, case.numbers, case.threshold, expected, actual))

    print(f"canonical={args.canonical}")
    print(f"generated={args.generated}")
    print(f"cases_file={args.cases_out}")
    print(f"case_count={len(cases)} true={true_count} false={false_count}")
    print(f"mismatch_count={len(mismatches)} non_bool_count={len(non_bool_results)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print(f"MISMATCH {mismatch!r}")
    if non_bool_results:
        for item in non_bool_results[:20]:
            print(f"NON_BOOL {item!r}")
    return 1 if mismatches or non_bool_results else 0


if __name__ == "__main__":
    raise SystemExit(main())
