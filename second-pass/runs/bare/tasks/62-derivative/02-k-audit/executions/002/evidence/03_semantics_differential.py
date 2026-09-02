#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with independent Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shlex
import subprocess
import sys


WORK = Path("/tmp/audit-work/reconstruction-62")
DEFINITION = Path(sys.argv[1]) if len(sys.argv) > 1 else WORK / "semantic-fresh-kompiled"


def load_candidate():
    path = WORK / "solution.py"
    spec = importlib.util.spec_from_file_location("fresh_candidate", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derivative


def value_term(xs: list[int]) -> str:
    return "ListV(" + ", ".join(f"IntV({x})" for x in xs) + ")"


def parse_int_list(output: str) -> list[int]:
    return [
        int(match)
        for match in re.findall(r"IntV\s*\(\s*(-?[0-9]+)\s*\)", output)
    ]


def main() -> int:
    candidate = load_candidate()
    cases = [
        [],
        [7],
        [0, 9],
        [1, 2, 3],
        [3, 1, 2, 4, 5],
        [0, -2, 3, -4],
        [10**30, -(10**25), 0, 10**20],
    ]
    failures = 0
    for xs in cases:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            "-cARGS=" + value_term(xs),
        ]
        print("COMMAND:", shlex.join(command))
        result = subprocess.run(command, cwd=WORK, text=True, capture_output=True)
        print(result.stdout, end="")
        print(result.stderr, end="")
        print("EXIT_STATUS:", result.returncode)
        expected = candidate(list(xs))
        actual = parse_int_list(result.stdout)
        matches = result.returncode == 0 and actual == expected
        print(f"INPUT: {xs!r}")
        print(f"PYTHON_EXPECTED: {expected!r}")
        print(f"K_PARSED_RESULT: {actual!r}")
        print(f"MATCH: {matches}")
        failures += not matches
    print(f"SEMANTICS_DIFFERENTIAL_FAILURES: {failures}")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
