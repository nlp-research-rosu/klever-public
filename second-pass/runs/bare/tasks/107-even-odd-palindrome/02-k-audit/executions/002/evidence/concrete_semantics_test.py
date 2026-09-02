#!/usr/bin/env python3
"""Compare the freshly rebuilt generated K semantics with Python."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
CASES = [1, 3, 9, 10, 11, 12, 99, 100, 101, 109, 110, 111, 121, 199, 200, 201, 202, 989, 999, 1000]


def load_solution():
    spec = importlib.util.spec_from_file_location("scratch_solution", WORK / "solution.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


solution = load_solution()
pattern = re.compile(
    r"VTuple\s*\(\s*VInt\s*\(\s*(-?\d+)\s*\)\s*,\s*"
    r"VInt\s*\(\s*(-?\d+)\s*\)\s*\)"
)
failures = []

print("COMMAND_TEMPLATE: krun solution.mpy -cN=<n> --definition concrete-kompiled --output pretty")
print(f"WORKDIR: {WORK}")
print(f"INPUTS: {CASES}")
for n in CASES:
    command = [
        "krun",
        "solution.mpy",
        f"-cN={n}",
        "--definition",
        "concrete-kompiled",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )
    matches = pattern.findall(completed.stdout)
    k_result = tuple(map(int, matches[0])) if len(matches) == 1 else None
    python_result = solution.even_odd_palindrome(n)
    ok = (
        completed.returncode == 0
        and k_result == python_result
        and "<return>\n    noReturn\n  </return>" in completed.stdout
    )
    print(
        f"n={n} exit={completed.returncode} "
        f"k_result={k_result} python_result={python_result} "
        f"return_reset={'noReturn' if 'noReturn' in completed.stdout else 'missing'} "
        f"match={ok}"
    )
    if completed.stderr:
        print(f"n={n} stderr={' '.join(completed.stderr.split())[:500]}")
    if not ok:
        failures.append((n, completed.returncode, k_result, python_result, completed.stdout))

print(f"failure_count={len(failures)}")
for failure in failures:
    print(f"FAILURE={failure!r}")
raise SystemExit(1 if failures else 0)
