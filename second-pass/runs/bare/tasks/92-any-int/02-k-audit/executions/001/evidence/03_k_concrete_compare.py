#!/usr/bin/env python3
"""Compare freshly compiled K execution against independent Python execution."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from decimal import Decimal
from pathlib import Path


DEFINITION = Path("/tmp/audit-work/92-any-int/concrete-kompiled")
SOLUTION = Path("/tmp/audit-work/92-any-int/src/solution.py")


def load_solution(path: Path):
    spec = importlib.util.spec_from_file_location("audit_generated_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


class IntSubclass(int):
    pass


def run_k(term: str):
    command = ["krun", "-d", str(DEFINITION), f"-cPGM={term}"]
    completed = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    match = re.search(r"boolVal\s*\(\s*(true|false)\s*\)", completed.stdout)
    parsed = None if match is None else match.group(1) == "true"
    return command, completed.returncode, parsed, completed.stdout


solution = load_solution(SOLUTION)

cases = [
    ("prompt-first", (5, 2, 7), "RunAnyInt(intVal(5), intVal(2), intVal(7))"),
    ("prompt-none", (3, 2, 2), "RunAnyInt(intVal(3), intVal(2), intVal(2))"),
    ("prompt-negative", (3, -2, 1), "RunAnyInt(intVal(3), intVal(-2), intVal(1))"),
    (
        "prompt-floats",
        (3.6, -2.2, 2),
        "RunAnyInt(floatVal(3.6), floatVal(-2.2), intVal(2))",
    ),
    ("zero-boundary", (0, 0, 0), "RunAnyInt(intVal(0), intVal(0), intVal(0))"),
    ("second-sum", (4, 10, 6), "RunAnyInt(intVal(4), intVal(10), intVal(6))"),
    ("third-sum", (10, 4, 6), "RunAnyInt(intVal(10), intVal(4), intVal(6))"),
    (
        "large",
        (10**40, -(10**40), 0),
        f"RunAnyInt(intVal({10**40}), intVal({-(10**40)}), intVal(0))",
    ),
    ("bool-first", (True, 1, 2), "RunAnyInt(boolVal(true), intVal(1), intVal(2))"),
    ("bool-second", (1, False, 1), "RunAnyInt(intVal(1), boolVal(false), intVal(1))"),
    (
        "int-subclass-first",
        (IntSubclass(1), 1, 2),
        'RunAnyInt(otherNumberVal("IntSubclass"), intVal(1), intVal(2))',
    ),
    ("float-third", (1, 2, 3.0), "RunAnyInt(intVal(1), intVal(2), floatVal(3.0))"),
    (
        "other-number",
        (Decimal("1"), 1, 2),
        'RunAnyInt(otherNumberVal("Decimal"), intVal(1), intVal(2))',
    ),
]

failures = 0
for name, python_args, k_term in cases:
    expected = solution(*python_args)
    command, status, actual, output = run_k(k_term)
    matches = status == 0 and actual is expected
    print(f"CASE: {name}")
    print("COMMAND:", " ".join(command))
    print(f"EXIT_STATUS: {status}")
    print(f"PYTHON_ARGS: {python_args!r}")
    print(f"PYTHON_RESULT: {expected!r}")
    print(f"K_PARSED_RESULT: {actual!r}")
    print(f"MATCH: {matches}")
    print("K_OUTPUT_BEGIN")
    print(output.rstrip())
    print("K_OUTPUT_END")
    if not matches:
        failures += 1

print(f"SUMMARY: cases={len(cases)} failures={failures}")
raise SystemExit(1 if failures else 0)
