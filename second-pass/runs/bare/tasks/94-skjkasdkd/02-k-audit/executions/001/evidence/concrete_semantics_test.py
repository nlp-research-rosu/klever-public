#!/usr/bin/env python3
"""Fresh concrete K executions compared with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable


SOURCE = Path("/tmp/audit-work/94-skjkasdkd/source")
DEFINITION = Path("/tmp/audit-work/94-skjkasdkd/build/semantic-kompiled")


def load_function(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.skjkasdkd


candidate = load_function(SOURCE / "solution.py", "concrete_candidate_94")
canonical = load_function(Path("/reference/canonical.py"), "concrete_canonical_94")


def oracle(values: list[int]) -> int:
    def prime(value: int) -> bool:
        return value >= 2 and all(
            value % divisor
            for divisor in range(2, int(value**0.5) + 1)
        )

    primes = [value for value in values if prime(value)]
    return sum(map(int, str(max(primes)))) if primes else 0


cases = [
    ("empty", []),
    ("negative-only", [-9, -2, -1]),
    ("zero", [0]),
    ("one-primality-boundary", [1]),
    ("two-primality-boundary", [2]),
    ("square-divisible", [4, 9, 25]),
    ("square-plus-prime", [25, 29]),
    ("order-left-max", [13, 11, 4]),
    ("order-right-max", [4, 11, 13]),
    ("digit-one", [7]),
    ("digit-two", [11]),
    ("digit-zero", [101]),
    (
        "prompt-1",
        [0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3],
    ),
    (
        "prompt-2",
        [1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1],
    ),
    (
        "prompt-3",
        [1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3],
    ),
    ("prompt-4", [0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6]),
    ("prompt-5", [0, 81, 12, 3, 1, 21]),
    ("prompt-6", [0, 8, 1, 2, 1, 7]),
]

failures: list[str] = []
for label, values in cases:
    args = "listVal(" + ", ".join(f"intVal({value})" for value in values) + ")"
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARGS={args}",
    ]
    print(f"CASE {label} input={values!r}")
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=SOURCE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"KRUN_EXIT: {completed.returncode}")
    print(completed.stdout.rstrip())
    match = re.search(
        r"result\s*\(\s*intVal\s*\(\s*(-?\d+)\s*\)\s*\)",
        completed.stdout,
    )
    k_result = int(match.group(1)) if match else None
    candidate_result = candidate(list(values))
    canonical_result = canonical(list(values))
    oracle_result = oracle(values)
    print(
        f"RESULTS k={k_result!r} candidate={candidate_result!r} "
        f"canonical={canonical_result!r} oracle={oracle_result!r}"
    )
    if completed.returncode != 0:
        failures.append(f"{label}: krun exit {completed.returncode}")
    if "<k>\n    .K\n  </k>" not in completed.stdout:
        failures.append(f"{label}: final <k> was not .K")
    if k_result != candidate_result:
        failures.append(f"{label}: K {k_result!r} != candidate {candidate_result!r}")
    if k_result != oracle_result:
        failures.append(f"{label}: K {k_result!r} != oracle {oracle_result!r}")
    print("---")

print(f"SUMMARY cases={len(cases)} failures={len(failures)}")
for failure in failures:
    print(f"FAIL: {failure}")
raise SystemExit(1 if failures else 0)
