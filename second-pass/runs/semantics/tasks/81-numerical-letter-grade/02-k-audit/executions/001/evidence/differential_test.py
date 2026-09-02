#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval problem 81."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[float | int]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


def outcome(function: Callable[[list[float | int]], list[str]], values: list[float | int]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(values)}
    except Exception as error:  # Record divergences in failure behavior as well as values.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def build_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = [
        {"name": "documented-example", "values": [4.0, 3, 1.7, 2, 3.5]},
        {"name": "empty", "values": []},
        {"name": "integer-boundaries", "values": [0, 1, 2, 3, 4]},
    ]

    thresholds = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
    boundary_values: list[float] = []
    for threshold in thresholds:
        boundary_values.extend(
            [
                math.nextafter(threshold, -math.inf),
                threshold,
                math.nextafter(threshold, math.inf),
            ]
        )
    cases.append({"name": "all-branch-boundaries-nextafter", "values": boundary_values})
    cases.append({"name": "range-edges", "values": [-1.0, -0.1, 0.0, 4.0, 4.1, 5.0]})

    generator = random.Random(810081)
    for index, length in enumerate([1, 2, 5, 16, 64, 257]):
        values = [generator.uniform(0.0, 4.0) for _ in range(length)]
        cases.append({"name": f"generated-{index}-length-{length}", "values": values})
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical_81")
    candidate = load_entry(args.candidate, "candidate_solution_81")
    cases = build_cases()
    args.inputs_out.write_text(
        json.dumps(cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    mismatches: list[dict[str, Any]] = []
    scalar_count = 0
    for case in cases:
        scalar_count += len(case["values"])
        expected = outcome(canonical, list(case["values"]))
        actual = outcome(candidate, list(case["values"]))
        if actual != expected:
            mismatches.append(
                {
                    "name": case["name"],
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    input_bytes = args.inputs_out.read_bytes()
    print(f"canonical={args.canonical}")
    print(f"candidate={args.candidate}")
    print("generator_seed=810081")
    print("generated_uniform_domain=[0.0,4.0]")
    print(f"case_count={len(cases)}")
    print(f"scalar_input_count={scalar_count}")
    print(f"inputs_sha256={hashlib.sha256(input_bytes).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches:
        print(json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
