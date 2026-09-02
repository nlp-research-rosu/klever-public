#!/usr/bin/env python3
"""Check that the fused operational rules remain body- and guard-sensitive."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


DEFINITION = Path("/tmp/audit-work/semantic-llvm-kompiled")
INPUT_TERM = "cons(5,cons(8,cons(7,cons(1,nil))))"
TESTS = [
    {
        "name": "submitted",
        "program": Path("/tmp/audit-work/candidate-src/solution.mpy"),
        "expected": 12,
    },
    {
        "name": "body-zero",
        "program": Path("/audit-output/evidence/solution-body-zero.mpy"),
        "expected": 0,
    },
    {
        "name": "condition-false",
        "program": Path("/audit-output/evidence/solution-condition-false.mpy"),
        "expected": 0,
    },
]


def main() -> int:
    records = []
    failed = False
    for test in TESTS:
        command = [
            "krun",
            str(test["program"]),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={INPUT_TERM}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        match = re.search(r"result\s*\(\s*(-?\d+)\s*\)", completed.stdout)
        actual = int(match.group(1)) if match else None
        passed = completed.returncode == 0 and actual == test["expected"]
        failed |= not passed
        records.append(
            {
                **test,
                "program": str(test["program"]),
                "command": command,
                "exit_status": completed.returncode,
                "actual": actual,
                "passed": passed,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )
    print(json.dumps({"tests": records}, indent=2, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
