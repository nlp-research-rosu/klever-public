#!/usr/bin/env python3
"""Witness where exact-rational K semantics diverges from real Python execution."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any


WORK = Path("/tmp/audit-work")
CANDIDATE = WORK / "candidate"
DEFINITION = CANDIDATE / "concrete-kompiled"
RESULT_RE = re.compile(
    r"<result>\s*PyNum\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*</result>"
)
CASES = (
    ("rounding", 2**53 + 1, 1),
    ("overflow", 10**400, 1),
)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def python_outcome(function: Any, a: int, h: int) -> tuple[str, Any]:
    try:
        value = function(a, h)
    except Exception as error:  # noqa: BLE001 - exception is part of the witness.
        return ("exception", type(error).__name__)
    if isinstance(value, float):
        numerator, denominator = value.as_integer_ratio()
        return ("float", Fraction(numerator, denominator))
    return ("value", value)


def main() -> None:
    canonical = load_module("canonical_numeric_witness", WORK / "canonical.py")
    candidate = load_module("candidate_numeric_witness", CANDIDATE / "solution.py")
    witnessed = 0
    for label, a, h in CASES:
        result = subprocess.run(
            [
                "krun",
                "solution.mpy",
                "--definition",
                str(DEFINITION),
                f"-cARGS=Args({a}, {h})",
            ],
            cwd=CANDIDATE,
            text=True,
            capture_output=True,
            check=False,
        )
        match = RESULT_RE.search(result.stdout)
        if result.returncode != 0 or match is None:
            print(result.stdout)
            print(result.stderr)
            raise SystemExit("K witness execution did not terminate in PyNum")
        k_value = Fraction(int(match.group(1)), int(match.group(2)))
        canonical_outcome = python_outcome(canonical.triangle_area, a, h)
        candidate_outcome = python_outcome(candidate.triangle_area, a, h)
        differs = (
            canonical_outcome == candidate_outcome
            and canonical_outcome != ("float", k_value)
            and canonical_outcome != ("value", k_value)
        )
        input_text = "2**53 + 1" if label == "rounding" else "10**400"
        print(f"witness={label} input_a={input_text} input_h=1")
        print(
            f"  K exit={result.returncode} exact_result={k_value} "
            f"numerator_digits={len(str(k_value.numerator))}"
        )
        print(f"  canonical Python outcome={canonical_outcome}")
        print(f"  candidate Python outcome={candidate_outcome}")
        print(f"  K/Python semantic divergence={differs}")
        if differs:
            witnessed += 1
    print(f"semantic divergence witnesses: {witnessed}/{len(CASES)}")
    if witnessed != len(CASES):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
