#!/usr/bin/env python3
"""Run the fresh generated K semantics and compare with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/34-unique")
PROGRAM = ROOT / "candidate-source/solution.mpy"
DEFINITION = ROOT / "concrete-kompiled"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_expr(values: list[int]) -> str:
    return "ListExpr(" + ", ".join(f"Int({value})" for value in values) + ")"


def parse_k_list(output: str) -> list[int]:
    match = re.search(
        r"<k>\s*VList\s*\((.*?)\)\s*~>\s*\.K\s*</k>", output, re.DOTALL
    )
    if match is None:
        raise ValueError("final <k> cell is not a VList")
    return [
        int(item)
        for item in re.findall(r"VInt\s*\(\s*(-?\d+)\s*\)", match.group(1))
    ]


def main() -> int:
    canonical = load("trusted_canonical_34_concrete", ROOT / "reference/canonical.py")
    generated = load(
        "scratch_generated_34_concrete", ROOT / "candidate-source/solution.py"
    )
    cases = [
        ("documented", [5, 3, 5, 2, 3, 3, 9, 0, 123]),
        ("empty", []),
        ("all-equal", [1, 1]),
        ("insert-lte", [1, 2]),
        ("insert-gt", [2, 1]),
        ("negative-zero-duplicates", [-1, -1, 2, 0]),
        ("extreme-ints", [-(10**30), 0, 10**30, -(10**30)]),
    ]
    failures = 0
    for label, values in cases:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cARGS={k_expr(values)}",
        ]
        print(f"CASE={label}")
        print("COMMAND=" + shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"KRUN_EXIT_STATUS={completed.returncode}")
        print("KRUN_STDOUT_BEGIN")
        print(completed.stdout.rstrip())
        print("KRUN_STDOUT_END")
        if completed.stderr:
            print("KRUN_STDERR_BEGIN")
            print(completed.stderr.rstrip())
            print("KRUN_STDERR_END")
        try:
            k_result = parse_k_list(completed.stdout)
        except Exception as exc:
            print(f"PARSE_ERROR={type(exc).__name__}: {exc}")
            failures += 1
            continue
        canonical_result = canonical.unique(list(values))
        generated_result = generated.unique(list(values))
        print(f"INPUT={values!r}")
        print(f"K_RESULT={k_result!r}")
        print(f"CANONICAL_PYTHON_RESULT={canonical_result!r}")
        print(f"GENERATED_PYTHON_RESULT={generated_result!r}")
        equal = k_result == canonical_result == generated_result
        print(f"ALL_EQUAL={equal}")
        failures += not equal or completed.returncode != 0

    print(f"TOTAL_CASES={len(cases)}")
    print(f"MISMATCH_OR_EXECUTION_FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
