#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval/21."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import struct
from pathlib import Path
from typing import Any, Callable


def load_function(path: str) -> Callable[[list[float]], list[float]]:
    file_path = Path(path)
    spec = importlib.util.spec_from_file_location(
        f"audit_{file_path.stem}_{abs(hash(file_path))}", file_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def float_record(value: float) -> dict[str, Any]:
    return {
        "repr": repr(value),
        "hex": value.hex(),
        "bits": struct.pack(">d", value).hex(),
    }


def outcome(function: Callable[[list[float]], list[float]], values: list[float]) -> Any:
    try:
        result = function(list(values))
    except Exception as error:
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }
    return {"kind": "return", "value": [float_record(x) for x in result]}


def same(left: Any, right: Any) -> bool:
    return left == right


def main() -> int:
    canonical = load_function("/reference/canonical.py")
    candidate = load_function("/tmp/audit-work/source/solution.py")

    named: list[tuple[str, list[float]]] = [
        ("prompt_example", [1.0, 2.0, 3.0, 4.0, 5.0]),
        ("empty", []),
        ("singleton", [1.0]),
        ("two_equal", [2.0, 2.0]),
        ("two_increasing", [-3.5, 8.25]),
        ("two_descending", [8.25, -3.5]),
        ("repeated_extrema", [-5.0, -5.0, 0.0, 5.0, 5.0]),
        ("negative", [-10.0, -2.0, -7.0]),
        ("fractional", [0.125, 0.5, 0.25, 0.375]),
        ("signed_zero", [-0.0, 0.0, 1.0]),
        ("large_finite", [-1.0e150, 0.0, 1.0e150]),
        ("tiny_normal", [1.0e-300, 2.0e-300, 4.0e-300]),
        ("positive_infinity", [0.0, 1.0, math.inf]),
        ("negative_infinity", [-math.inf, 0.0, 1.0]),
        ("nan_member", [0.0, math.nan, 1.0]),
    ]

    generator = random.Random(210021)
    generated: list[tuple[str, list[float]]] = []
    for case_index in range(200):
        length = generator.randint(2, 12)
        values = [
            generator.randint(-10000, 10000) / generator.choice((1, 2, 4, 5, 10))
            for _ in range(length)
        ]
        if case_index % 4 == 0:
            values[-1] = values[0]
        if min(values) == max(values):
            values[-1] += 1.0
        generated.append((f"generated_{case_index:03d}", values))

    records: list[dict[str, Any]] = []
    mismatch_count = 0
    for name, values in named + generated:
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        matches = same(expected, actual)
        mismatch_count += not matches
        records.append(
            {
                "name": name,
                "input": [float_record(x) for x in values],
                "canonical": expected,
                "candidate": actual,
                "match": matches,
            }
        )

    print(
        json.dumps(
            {
                "oracle": "/reference/canonical.py:rescale_to_unit",
                "candidate": "/tmp/audit-work/source/solution.py:rescale_to_unit",
                "seed": 210021,
                "named_case_count": len(named),
                "generated_case_count": len(generated),
                "mismatch_count": mismatch_count,
                "records": records,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
