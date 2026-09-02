#!/usr/bin/env python3
"""Independent differential test for trusted and generated Python entry points."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/30-get-positive/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


def value_equal(left: Any, right: Any) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        if math.isnan(left) and math.isnan(right):
            return True
    return type(left) is type(right) and left == right


def list_equal(left: list[Any], right: list[Any]) -> bool:
    return len(left) == len(right) and all(
        value_equal(a, b) for a, b in zip(left, right)
    )


def run_one(
    canonical: Callable[[list[Any]], list[Any]],
    generated: Callable[[list[Any]], list[Any]],
    values: list[Any],
) -> tuple[list[Any], list[Any]]:
    canonical_input = list(values)
    generated_input = list(values)
    canonical_result = canonical(canonical_input)
    generated_result = generated(generated_input)
    if not list_equal(canonical_result, generated_result):
        raise AssertionError(
            f"mismatch input={values!r}: "
            f"canonical={canonical_result!r}, generated={generated_result!r}"
        )
    if not list_equal(canonical_input, values):
        raise AssertionError(f"canonical mutated its input: {values!r}")
    if not list_equal(generated_input, values):
        raise AssertionError(f"generated function mutated its input: {values!r}")
    return canonical_result, generated_result


def stable_case(case: list[Any]) -> list[str]:
    return [repr(value) for value in case]


def main() -> None:
    canonical = load_entry(CANONICAL, "trusted_canonical_get_positive")
    generated = load_entry(GENERATED, "generated_get_positive")

    named_cases: list[tuple[str, list[Any]]] = [
        ("documented-example-1", [-1, 2, -4, 5, 6]),
        (
            "documented-example-2",
            [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
        ),
        ("empty", []),
        ("negative-boundary", [-1]),
        ("zero-boundary", [0]),
        ("positive-boundary", [1]),
        ("all-nonpositive", [-4, -3, -2, -1, 0]),
        ("all-positive", [1, 2, 3, 4]),
        ("alternating-branches", [1, 0, -1, 2, -2, 3]),
        ("formal-ground-witness", [-2, 0, 3, 5]),
        ("duplicates-order", [2, 2, -1, 2, 0, 2]),
        ("unbounded-integers", [-(10**100), -1, 0, 1, 10**100]),
        (
            "float-boundaries",
            [
                float("-inf"),
                -1.5,
                -0.0,
                0.0,
                math.nextafter(0.0, 1.0),
                1.5,
                float("inf"),
            ],
        ),
        ("mixed-int-float", [-2, -0.5, 0, 0.5, 2]),
        ("booleans-as-python-numbers", [False, True, -1, 0, 1]),
    ]

    case_fingerprint = hashlib.sha256()
    checked = 0
    for name, case in named_cases:
        canonical_result, _ = run_one(canonical, generated, case)
        serialized = json.dumps(
            stable_case(case), ensure_ascii=False, separators=(",", ":")
        ).encode()
        case_fingerprint.update(serialized)
        checked += 1
        print(f"NAMED {name} input={case!r} output={canonical_result!r}")

    # Exhaust every list of length 0 through 6 over the three branch-boundary
    # representatives -1, 0, and 1.
    frontier: list[list[int]] = [[]]
    for length in range(7):
        if length:
            frontier = [
                prefix + [value]
                for prefix in frontier
                for value in (-1, 0, 1)
            ]
        for case in frontier:
            run_one(canonical, generated, case)
            case_fingerprint.update(
                json.dumps(case, separators=(",", ":")).encode()
            )
            checked += 1

    # Deterministic broader integer and finite-float sampling.
    rng = random.Random(30030)
    pool: tuple[int | float, ...] = (
        -(10**30),
        -1000,
        -2,
        -1,
        -0.5,
        -0.0,
        0,
        math.nextafter(0.0, 1.0),
        0.5,
        1,
        2,
        1000,
        10**30,
    )
    for _ in range(1000):
        case = [rng.choice(pool) for _ in range(rng.randrange(0, 31))]
        run_one(canonical, generated, case)
        case_fingerprint.update(
            json.dumps(stable_case(case), separators=(",", ":")).encode()
        )
        checked += 1

    print("EXHAUSTIVE_SCOPE lengths=0..6 alphabet=(-1,0,1)")
    print("RANDOM_SCOPE seed=30030 cases=1000 lengths=0..30")
    print(f"TOTAL_CASES {checked}")
    print(f"INPUT_CORPUS_SHA256 {case_fingerprint.hexdigest()}")
    print("MISMATCHES 0")


if __name__ == "__main__":
    main()
