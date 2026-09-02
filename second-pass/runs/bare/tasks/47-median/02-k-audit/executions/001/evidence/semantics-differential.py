#!/usr/bin/env python3
"""Compare freshly rebuilt K execution with independent CPython execution."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/47-median/candidate-src/solution.py")
PROGRAM = Path("/tmp/audit-work/47-median/candidate-src/solution.mpy")
DEFINITION = Path("/tmp/audit-work/47-median/build/concrete-kompiled")

CASES = [
    ("odd-normal", [3, 1, 2]),
    ("even-normal", [1, 2, 3, 4]),
    ("prompt-odd", [3, 1, 2, 4, 5]),
    ("prompt-even", [-10, 4, 6, 1000, 10, 20]),
    ("empty-boundary", []),
    ("length-1-boundary", [7]),
    ("length-2-boundary", [1, 2]),
    ("rounding-witness", [0, 1, 2**54, 2**54 + 1]),
    ("overflow-witness", [10**400, 10**400, 10**400, 10**400]),
]


def load_candidate():
    spec = importlib.util.spec_from_file_location("stage3_candidate", SOLUTION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SOLUTION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


def ints_term(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def python_outcome(fn, values: list[int]):
    try:
        value = fn(values.copy())
    except Exception as exc:
        return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}
    return {"kind": "return", "type": type(value).__name__, "repr": repr(value)}


def k_outcome(stdout: str):
    terminal = re.search(r"<k>\s*\.K\s*</k>", stdout, re.DOTALL) is not None
    integer = re.search(
        r"<result>\s*intVal\s*\(\s*(-?\d+)\s*\)\s*</result>", stdout, re.DOTALL
    )
    floating = re.search(
        r"<result>\s*floatVal\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*</result>",
        stdout,
        re.DOTALL,
    )
    if terminal and integer:
        return {"kind": "return-int", "value": int(integer.group(1))}
    if terminal and floating:
        return {
            "kind": "return-exact-rational",
            "numerator": int(floating.group(1)),
            "denominator": int(floating.group(2)),
        }
    return {"kind": "stuck-or-unmodeled", "terminal": terminal}


def bridge_matches(py, kval) -> bool:
    if py["kind"] != "return":
        return False
    if kval["kind"] == "return-int":
        return py["type"] == "int" and int(py["repr"]) == kval["value"]
    if kval["kind"] == "return-exact-rational" and py["type"] == "float":
        py_fraction = Fraction.from_float(float(py["repr"]))
        k_fraction = Fraction(kval["numerator"], kval["denominator"])
        return py_fraction == k_fraction
    return False


def main() -> int:
    candidate = load_candidate()
    mismatches = 0
    for label, values in CASES:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={ints_term(values)}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        py = python_outcome(candidate, values)
        kval = k_outcome(completed.stdout)
        match = completed.returncode == 0 and bridge_matches(py, kval)
        if not match:
            mismatches += 1
        print(
            json.dumps(
                {
                    "label": label,
                    "input": values,
                    "command": shlex.join(command),
                    "k_exit": completed.returncode,
                    "k_outcome": kval,
                    "python_outcome": py,
                    "exact_value_bridge_match": match,
                    "k_stdout": completed.stdout,
                    "k_stderr": completed.stderr,
                },
                sort_keys=True,
            )
        )
    print(f"SEMANTICS_CASES {len(CASES)}")
    print(f"SEMANTICS_BRIDGE_MISMATCHES {mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
