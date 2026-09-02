#!/usr/bin/env python3
"""Concrete contract-valid inputs outside every operator shape claimed in spec.k."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


ALLOWED = {"+", "-", "*", "//", "**"}


def entry(path: str, name: str) -> Callable[[list[str], list[int]], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


def valid(operators: list[str], operands: list[int]) -> bool:
    return (
        len(operators) >= 1
        and len(operands) == len(operators) + 1
        and set(operators) <= ALLOWED
        and all(isinstance(value, int) and value >= 0 for value in operands)
    )


def main() -> int:
    canonical = entry("/reference/canonical.py", "coverage_canonical")
    candidate = entry("/candidate/solution.py", "coverage_candidate")
    # Human inspection of spec.k shows its only operator shapes are:
    # [+], [-], [*], [//], fixed [**], [-,-], fixed [//,//], fixed [**,**],
    # [+,*,-], and [+,*,**,//,-].
    cases = [
        {
            "reason_unclaimed": "two additions: no two-plus entry claim",
            "operators": ["+", "+"],
            "operands": [1, 2, 3],
        },
        {
            "reason_unclaimed": "single exponentiation is claimed only for base 2 exponent 5",
            "operators": ["**"],
            "operands": [3, 4],
        },
        {
            "reason_unclaimed": "valid four-operator mixed shape absent from spec.k",
            "operators": ["+", "-", "*", "//"],
            "operands": [10, 2, 3, 4, 2],
        },
        {
            "reason_unclaimed": "valid length-six operator list; every claim has length at most five",
            "operators": ["+", "*", "-", "+", "//", "*"],
            "operands": [2, 3, 4, 5, 6, 2, 7],
        },
    ]
    failures = 0
    for case in cases:
        case["contract_valid"] = valid(case["operators"], case["operands"])
        case["canonical_result"] = canonical(case["operators"], case["operands"])
        case["candidate_result"] = candidate(case["operators"], case["operands"])
        case["implementations_match"] = case["canonical_result"] == case["candidate_result"]
        failures += int(not case["contract_valid"] or not case["implementations_match"])
    output = {
        "spec_operator_shapes_from_static_inspection": [
            ["+"],
            ["-"],
            ["*"],
            ["//"],
            ["**"],
            ["-", "-"],
            ["//", "//"],
            ["**", "**"],
            ["+", "*", "-"],
            ["+", "*", "**", "//", "-"],
        ],
        "uncovered_case_count": len(cases),
        "failures": failures,
        "cases": cases,
    }
    Path("/audit-output/evidence/04_uncovered_cases.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
