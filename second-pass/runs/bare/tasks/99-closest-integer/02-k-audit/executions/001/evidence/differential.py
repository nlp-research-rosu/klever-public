#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 99."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import random
from typing import Any, Callable


def load_function(module_name: str, path: Path) -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


CANONICAL = load_function(
    "trusted_canonical", Path("/tmp/audit-work/99-closest-integer/trusted/canonical.py")
)
CANDIDATE = load_function(
    "generated_solution", Path("/tmp/audit-work/99-closest-integer/source/solution.py")
)


def outcome(function: Callable[[str], int], value: str) -> dict[str, Any]:
    try:
        result = function(value)
        return {"kind": "return", "type": type(result).__name__, "value": result}
    except Exception as error:  # The empty/invalid boundary is intentionally observed.
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "message": str(error),
        }


def generated_inputs() -> list[str]:
    rng = random.Random(990099)
    values: list[str] = []
    for _ in range(80):
        sign = "-" if rng.randrange(2) else ""
        integer = rng.randrange(0, 101)
        digits = rng.randrange(0, 7)
        if digits == 0:
            values.append(f"{sign}{integer}")
        else:
            scale = 10**digits
            fraction = rng.randrange(scale)
            values.append(f"{sign}{integer}.{fraction:0{digits}d}")
    return values


CASES: list[tuple[str, str]] = [
    ("example", "10"),
    ("example", "15.3"),
    ("example", "14.5"),
    ("example", "-14.5"),
    ("empty", ""),
    ("sign-boundary", "-0"),
    ("sign-boundary", "-0.0"),
    ("sign-boundary", "0"),
    ("sign-boundary", "+0.0"),
    ("half-boundary", "-1.5001"),
    ("half-boundary", "-1.5"),
    ("half-boundary", "-1.4999"),
    ("half-boundary", "-0.5001"),
    ("half-boundary", "-0.5"),
    ("half-boundary", "-0.4999"),
    ("half-boundary", "0.4999"),
    ("half-boundary", "0.5"),
    ("half-boundary", "0.5001"),
    ("half-boundary", "1.4999"),
    ("half-boundary", "1.5"),
    ("half-boundary", "1.5001"),
    ("format-boundary", ".5"),
    ("format-boundary", "-.5"),
    ("format-boundary", "14.5000"),
    ("format-boundary", "-14.5000"),
    ("format-boundary", "1e2"),
    ("format-boundary", "1.5e2"),
    ("format-boundary", "1.45e1"),
    ("precision-boundary", "1.499999999999999999999999"),
    ("precision-boundary", "1.500000000000000000000001"),
    ("precision-boundary", "-1.499999999999999999999999"),
    ("precision-boundary", "-1.500000000000000000000001"),
    ("decimal-context-boundary", "9999999999999999999999999999.4"),
    ("decimal-context-boundary", "-9999999999999999999999999999.4"),
]
CASES.extend(("generated", value) for value in generated_inputs())


def main() -> None:
    mismatch_count = 0
    same_return_count = 0
    same_exception_type_count = 0
    for index, (category, value) in enumerate(CASES, 1):
        canonical = outcome(CANONICAL, value)
        candidate = outcome(CANDIDATE, value)
        same = canonical == candidate
        if same:
            if canonical["kind"] == "return":
                same_return_count += 1
            else:
                same_exception_type_count += 1
        else:
            mismatch_count += 1
        print(
            json.dumps(
                {
                    "index": index,
                    "category": category,
                    "input": value,
                    "canonical": canonical,
                    "candidate": candidate,
                    "same": same,
                },
                sort_keys=True,
            )
        )
    print(
        "SUMMARY "
        + json.dumps(
            {
                "total": len(CASES),
                "same_returns": same_return_count,
                "same_exceptions": same_exception_type_count,
                "mismatches": mismatch_count,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
