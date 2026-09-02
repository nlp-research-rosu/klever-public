#!/usr/bin/env python3
"""Compare fresh K concrete execution against both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys


SCRATCH = Path("/tmp/audit-work/121-solution-audit")
CANDIDATE = SCRATCH / "candidate"
DEFINITION = CANDIDATE / "semantic-audit-kompiled"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_ints(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value},{term})"
    return term


def main() -> int:
    canonical = load("trusted_canonical_semantics", SCRATCH / "reference/canonical.py")
    generated = load("generated_solution_semantics", CANDIDATE / "solution.py")
    cases = [
        ("empty-zero-iteration", []),
        ("singleton-even-false-final", [0]),
        ("singleton-odd-true-final", [-1]),
        ("pair-true-skip", [5, 999]),
        ("pair-false-skip", [-4, 999]),
        ("documented-1", [5, 8, 7, 1]),
        ("documented-2", [3, 3, 3, 3, 3]),
        ("documented-3", [30, 13, 24, 321]),
        ("negative-mixed", [-5, 2, -3]),
        ("large", [10**40 + 1, 7, -(10**40 + 3), 9]),
    ]
    mismatches = 0
    result_pattern = re.compile(r"result\s*\(\s*(-?[0-9]+)\s*\)")

    for name, values in cases:
        command = [
            "krun",
            str(CANDIDATE / "solution.mpy"),
            "--definition",
            str(DEFINITION),
            "-cINPUT=" + k_ints(values),
        ]
        print("$ " + " ".join(command))
        completed = subprocess.run(
            command,
            cwd=CANDIDATE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(completed.stdout.rstrip())
        print(f"[exit {completed.returncode}]")
        match = result_pattern.search(completed.stdout)
        k_result = int(match.group(1)) if match else None
        canonical_result = canonical.solution(values)
        generated_result = generated.solution(values)
        agrees = (
            completed.returncode == 0
            and k_result == canonical_result
            and k_result == generated_result
        )
        print(
            f"case={name} input={values!r} K={k_result!r} "
            f"canonical={canonical_result!r} generated={generated_result!r} "
            f"agree={agrees}"
        )
        if not agrees:
            mismatches += 1

    print(f"semantic_cases={len(cases)}")
    print(f"semantic_mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
