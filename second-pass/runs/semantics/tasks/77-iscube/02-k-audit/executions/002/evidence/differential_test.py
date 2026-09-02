#!/usr/bin/env python3
"""Differential and mathematical-contract tests for HumanEval/77."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential_inputs.json")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.iscube


def observe(function, value: int):
    try:
        result = function(value)
        return {"kind": "return", "type": type(result).__name__, "value": result}
    except Exception as err:  # The exception itself is observable program behavior.
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def mathematical_iscube(value: int) -> bool:
    magnitude = abs(value)
    low, high = 0, 1
    while high**3 < magnitude:
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**3 < magnitude:
            low = middle
        else:
            high = middle
    return low**3 == magnitude or high**3 == magnitude


def build_inputs() -> tuple[list[int], dict[str, int]]:
    ordered: list[int] = []
    seen: set[int] = set()
    categories: dict[str, int] = {}

    def add(category: str, values):
        before = len(ordered)
        for value in values:
            value = int(value)
            if value not in seen:
                seen.add(value)
                ordered.append(value)
        categories[category] = len(ordered) - before

    add("documented_examples", [1, 2, -1, 64, 0, 180])
    add("dense_small_range", range(-4096, 4097))

    cube_boundaries = []
    for root in range(0, 513):
        cube = root**3
        for delta in (-1, 0, 1):
            value = cube + delta
            if value >= 0:
                cube_boundaries.extend((value, -value))
    add("cube_branch_boundaries", cube_boundaries)

    rng = random.Random(770077)
    add(
        "fixed_seed_random_30_digit",
        (rng.randrange(-(10**30), 10**30 + 1) for _ in range(2000)),
    )

    decimal_roots = []
    for exponent in range(1, 111):
        root = 10**exponent
        cube = root**3
        decimal_roots.extend(
            [
                cube,
                -cube,
                cube - 1,
                cube + 1,
                -(cube - 1),
                -(cube + 1),
            ]
        )
    add("large_decimal_cube_boundaries", decimal_roots)

    binary_roots = []
    for exponent in range(0, 361, 7):
        root = 2**exponent
        cube = root**3
        binary_roots.extend([cube, -cube, cube - 1, cube + 1])
    add("large_binary_cube_boundaries", binary_roots)

    return ordered, categories


def main() -> int:
    canonical = load_entry("trusted_canonical", CANONICAL_PATH)
    generated = load_entry("candidate_solution", GENERATED_PATH)
    inputs, categories = build_inputs()
    INPUTS_PATH.write_text(json.dumps(inputs, separators=(",", ":")) + "\n")

    differential_mismatches = []
    canonical_contract_mismatches = []
    generated_contract_mismatches = []
    canonical_exception_examples = []
    generated_exception_examples = []
    canonical_exceptions = 0
    generated_exceptions = 0
    for value in inputs:
        expected = mathematical_iscube(value)
        canonical_observation = observe(canonical, value)
        generated_observation = observe(generated, value)
        if canonical_observation["kind"] == "raise":
            canonical_exceptions += 1
            if len(canonical_exception_examples) < 10:
                canonical_exception_examples.append([value, canonical_observation])
        if generated_observation["kind"] == "raise":
            generated_exceptions += 1
            if len(generated_exception_examples) < 10:
                generated_exception_examples.append([value, generated_observation])
        if canonical_observation != generated_observation:
            differential_mismatches.append(
                [value, canonical_observation, generated_observation]
            )
        expected_observation = {
            "kind": "return",
            "type": "bool",
            "value": expected,
        }
        if canonical_observation != expected_observation:
            canonical_contract_mismatches.append(
                [value, expected_observation, canonical_observation]
            )
        if generated_observation != expected_observation:
            generated_contract_mismatches.append(
                [value, expected_observation, generated_observation]
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print(f"inputs_file={INPUTS_PATH}")
    print(f"categories={json.dumps(categories, sort_keys=True)}")
    print(f"total_unique_inputs={len(inputs)}")
    print(f"differential_mismatch_count={len(differential_mismatches)}")
    print(f"canonical_exception_count={canonical_exceptions}")
    print(f"generated_exception_count={generated_exceptions}")
    print(f"canonical_contract_mismatch_count={len(canonical_contract_mismatches)}")
    print(f"generated_contract_mismatch_count={len(generated_contract_mismatches)}")
    print(
        "first_canonical_exception_examples="
        + json.dumps(canonical_exception_examples, sort_keys=True)
    )
    print(
        "first_generated_exception_examples="
        + json.dumps(generated_exception_examples, sort_keys=True)
    )
    print(
        "first_differential_mismatches="
        + json.dumps(differential_mismatches[:20], sort_keys=True)
    )
    print(
        "first_canonical_contract_mismatches="
        + json.dumps(canonical_contract_mismatches[:20], sort_keys=True)
    )
    print(
        "first_generated_contract_mismatches="
        + json.dumps(generated_contract_mismatches[:20], sort_keys=True)
    )
    return 1 if differential_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
