#!/usr/bin/env python3
"""Exhibit concrete satisfying witnesses for all seven candidate claims."""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Callable


def load(path: str, module_name: str) -> Callable[[list[float]], list[float]]:
    file_path = Path(path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


canonical = load("/reference/canonical.py", "audit_canonical_witness")
candidate = load("/tmp/audit-work/source/solution.py", "audit_candidate_witness")

witnesses = [
    {
        "claim": "c1",
        "bindings": {},
        "input": [1, 2, 3, 4, 5],
        "claimed": [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)],
        "precondition": True,
    },
    {
        "claim": "c2",
        "bindings": {},
        "input": [-5, 0, 5, 5],
        "claimed": [Fraction(0), Fraction(1, 2), Fraction(1), Fraction(1)],
        "precondition": True,
    },
    {
        "claim": "c3",
        "bindings": {"A": 0, "B": 2},
        "input": [0, 2],
        "claimed": [Fraction(0), Fraction(1)],
        "precondition": 0 < 2,
    },
    {
        "claim": "c4",
        "bindings": {"A": 0, "B": 1, "C": 2},
        "input": [0, 1, 2],
        "claimed": [Fraction(0), Fraction(1, 2), Fraction(1)],
        "precondition": 0 < 1 < 2,
    },
    {
        "claim": "c5",
        "bindings": {"A": 0, "B": 1, "C": 2},
        "input": [0, 1, 2],
        "claimed": [Fraction(0), Fraction(1, 2), Fraction(1)],
        "precondition": 0 < 1 < 2 and 0 != 2,
    },
    {
        "claim": "c6",
        "bindings": {"A": 0, "B": 1, "C": 2},
        "input": [2, 1, 0],
        "claimed": [Fraction(1), Fraction(1, 2), Fraction(0)],
        "precondition": 0 < 1 < 2,
    },
    {
        "claim": "c7",
        "bindings": {"A": 0, "B": 2},
        "input": [0, 0, 2, 2],
        "claimed": [Fraction(0), Fraction(0), Fraction(1), Fraction(1)],
        "precondition": 0 < 2,
    },
]

records = []
failures = 0
for witness in witnesses:
    values = [float(value) for value in witness["input"]]
    expected = [float(value) for value in witness["claimed"]]
    candidate_result = candidate(values)
    canonical_result = canonical(values)
    accepted = bool(
        witness["precondition"]
        and candidate_result == expected
        and canonical_result == expected
    )
    failures += not accepted
    records.append(
        {
            "claim": witness["claim"],
            "bindings": witness["bindings"],
            "initial_cells": {
                "k": f"verify(solutionProgram, vlist({witness['input']}))",
                "functions": ".Map",
                "env": ".Map",
                "result": "noResult",
            },
            "precondition_satisfied": bool(witness["precondition"]),
            "claimed_exact_rationals": [str(value) for value in witness["claimed"]],
            "candidate_python": candidate_result,
            "canonical_python": canonical_result,
            "accepted": accepted,
        }
    )

print(json.dumps({"failure_count": failures, "witnesses": records}, indent=2))
raise SystemExit(1 if failures else 0)
