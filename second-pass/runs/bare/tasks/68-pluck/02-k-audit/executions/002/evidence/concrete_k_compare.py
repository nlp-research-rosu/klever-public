#!/usr/bin/env python3
"""Compare fresh concrete K execution with independent Python results."""

from __future__ import annotations

from pathlib import Path
import re
import shlex
import subprocess
import sys


WORK = Path("/tmp/audit-work/candidate")
DEFINITION = WORK / "audit-semantic-kompiled"


def oracle(values: list[int]) -> list[int]:
    best: tuple[int, int] | None = None
    for index, value in enumerate(values):
        if value % 2 == 0 and (best is None or value < best[0]):
            best = (value, index)
    return [] if best is None else [best[0], best[1]]


def k_list(values: list[int]) -> str:
    return "VList(" + ", ".join(map(str, values)) + ")"


def parse_result(output: str) -> list[int]:
    match = re.search(r"<result>\s*VList\s*\((.*?)\)\s*</result>", output, re.S)
    if match is None:
        raise ValueError("no final VList result cell")
    body = match.group(1).replace(".Ints", "").strip(" ,\n")
    return [] if not body else [int(item.strip()) for item in body.split(",")]


def main() -> int:
    cases = [
        [],
        [0],
        [1],
        [4, 2, 3],
        [1, 2, 3],
        [7, 5, 9],
        [2, 2],
        [8, 3, 2],
        [5, 0, 3, 0, 4, 2],
        [999_999_999, 1_000_000_000, 2],
        [3] * 29 + [0],
    ]
    mismatches = 0
    for index, values in enumerate(cases, start=1):
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            f"-cARGS={k_list(values)}",
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            capture_output=True,
            check=False,
        )
        print(f"case[{index}].command={shlex.join(command)}")
        print(f"case[{index}].input={values!r}")
        print(f"case[{index}].exit_status={completed.returncode}")
        if completed.returncode != 0:
            print(f"case[{index}].stderr={completed.stderr[-2000:]!r}")
            mismatches += 1
            continue
        try:
            actual = parse_result(completed.stdout)
        except ValueError as error:
            print(f"case[{index}].parse_error={error}")
            print(f"case[{index}].stdout_tail={completed.stdout[-2000:]!r}")
            mismatches += 1
            continue
        expected = oracle(values)
        print(f"case[{index}].k_result={actual!r}")
        print(f"case[{index}].python_result={expected!r}")
        print(f"case[{index}].match={actual == expected}")
        mismatches += actual != expected
    print(f"case_count={len(cases)}")
    print(f"mismatch_count={mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
