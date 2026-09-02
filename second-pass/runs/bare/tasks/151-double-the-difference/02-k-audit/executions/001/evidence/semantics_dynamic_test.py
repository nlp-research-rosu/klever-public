#!/usr/bin/env python3
"""Compare fresh K execution of solution.mpy with independent Python execution."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
from typing import Any


WORK = Path("/tmp/audit-work/candidate-src")
DEFINITION = Path("/tmp/audit-work/build-verified/semantic-kompiled")


def load_candidate():
    spec = importlib.util.spec_from_file_location(
        "dynamic_candidate", WORK / "solution.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import candidate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.double_the_difference


candidate = load_candidate()


def k_float(value: float) -> str:
    text = repr(value)
    if text == "-0.0":
        return "-0.0"
    return text


def vals(values: list[Any]) -> str:
    tail = "nil"
    for value in reversed(values):
        if isinstance(value, bool):
            tail = f"boolCons({'true' if value else 'false'},{tail})"
        elif isinstance(value, int):
            tail = f"intCons({value},{tail})"
        elif isinstance(value, float):
            tail = f"floatCons({k_float(value)},{tail})"
        elif isinstance(value, list):
            tail = f"listCons({vals(value)},{tail})"
        else:
            raise TypeError(f"unmodeled test value: {value!r}")
    return tail


def extract_result(output: str) -> int:
    match = re.search(
        r"<result>\s*pyInt\s*\(\s*(-?[0-9]+)\s*\)\s*</result>",
        output,
    )
    if match is None:
        raise AssertionError(f"no pyInt result in K output:\n{output}")
    return int(match.group(1))


def main() -> int:
    cases: list[list[Any]] = [
        [1, 3, 2, 0],
        [-1, -2, 0],
        [9, -2],
        [0],
        [],
        [-3],
        [-1],
        [1],
        [2],
        [3],
        [4],
        [-2, -1, 0, 1, 2, 3, 4],
        [-1.5, -1.0, -0.0, 0.0, 1.0, 1.5, 2.0, 3.0],
        [True],
        [False],
        [True, False, 1, 2, -1, 3, 1.5],
        [[7], 3],
        [[], 5, [9], -7],
        [-(10**50), 10**50, 10**50 + 1],
    ]
    mismatches = 0
    for index, case in enumerate(cases):
        input_term = f"pyList({vals(case)})"
        command = [
            "krun",
            str(WORK / "solution.mpy"),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={input_term}",
        ]
        print(f"CASE {index}: input={case!r}")
        print("COMMAND: " + " ".join(command))
        process = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
            check=False,
        )
        print(f"KRUN_EXIT_STATUS={process.returncode}")
        if process.returncode != 0:
            print(process.stdout)
            raise AssertionError(f"krun failed for case {index}")
        k_result = extract_result(process.stdout)
        python_result = candidate(list(case))
        matches = k_result == python_result
        print(
            f"RESULT: k={k_result!r} python={python_result!r} "
            f"match={matches}"
        )
        if not matches:
            mismatches += 1
    print(f"SEMANTICS_DYNAMIC_CASES={len(cases)}")
    print(f"SEMANTICS_DYNAMIC_MISMATCHES={mismatches}")
    if mismatches:
        raise AssertionError(f"{mismatches} semantics/Python mismatches")
    print("SEMANTICS_DYNAMIC_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
