#!/usr/bin/env python3
"""Compare fresh K concrete execution against independent Python execution."""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
from decimal import Decimal
from pathlib import Path
from typing import Any


def load_solution(path: Path):
    spec = importlib.util.spec_from_file_location("generated_solution_for_k_compare", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("definition", type=Path)
    parser.add_argument("solution", type=Path)
    args = parser.parse_args()
    solution = load_solution(args.solution)

    huge = 10**100
    cases: list[tuple[str, tuple[Any, Any, Any], str]] = [
        ("example-true", (5, 2, 7), "RunAnyInt(intVal(5), intVal(2), intVal(7))"),
        ("example-false", (3, 2, 2), "RunAnyInt(intVal(3), intVal(2), intVal(2))"),
        ("second-branch", (2, 5, 3), "RunAnyInt(intVal(2), intVal(5), intVal(3))"),
        ("third-branch", (5, 2, 3), "RunAnyInt(intVal(5), intVal(2), intVal(3))"),
        ("zero-boundary", (0, 0, 0), "RunAnyInt(intVal(0), intVal(0), intVal(0))"),
        (
            "negative-boundary",
            (-5, 2, -3),
            "RunAnyInt(intVal(-5), intVal(2), intVal(-3))",
        ),
        (
            "unbounded-large-int",
            (huge, -huge, 0),
            f"RunAnyInt(intVal({huge}), intVal(-{huge}), intVal(0))",
        ),
        (
            "float-first",
            (1.0, 2, 3),
            "RunAnyInt(floatVal(1.0), intVal(2), intVal(3))",
        ),
        (
            "float-second",
            (1, 2.0, 3),
            "RunAnyInt(intVal(1), floatVal(2.0), intVal(3))",
        ),
        (
            "float-third",
            (1, 2, 3.0),
            "RunAnyInt(intVal(1), intVal(2), floatVal(3.0))",
        ),
        (
            "bool-first",
            (True, 1, 2),
            "RunAnyInt(boolVal(true), intVal(1), intVal(2))",
        ),
        (
            "modeled-other-number",
            (Decimal("1"), 2, 3),
            'RunAnyInt(otherNumberVal("decimal:1"), intVal(2), intVal(3))',
        ),
    ]

    failures = 0
    for name, py_args, k_term in cases:
        command = [
            "krun",
            "--definition",
            str(args.definition),
            "-cPGM=" + k_term,
        ]
        result = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        match = re.search(r"boolVal\s*\(\s*(true|false)\s*\)", result.stdout)
        k_value = None if match is None else match.group(1) == "true"
        python_value = solution(*py_args)
        env_cleared = bool(re.search(r"<env>\s*\.Map\s*</env>", result.stdout))
        ok = (
            result.returncode == 0
            and match is not None
            and k_value is python_value
            and env_cleared
        )
        failures += not ok
        print(f"CASE {name}")
        print("COMMAND: " + " ".join(command))
        print(f"PYTHON_ARGS: {py_args!r}")
        print(f"PYTHON_RESULT: {python_value!r}")
        print(f"K_EXIT_STATUS: {result.returncode}")
        print(f"K_RESULT: {k_value!r}")
        print(f"K_ENV_CLEARED: {env_cleared}")
        print(f"MATCH: {ok}")
        print("K_OUTPUT_BEGIN")
        print(result.stdout.rstrip())
        print("K_OUTPUT_END")

    print(f"TOTAL_CASES: {len(cases)}")
    print(f"TOTAL_FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
