#!/usr/bin/env python3
"""Compare fresh K concrete results with actual submitted-Python outcomes."""

from __future__ import annotations

import fractions
import importlib.util
import pathlib
import re
import subprocess


WORK = pathlib.Path("/tmp/audit-work/45-triangle-area")
RESULT_PATTERN = re.compile(
    r"<result>\s*PyNum\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*</result>",
    re.DOTALL,
)


def load_solution():
    path = WORK / "solution.py"
    spec = importlib.util.spec_from_file_location("submitted_for_k_comparison", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def run_k(a: int, h: int) -> tuple[int, int, str]:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "fresh-concrete-kompiled",
        f"-cARGS=Args({a},{h})",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"K command failed ({completed.returncode}): {command!r}\n{completed.stdout}"
        )
    match = RESULT_PATTERN.search(completed.stdout)
    if match is None:
        raise RuntimeError(f"no PyNum result in K output:\n{completed.stdout}")
    return int(match.group(1)), int(match.group(2)), " ".join(command)


def python_outcome(function, a: int, h: int):
    try:
        value = function(a, h)
        return ("value", value, fractions.Fraction.from_float(value))
    except Exception as error:
        return ("exception", type(error).__name__)


def main() -> None:
    cases = [
        (5, 3, "documented"),
        (0, 99, "zero boundary"),
        (-5, 3, "negative representative"),
        (2**53 - 1, 1, "last exact half below rounding transition"),
        (2**53 + 1, 1, "binary-float rounding witness"),
        (10**308, 1, "large finite-float witness"),
        (10**309, 1, "integer-to-float overflow witness"),
    ]
    solution = load_solution()
    mismatches = 0

    for a, h, label in cases:
        numerator, denominator, command = run_k(a, h)
        k_value = fractions.Fraction(numerator, denominator)
        py = python_outcome(solution, a, h)
        if py[0] == "value":
            agrees = k_value == py[2]
        else:
            agrees = False  # K produced a normal value where Python raised.
        if not agrees:
            mismatches += 1
        print(f"case={label}")
        print(f"  input=({a}, {h})")
        print(f"  k_command={command}")
        print(f"  k_exact={k_value!r}")
        print(f"  python={py!r}")
        print(f"  exact_observable_agreement={agrees}")

    print(f"total_cases={len(cases)}")
    print(f"mismatches={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
