#!/usr/bin/env python3
"""Independent finite differential test for HumanEval problem 42."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observe(function: Callable[[list[int]], list[int]], values: list[int]) -> dict[str, Any]:
    argument = list(values)
    before = list(argument)
    try:
        result = function(argument)
        return {
            "kind": "return",
            "result": result,
            "result_type": type(result).__name__,
            "input_after": argument,
            "input_unchanged": argument == before,
            "distinct_result": result is not argument,
        }
    except Exception as error:  # pragma: no cover - retained to compare exceptions
        return {
            "kind": "raise",
            "exception_type": type(error).__name__,
            "exception_text": str(error),
            "input_after": argument,
            "input_unchanged": argument == before,
        }


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py TRUSTED_CANONICAL GENERATED_SOLUTION", file=sys.stderr)
        return 64

    canonical_path = Path(sys.argv[1]).resolve()
    generated_path = Path(sys.argv[2]).resolve()
    canonical = load_module("trusted_canonical_42", canonical_path)
    generated = load_module("generated_solution_42", generated_path)

    documented = [
        [1, 2, 3],
        [5, 3, 5, 2, 3, 3, 9, 0, 123],
    ]
    boundary = [
        [],
        [0],
        [-1],
        [1],
        [0, 0],
        [-2, -1, 0, 1, 2],
        [-(2**63), 2**63 - 1],
        [-(10**100), 0, 10**100],
    ]

    rng = random.Random(420042)
    representative: list[list[int]] = []
    value_pool = [
        -(10**50),
        -(2**63),
        -1000,
        -2,
        -1,
        0,
        1,
        2,
        1000,
        2**63 - 1,
        10**50,
    ]
    for case_index in range(256):
        length = case_index % 17
        representative.append(
            [
                rng.choice(value_pool)
                if rng.randrange(4) == 0
                else rng.randint(-1_000_000, 1_000_000)
                for _ in range(length)
            ]
        )

    cases = documented + boundary + representative
    encoded_inputs = json.dumps(cases, separators=(",", ":"), ensure_ascii=True)
    print(f"CANONICAL_PATH={canonical_path}")
    print(f"GENERATED_PATH={generated_path}")
    print("DOMAIN=list[int]")
    print(f"DOCUMENTED_CASES={len(documented)}")
    print(f"BOUNDARY_CASES={len(boundary)}")
    print(f"REPRESENTATIVE_CASES={len(representative)}")
    print(f"TOTAL_CASES={len(cases)}")
    print("RANDOM_SEED=420042")
    print(f"INPUTS_SHA256={hashlib.sha256(encoded_inputs.encode()).hexdigest()}")
    print(f"INPUTS_JSON={encoded_inputs}")

    mismatches: list[dict[str, Any]] = []
    for index, values in enumerate(cases):
        expected = observe(canonical.incr_list, values)
        actual = observe(generated.incr_list, values)
        if actual != expected:
            mismatches.append(
                {"index": index, "input": values, "canonical": expected, "generated": actual}
            )

    print(f"MISMATCH_COUNT={len(mismatches)}")
    if mismatches:
        print(f"MISMATCHES_JSON={json.dumps(mismatches, separators=(',', ':'))}")
        return 1
    print("DIFFERENTIAL_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
