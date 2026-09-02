#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from fractions import Fraction
from pathlib import Path
from types import ModuleType


WORK = Path("/tmp/audit-work")
CANDIDATE = WORK / "candidate"
DEFINITION = CANDIDATE / "concrete-kompiled"
CASES = (
    (5, 3),       # documented normal input
    (0, 99),      # zero side
    (99, 0),      # zero height
    (0, 0),       # both boundary values
    (-4, 3),      # representative signed input admitted by the K theorem
    (7, -2),
    (2, 2),       # even product
    (7, 3),       # odd product
)
RESULT_RE = re.compile(
    r"<result>\s*PyNum\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*</result>"
)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    canonical = load_module("canonical_for_k", WORK / "canonical.py")
    candidate = load_module("candidate_for_k", CANDIDATE / "solution.py")
    mismatches = 0
    for a, h in CASES:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            f"-cARGS=Args({a}, {h})",
        ]
        result = subprocess.run(
            command,
            cwd=CANDIDATE,
            text=True,
            capture_output=True,
            check=False,
        )
        match = RESULT_RE.search(result.stdout)
        k_value = Fraction(int(match.group(1)), int(match.group(2))) if match else None
        canonical_value = canonical.triangle_area(a, h)
        candidate_value = candidate.triangle_area(a, h)
        agrees = (
            result.returncode == 0
            and k_value is not None
            and float(k_value) == canonical_value
            and type(canonical_value) is type(candidate_value)
            and canonical_value == candidate_value
        )
        print(
            f"args=({a}, {h}) exit={result.returncode} "
            f"K={k_value} canonical={canonical_value!r} "
            f"candidate={candidate_value!r} agrees={agrees}"
        )
        if not agrees:
            mismatches += 1
            print(result.stdout)
            print(result.stderr)
    print(f"concrete cases: {len(CASES)}")
    print(f"mismatch count: {mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
