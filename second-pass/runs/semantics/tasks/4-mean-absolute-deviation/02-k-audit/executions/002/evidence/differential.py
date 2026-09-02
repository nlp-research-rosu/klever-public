#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test."""

from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load(path: str, module_name: str) -> Callable[[list[float]], float]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def outcome(function: Callable[[list[float]], float], values: list[float]) -> dict[str, Any]:
    try:
        result = function(values)
    except Exception as error:  # differential comparison intentionally records exceptions
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}
    if math.isnan(result):
        encoded: str | float = "NaN"
    elif math.isinf(result):
        encoded = "Infinity" if result > 0 else "-Infinity"
    else:
        encoded = result
    return {"kind": "return", "value": encoded, "hex": result.hex()}


def equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["kind"] != right["kind"]:
        return False
    if left["kind"] == "exception":
        return left["type"] == right["type"]
    if left["value"] == "NaN" and right["value"] == "NaN":
        return True
    return left["hex"] == right["hex"]


def main() -> None:
    canonical = load("/reference/canonical.py", "trusted_canonical")
    candidate = load("/tmp/audit-work/candidate/solution.py", "candidate_solution")

    cases: list[tuple[str, list[float]]] = [
        ("documented_example", [1.0, 2.0, 3.0, 4.0]),
        ("empty_boundary", []),
        ("singleton_zero", [0.0]),
        ("singleton_negative", [-7.25]),
        ("two_symmetric", [-1.0, 1.0]),
        ("duplicates", [2.5, 2.5, 2.5]),
        ("mixed_sign", [-10.0, -0.5, 0.0, 3.25, 100.0]),
        ("signed_zero", [-0.0, 0.0]),
        ("rounding_boundary", [1e16, 1.0, -1e16]),
        ("subnormal", [5e-324, 0.0, -5e-324]),
        ("large_finite", [1e308, 1e308]),
        ("positive_infinity", [1.0, float("inf")]),
        ("nan_member", [1.0, float("nan")]),
    ]
    rng = random.Random(0x4D4144)
    pool = [-1000.5, -13.0, -1.25, -0.0, 0.0, 0.125, 1.0, 2.5, 99.75, 1000.5]
    for length in range(1, 9):
        for sample in range(25):
            cases.append(
                (
                    f"generated_len_{length:02d}_{sample:02d}",
                    [rng.choice(pool) for _ in range(length)],
                )
            )

    mismatches = 0
    records: list[dict[str, Any]] = []
    for name, values in cases:
        canonical_result = outcome(canonical, list(values))
        candidate_result = outcome(candidate, list(values))
        matches = equal(canonical_result, candidate_result)
        mismatches += not matches
        records.append(
            {
                "name": name,
                "input": [repr(value) for value in values],
                "canonical": canonical_result,
                "candidate": candidate_result,
                "match": matches,
            }
        )

    summary = {
        "oracle": "/reference/canonical.py",
        "candidate": "/tmp/audit-work/candidate/solution.py",
        "case_count": len(records),
        "mismatch_count": mismatches,
        "cases": records,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
