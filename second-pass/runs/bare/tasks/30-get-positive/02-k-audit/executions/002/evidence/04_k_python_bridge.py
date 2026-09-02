#!/usr/bin/env python3
"""Finite independent comparison of generated K semantics with Python."""

from __future__ import annotations

import itertools
import random
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/30-get-positive/candidate-src")


def pylist(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return result


def decode_k(stdout: str) -> list[int]:
    match = re.search(r"<k>\s*(.*?)\s*~>\s*\.K\s*</k>", stdout, re.S)
    if match is None:
        raise ValueError(f"cannot find final <k> result in {stdout!r}")
    return [int(token) for token in re.findall(r"-?\d+", match.group(1))]


def main() -> int:
    cases = [
        [-1, 2, -4, 5, 6],
        [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
        [],
        [-1],
        [0],
        [1],
        [-2, -1, 0, 1, 2, 2],
        [-10**30, 0, 10**30],
    ]
    pool = [-2, -1, 0, 1, 2]
    for length in range(3):
        cases.extend(list(values) for values in itertools.product(pool, repeat=length))
    rng = random.Random(20260726)
    for _ in range(25):
        cases.append(
            [rng.randint(-100, 100) for _ in range(rng.randrange(0, 9))]
        )

    mismatches = []
    for index, values in enumerate(cases):
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "concrete-kompiled",
            "--color",
            "off",
            "-cINPUT=" + pylist(values),
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        expected = [value for value in values if value > 0]
        try:
            actual = decode_k(completed.stdout) if completed.returncode == 0 else None
        except ValueError:
            actual = None
        ok = completed.returncode == 0 and actual == expected
        print(
            f"CASE index={index} input={values!r} expected={expected!r} "
            f"k={actual!r} krun_exit={completed.returncode} equal={ok}"
        )
        if not ok:
            mismatches.append((index, values, expected, completed.returncode, completed.stdout))
    print(
        "COMMAND_PATTERN krun solution.mpy --definition concrete-kompiled "
        "--color off -cINPUT=<encoded PyList>"
    )
    print(
        "SCOPE 2 examples; empty and -1/0/+1 boundaries; duplicates; "
        "arbitrary-precision extremes; exhaustive lengths 0..2 over "
        "[-2,-1,0,1,2]; 25 deterministic random lists of length 0..8"
    )
    print(f"CASES={len(cases)} MISMATCHES={len(mismatches)}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
