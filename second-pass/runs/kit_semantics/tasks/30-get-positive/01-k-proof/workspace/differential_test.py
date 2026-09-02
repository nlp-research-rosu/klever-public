#!/usr/bin/env python3
"""Finite CPython-oracle versus MPY/LLVM differential evidence."""

from __future__ import annotations

import random
import subprocess
from pathlib import Path

from solution import get_positive


ROOT = Path(__file__).resolve().parent


def cases() -> list[list[int | float]]:
    fixed: list[list[int | float]] = [
        [],
        [0],
        [-1],
        [1],
        [-1, 0, 1],
        [-0.0, 0.0, 0.25, -0.25],
        [-2.5, 0.0, 1.25, 7],
        [-1, 2, -4, 5, 6],
        [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
        [-(10**30), 10**30, -1.0e200, 1.0e200],
    ]
    rng = random.Random(20260729)
    pool: list[int | float] = [
        -1000,
        -7,
        -1,
        0,
        1,
        7,
        1000,
        -99.75,
        -0.5,
        -0.0,
        0.0,
        0.5,
        99.75,
    ]
    sampled = [
        [rng.choice(pool) for _ in range(rng.randrange(0, 9))]
        for _ in range(50)
    ]
    return fixed + sampled


def oracle(values: list[int | float]) -> list[int | float]:
    # Independent implementation form: this does not call get_positive and
    # shares none of the K summary equations.
    return [value for value in values if value > 0]


def main() -> int:
    test_cases = cases()
    mismatches = [
        (values, get_positive(values), oracle(values))
        for values in test_cases
        if get_positive(values) != oracle(values)
    ]
    if mismatches:
        raise AssertionError(f"CPython mismatches: {mismatches!r}")

    solution_source = (ROOT / "solution.py").read_text(encoding="utf-8")
    assertions = "\n".join(
        f"assert get_positive({values!r}) == {oracle(values)!r}"
        for values in test_cases
    )
    smoke_source = solution_source + "\n\n" + assertions + "\n"
    smoke_py = ROOT / "differential-smoke.py"
    smoke_mpy = ROOT / "differential-smoke.mpy"
    smoke_py.write_text(smoke_source, encoding="utf-8")

    translated = subprocess.run(
        ["python3", "py2mpy.py", smoke_py.name],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    smoke_mpy.write_text(translated.stdout, encoding="utf-8")

    executed = subprocess.run(
        ["krun", smoke_mpy.name, "--definition", "runtime-kompiled"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if "<exit-code>\n    0\n  </exit-code>" not in executed.stdout:
        raise AssertionError(
            "MPY/LLVM assertion failure:\n"
            + executed.stdout[-4000:]
            + executed.stderr[-4000:]
        )

    print(
        f"cases={len(test_cases)} "
        "cpython_mismatches=0 mpy_llvm_mismatches=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
