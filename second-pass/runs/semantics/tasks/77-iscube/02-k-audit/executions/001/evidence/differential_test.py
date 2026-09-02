#!/usr/bin/env python3
"""Differential and exact-contract tests for HumanEval 77 (iscube)."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_iscube(value: int) -> bool:
    """Integer-only oracle: binary-search the nonnegative cube root."""
    target = abs(value)
    low, high = 0, 1
    while high**3 < target:
        high *= 2
    while low <= high:
        middle = (low + high) // 2
        cube = middle**3
        if cube == target:
            return True
        if cube < target:
            low = middle + 1
        else:
            high = middle - 1
    return False


def outcome(function: Callable[[int], bool], value: int) -> tuple[str, str]:
    try:
        result = function(value)
        return ("return", repr(result))
    except Exception as error:  # Deliberately compare observable exception behavior.
        return ("exception", f"{type(error).__name__}: {error}")


def add_case(
    cases: dict[int, set[str]], value: int, category: str
) -> None:
    cases.setdefault(value, set()).add(category)


def build_cases() -> dict[int, set[str]]:
    cases: dict[int, set[str]] = {}

    for value in [1, 2, -1, 64, 0, 180]:
        add_case(cases, value, "documented-example")

    # There is no empty value in the documented integer-only domain; zero is
    # the relevant neutral/boundary input.
    add_case(cases, 0, "zero-boundary")

    # Exercise abs's sign split and the comparison's true/false outcomes at
    # both sides of cube boundaries.
    roots = [
        0,
        1,
        2,
        3,
        4,
        5,
        10,
        99,
        100,
        999,
        1000,
        10**5,
        10**10,
        10**15,
        10**16,
        2**53,
    ]
    for root in roots:
        cube = root**3
        for delta in [-1, 0, 1]:
            if cube + delta < 0:
                continue
            magnitude = cube + delta
            add_case(cases, magnitude, "cube-adjacent-boundary")
            add_case(cases, -magnitude, "negative-cube-adjacent-boundary")

    # Explicit conversion/precision stress points, including inputs at and
    # beyond binary-float conversion range.
    for value in [
        10**307,
        10**308,
        10**309,
        (10**100) ** 3,
        (10**103) ** 3,
        -((10**100) ** 3),
        -((10**103) ** 3),
    ]:
        add_case(cases, value, "large-integer-boundary")

    generator = random.Random(770077)
    for _ in range(300):
        add_case(
            cases,
            generator.randint(-(10**18), 10**18),
            "seeded-random-integer",
        )
    for _ in range(100):
        root = generator.randint(0, 10**18)
        cube = root**3
        for sign in [1, -1]:
            add_case(cases, sign * cube, "seeded-random-exact-cube")
            add_case(cases, sign * (cube + 1), "seeded-random-near-cube")
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical")
    parser.add_argument("generated")
    parser.add_argument("inputs_json")
    arguments = parser.parse_args()

    canonical = load_module("trusted_canonical", Path(arguments.canonical))
    generated = load_module("generated_solution", Path(arguments.generated))
    cases = build_cases()

    serialized = [
        {"value": str(value), "categories": sorted(categories)}
        for value, categories in sorted(cases.items())
    ]
    Path(arguments.inputs_json).write_text(
        json.dumps(serialized, indent=2) + "\n", encoding="utf-8"
    )

    differential_mismatches: list[tuple[int, tuple[str, str], tuple[str, str]]] = []
    contract_mismatches: list[tuple[int, tuple[str, str], bool]] = []
    for value in sorted(cases):
        canonical_result = outcome(canonical.iscube, value)
        generated_result = outcome(generated.iscube, value)
        if canonical_result != generated_result:
            differential_mismatches.append(
                (value, canonical_result, generated_result)
            )
        expected = exact_iscube(value)
        if generated_result != ("return", repr(expected)):
            contract_mismatches.append((value, generated_result, expected))

    print("EMPTY_CASE: not applicable to the documented integer-only input domain")
    print(f"INPUT_COUNT: {len(cases)}")
    print("INPUT_ARTIFACT:", arguments.inputs_json)
    print(f"CANONICAL_VS_GENERATED_MISMATCHES: {len(differential_mismatches)}")
    for item in differential_mismatches[:20]:
        print("DIFF:", item)
    print(f"GENERATED_VS_EXACT_CONTRACT_MISMATCHES: {len(contract_mismatches)}")
    for item in contract_mismatches[:20]:
        print("CONTRACT_MISMATCH:", item)

    witness = (10**15) ** 3
    print("FOCUSED_WITNESS_INPUT:", witness)
    print("FOCUSED_WITNESS_EXPECTED:", exact_iscube(witness))
    print("FOCUSED_WITNESS_CANONICAL:", outcome(canonical.iscube, witness))
    print("FOCUSED_WITNESS_GENERATED:", outcome(generated.iscube, witness))
    return 0 if not differential_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
