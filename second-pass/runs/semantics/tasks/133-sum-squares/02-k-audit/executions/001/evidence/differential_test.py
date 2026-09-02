#!/usr/bin/env python3
"""Independent deterministic differential test for HumanEval 133."""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import random
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Callable[[list[int | float]], Any], values: list[int | float]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(list(values))}
    except Exception as error:  # Exception parity is recorded for non-finite cases.
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


def printable(values: list[int | float]) -> list[str]:
    return [repr(value) for value in values]


def main() -> int:
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_module(
        "candidate_solution",
        Path("/tmp/audit-work/133-sum-squares-audit/solution.py"),
    )

    documented = [
        [1, 2, 3],
        [1, 4, 9],
        [1, 3, 5, 7],
        [1.4, 4.2, 0],
        [-2.4, 1, 1],
    ]
    boundaries = [
        [],
        [0],
        [-0.0],
        [-1],
        [-1.000000001],
        [-0.999999999],
        [0.000000001],
        [0.999999999],
        [1.0],
        [1.000000001],
        [-2.4],
        [10**30, -(10**30)],
        [2.5, -2.5, 0],
        [True, False],
        [float("nan")],
        [float("inf")],
        [float("-inf")],
    ]

    atom_pool: list[int | float] = [
        -3,
        -2.000000001,
        -2,
        -1.2,
        -0.000000001,
        0,
        0.000000001,
        1,
        1.999999999,
    ]
    exhaustive = [
        list(values)
        for length in range(4)
        for values in itertools.product(atom_pool, repeat=length)
    ]

    rng = random.Random(133)
    random_cases: list[list[int | float]] = []
    for _ in range(200):
        length = rng.randrange(0, 9)
        case: list[int | float] = []
        for _ in range(length):
            if rng.randrange(2):
                case.append(rng.randint(-1000, 1000))
            else:
                integer = rng.randint(-1000, 1000)
                fraction = rng.choice([0.0, 0.000001, 0.1, 0.5, 0.999999])
                case.append(integer + fraction)
        random_cases.append(case)

    groups = (
        ("documented", documented),
        ("boundary", boundaries),
        ("exhaustive-length-0-to-3", exhaustive),
        ("seeded-random-133", random_cases),
    )
    mismatches = 0
    total = 0
    for group, cases in groups:
        for index, values in enumerate(cases):
            expected = outcome(canonical.sum_squares, values)
            actual = outcome(generated.sum_squares, values)
            equal = expected == actual
            total += 1
            mismatches += int(not equal)
            print(
                json.dumps(
                    {
                        "group": group,
                        "index": index,
                        "input_repr": printable(values),
                        "canonical": expected,
                        "generated": actual,
                        "match": equal,
                    },
                    allow_nan=False,
                    sort_keys=True,
                )
            )

    print(
        json.dumps(
            {
                "summary": {
                    "documented": len(documented),
                    "boundary": len(boundaries),
                    "exhaustive": len(exhaustive),
                    "random": len(random_cases),
                    "total": total,
                    "mismatches": mismatches,
                    "random_seed": 133,
                }
            },
            sort_keys=True,
        )
    )
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
