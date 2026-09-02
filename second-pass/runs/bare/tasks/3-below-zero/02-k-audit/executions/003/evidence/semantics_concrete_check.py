#!/usr/bin/env python3
"""Fresh concrete generated-semantics checks against independent Python."""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/rebuild")
DEFINITION = WORK / "audit-semantic-llvm"
PROGRAM = WORK / "solution.mpy"


def int_list(values: list[int]) -> str:
    term = ".IntList"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def oracle(values: list[int]) -> bool:
    running = 0
    for value in values:
        running += value
        if running < 0:
            return True
    return False


def main() -> None:
    cases = [
        [],
        [0],
        [-1],
        [1],
        [1, 2, 3],
        [1, 2, -4, 5],
        [5, -5],
        [5, -5, -1],
        [-1, 100],
        [2**80, -(2**80)],
        [-(2**80), 2**80],
    ]
    for values in cases:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            "-cOPERATIONS=" + int_list(values),
        ]
        print("RUN:", shlex.join(command))
        result = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            capture_output=True,
            check=False,
        )
        print(f"KRUN_EXIT={result.returncode}")
        if result.stderr:
            print("KRUN_STDERR:", result.stderr.strip())
        if result.returncode != 0:
            print(result.stdout)
            raise SystemExit(result.returncode)
        match = re.search(r"BoolV \( (true|false) \)", result.stdout)
        actual = None if match is None else match.group(1) == "true"
        expected = oracle(values)
        final_k = bool(re.search(r"<k>\s*\.K\s*</k>", result.stdout))
        reset_balance = bool(
            re.search(r"<balance>\s*0\s*</balance>", result.stdout)
        )
        reset_current = bool(
            re.search(r"<current>\s*0\s*</current>", result.stdout)
        )
        print(
            f"CASE input={values!r} expected={expected} actual={actual} "
            f"final_k={final_k} reset_balance={reset_balance} "
            f"reset_current={reset_current}"
        )
        if (
            actual is not expected
            or not final_k
            or not reset_balance
            or not reset_current
        ):
            print(result.stdout)
            raise SystemExit(1)
    print(f"CONCRETE_CASES={len(cases)} MISMATCHES=0")
    print("GENERATED_SEMANTICS_CONCRETE: PASS")


if __name__ == "__main__":
    main()
