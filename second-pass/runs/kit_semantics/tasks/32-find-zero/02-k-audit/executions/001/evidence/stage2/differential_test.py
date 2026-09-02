#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval/32."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
from pathlib import Path
from types import ModuleType
from typing import Any


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Any, coefficients: list[int | float]) -> dict[str, Any]:
    try:
        value = function(list(coefficients))
        return {"kind": "value", "value": value}
    except Exception as error:  # Boundary behavior is part of the record.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def direct_poly(coefficients: list[int | float], x: float) -> float:
    return sum(float(coefficient) * (x**index) for index, coefficient in enumerate(coefficients))


def branch_profile(coefficients: list[int | float]) -> dict[str, Any]:
    """Independent direct-power rendering of the source control decisions."""
    begin = -1.0
    end = 1.0
    expand_true = 0
    while direct_poly(coefficients, begin) * direct_poly(coefficients, end) > 0.0:
        expand_true += 1
        begin *= 2.0
        end *= 2.0
        if expand_true > 2048:
            raise RuntimeError("unexpected expansion bound exceeded")

    bisect_begin = 0
    bisect_end = 0
    iterations = 0
    while end - begin > 1e-10:
        center = (begin + end) / 2.0
        if direct_poly(coefficients, center) * direct_poly(coefficients, begin) > 0.0:
            begin = center
            bisect_begin += 1
        else:
            end = center
            bisect_end += 1
        iterations += 1
        if iterations > 4096:
            raise RuntimeError("unexpected bisection bound exceeded")
    return {
        "expand_true": expand_true,
        "expand_false_exit": 1,
        "bisect_begin_branch": bisect_begin,
        "bisect_end_branch": bisect_end,
        "direct_result": begin,
    }


def valid_contract_input(coefficients: list[int | float]) -> bool:
    return (
        len(coefficients) >= 2
        and len(coefficients) % 2 == 0
        and coefficients[-1] != 0
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("audit_canonical", args.canonical)
    candidate = load_module("audit_candidate", args.candidate)

    documented_and_boundaries: list[tuple[str, list[int | float]]] = [
        ("prompt-linear", [1, 2]),
        ("prompt-cubic", [-6, 11, -6, 1]),
        ("minimal-root-zero", [0, 1]),
        ("root-at-left-endpoint", [1, 1]),
        ("root-at-right-endpoint", [-1, 1]),
        ("expansion-required", [10, 0, 0, 1]),
        ("both-bisection-branches", [-2.0, -1.0, 0.5, 1.0]),
        ("mixed-int-float", [3, -2.5, 1, 0.25]),
        ("small-leading-nonzero", [1.0, 0.0, 0.0, 1e-6]),
        ("six-coefficients", [2, -3, 1, 4, -2, 1]),
    ]

    random_generator = random.Random(3200729)
    generated: list[tuple[str, list[int | float]]] = []
    for index in range(200):
        size = random_generator.choice((2, 4, 6, 8, 10, 12))
        coefficients: list[int | float] = []
        for _ in range(size):
            if random_generator.random() < 0.5:
                coefficients.append(random_generator.randint(-8, 8))
            else:
                coefficients.append(round(random_generator.uniform(-8.0, 8.0), 5))
        if coefficients[-1] == 0:
            coefficients[-1] = random_generator.choice((-1, 1))
        generated.append((f"generated-{index:03d}", coefficients))

    mismatches: list[dict[str, Any]] = []
    coverage = {
        "expand_true": 0,
        "expand_false_exit": 0,
        "bisect_begin_branch": 0,
        "bisect_end_branch": 0,
    }
    all_cases = documented_and_boundaries + generated
    for label, coefficients in all_cases:
        assert valid_contract_input(coefficients), (label, coefficients)
        canonical_outcome = outcome(canonical.find_zero, coefficients)
        candidate_outcome = outcome(candidate.find_zero, coefficients)
        profile = branch_profile(coefficients)
        for key in coverage:
            coverage[key] += int(profile[key])

        case_record = {
            "label": label,
            "coefficients": coefficients,
            "canonical": canonical_outcome,
            "candidate": candidate_outcome,
            "branches": profile,
        }
        matches = (
            canonical_outcome["kind"] == "value"
            and candidate_outcome["kind"] == "value"
            and math.isclose(
                canonical_outcome["value"],
                candidate_outcome["value"],
                rel_tol=1e-9,
                abs_tol=1e-8,
            )
        )
        if not matches:
            mismatches.append(case_record)
        print(json.dumps(case_record, sort_keys=True))

    # Explicitly inspect the empty-list boundary even though it violates the
    # stated "largest coefficient nonzero" precondition.
    empty_record = {
        "label": "empty-outside-contract",
        "coefficients": [],
        "canonical": outcome(canonical.find_zero, []),
        "candidate": outcome(candidate.find_zero, []),
        "contract_input": valid_contract_input([]),
    }
    print(json.dumps(empty_record, sort_keys=True))

    summary = {
        "intended_domain_cases": len(all_cases),
        "documented_and_boundary_cases": len(documented_and_boundaries),
        "generated_cases": len(generated),
        "mismatches": len(mismatches),
        "branch_coverage_counts": coverage,
        "empty_boundary": empty_record,
    }
    print("SUMMARY " + json.dumps(summary, sort_keys=True))

    required_coverage = (
        coverage["expand_true"] > 0
        and coverage["expand_false_exit"] > 0
        and coverage["bisect_begin_branch"] > 0
        and coverage["bisect_end_branch"] > 0
    )
    return 0 if not mismatches and required_coverage else 1


if __name__ == "__main__":
    raise SystemExit(main())
