#!/usr/bin/env python3
"""False-conclusion witnesses for the exactNum Decimal arithmetic rules."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
from typing import Callable


SOLUTION = Path("/tmp/audit-work/99-closest-integer/source/solution.py")
PROGRAM = Path("/tmp/audit-work/99-closest-integer/source/solution.mpy")
DEFINITION = Path(
    "/tmp/audit-work/99-closest-integer/build/semantic-fresh-kompiled"
)
RESULT_PATTERN = re.compile(
    r"<result>\s*pyInt\s*\(\s*(-?[0-9]+)\s*\)\s*</result>"
)
CASES = [
    ("S17 exact addition", "9999999999999999999999999999.4"),
    ("S18 exact subtraction", "-9999999999999999999999999999.4"),
]


def load_solution() -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location("context_solution", SOLUTION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SOLUTION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


def exact_oracle(value: str) -> int:
    fraction = Fraction(value)
    shifted = (
        fraction + Fraction(1, 2)
        if fraction >= 0
        else fraction - Fraction(1, 2)
    )
    return int(shifted)


def main() -> None:
    solution = load_solution()
    mismatch_count = 0
    print(
        "DECIMAL_CONTEXT "
        + json.dumps(
            {
                "precision": getcontext().prec,
                "rounding": getcontext().rounding,
                "Emin": getcontext().Emin,
                "Emax": getcontext().Emax,
            },
            sort_keys=True,
        )
    )
    for rule, value in CASES:
        number = Decimal(value)
        half = Decimal("0.5")
        shifted = number + half if number >= 0 else number - half
        python_result = solution(value)
        expected_exact = exact_oracle(value)
        arg = f"-cARG=pyStr({json.dumps(value)})"
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            arg,
        ]
        print("COMMAND: " + shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        output = completed.stdout + completed.stderr
        print(output.rstrip())
        print(f"EXIT_STATUS: {completed.returncode}")
        match = RESULT_PATTERN.search(output)
        if match is None:
            raise RuntimeError(f"no pyInt K result for {value}")
        k_result = int(match.group(1))
        false_conclusion = k_result == expected_exact and k_result != python_result
        mismatch_count += false_conclusion
        print(
            "WITNESS "
            + json.dumps(
                {
                    "rule": rule,
                    "input": value,
                    "decimal_shifted_value": str(shifted),
                    "python_result": python_result,
                    "exact_fraction_oracle": expected_exact,
                    "k_result": k_result,
                    "k_conclusion_is_false_of_real_program": false_conclusion,
                },
                sort_keys=True,
            )
        )
    print(
        "SUMMARY "
        + json.dumps(
            {
                "cases": len(CASES),
                "false_real_program_conclusions": mismatch_count,
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if mismatch_count == len(CASES) else 1)


if __name__ == "__main__":
    main()
