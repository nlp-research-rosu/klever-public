#!/usr/bin/env python3
"""Compare freshly rebuilt K execution with independent Python execution."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
from typing import Any, Callable


DEFINITION = Path(
    "/tmp/audit-work/99-closest-integer/build/semantic-fresh-kompiled"
)
PROGRAM = Path("/tmp/audit-work/99-closest-integer/source/solution.mpy")
SOLUTION = Path("/tmp/audit-work/99-closest-integer/source/solution.py")
RESULT_PATTERN = re.compile(
    r"<result>\s*pyInt\s*\(\s*(-?[0-9]+)\s*\)\s*</result>"
)

CASES = [
    ("normal", "10"),
    ("normal", "15.3"),
    ("tie", "14.5"),
    ("tie", "-14.5"),
    ("sign", "-0.0"),
    ("below-half", "-0.49"),
    ("above-half", "-0.51"),
    ("below-half", "0.49"),
    ("at-half", "0.5"),
    ("above-half", "0.51"),
    ("precision", "1.499999999999999999999999"),
    ("precision", "1.500000000000000000000001"),
    ("precision", "-1.499999999999999999999999"),
    ("precision", "-1.500000000000000000000001"),
    ("exponent", "1.5e2"),
    ("exponent", "1.45e1"),
    ("empty-invalid", ""),
]


def load_solution() -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location("audit_solution", SOLUTION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SOLUTION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


def python_outcome(function: Callable[[str], int], value: str) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(value)}
    except Exception as error:
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "message": str(error),
        }


def quote_k_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def main() -> None:
    function = load_solution()
    matches = 0
    mismatches = 0
    invalid_nonreturn_matches = 0
    for category, value in CASES:
        arg = f"pyStr({quote_k_string(value)})"
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cARG={arg}",
        ]
        print("COMMAND: " + shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        output = completed.stdout + completed.stderr
        print(output.rstrip())
        print(f"EXIT_STATUS: {completed.returncode}")
        match = RESULT_PATTERN.search(output)
        if match:
            k_outcome: dict[str, Any] = {
                "kind": "return",
                "value": int(match.group(1)),
            }
        else:
            k_outcome = {"kind": "nonreturn", "residual": "<result> noResult"}
        py_outcome = python_outcome(function, value)
        same = k_outcome == py_outcome
        if (
            category == "empty-invalid"
            and k_outcome["kind"] == "nonreturn"
            and py_outcome["kind"] == "raise"
        ):
            invalid_nonreturn_matches += 1
            comparison = "both reject/nonreturn; exception behavior is not modeled"
        elif same:
            matches += 1
            comparison = "same returned integer"
        else:
            mismatches += 1
            comparison = "MISMATCH"
        print(
            "COMPARISON: "
            + json.dumps(
                {
                    "category": category,
                    "input": value,
                    "python": py_outcome,
                    "k": k_outcome,
                    "assessment": comparison,
                },
                sort_keys=True,
            )
        )
        print()
    print(
        "SUMMARY "
        + json.dumps(
            {
                "valid_return_matches": matches,
                "valid_mismatches": mismatches,
                "invalid_both_nonreturn_or_raise": invalid_nonreturn_matches,
                "total": len(CASES),
            },
            sort_keys=True,
        )
    )
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
