#!/usr/bin/env python3
"""Run the freshly compiled generated semantics on concrete integer lists."""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/57-monotonic")
DEFINITION = SCRATCH / "build-audit/semantic-llvm-kompiled"
PROGRAM = SCRATCH / "solution.regenerated.mpy"

CASES = [
    ("empty", []),
    ("singleton", [0]),
    ("equal-pair", [1, 1]),
    ("increasing", [1, 2, 4, 20]),
    ("decreasing", [4, 1, 0, -10]),
    ("peak-nonmonotonic", [1, 20, 4, 10]),
    ("valley-nonmonotonic", [2, 1, 2]),
    ("duplicates-increasing", [-2, -2, 0, 3, 3]),
    ("duplicates-decreasing", [3, 3, 0, -2, -2]),
    ("large-integers", [-(10**30), 0, 10**30]),
]


def int_list_term(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return f"listVal({term})"


def oracle(values: list[int]) -> bool:
    return (
        all(left <= right for left, right in zip(values, values[1:]))
        or all(left >= right for left, right in zip(values, values[1:]))
    )


def main() -> int:
    failures = 0
    for label, values in CASES:
        command = [
            "krun",
            str(PROGRAM),
            f"-cARG={int_list_term(values)}",
            "--definition",
            str(DEFINITION),
        ]
        print(f"COMMAND {label}: {shlex.join(command)}")
        completed = subprocess.run(
            command,
            cwd=SCRATCH,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"EXIT {label}: {completed.returncode}")
        print(f"OUTPUT {label}:")
        print(completed.stdout.rstrip())
        expected = oracle(values)
        match = re.search(r"boolVal\s*\(\s*(true|false)\s*\)", completed.stdout)
        actual = None if match is None else match.group(1) == "true"
        ok = completed.returncode == 0 and actual is expected
        print(
            f"COMPARE {label}: input={values!r} "
            f"independent_python={expected} k={actual} ok={ok}"
        )
        failures += int(not ok)
    print(f"cases={len(CASES)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
