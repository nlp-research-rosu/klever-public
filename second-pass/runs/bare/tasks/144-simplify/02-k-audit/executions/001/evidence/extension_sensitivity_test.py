#!/usr/bin/env python3
"""Compare base and proof-extended semantics on complete observable states."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


PROGRAM = Path("/tmp/audit-work/review-144/source/solution.mpy")
BASE = Path("/tmp/audit-work/review-144/build/semantic-kompiled")
EXTENDED = Path("/tmp/audit-work/review-144/build/verification-kompiled")


def run(definition: Path, x: str, n: str):
    args = f"strVal({json.dumps(x)}),strVal({json.dumps(n)})"
    command = [
        "krun",
        str(PROGRAM),
        f"-cARGS={args}",
        "--definition",
        str(definition),
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    return command, completed


def main() -> int:
    cases = [
        ("true", "1/5", "5/1"),
        ("false", "1/6", "2/1"),
        ("minimum", "1/1", "1/1"),
        ("large_false", "9007199254740993/2", "1/1"),
        ("large_true", "9007199254740993/3", "3/1"),
    ]
    failures = []
    for label, x, n in cases:
        base_command, base_run = run(BASE, x, n)
        extended_command, extended_run = run(EXTENDED, x, n)
        same = (
            base_run.returncode == extended_run.returncode == 0
            and base_run.stdout == extended_run.stdout
            and base_run.stderr == extended_run.stderr
        )
        print(f"case={label}")
        print(f"base_command={base_command!r}")
        print(f"extended_command={extended_command!r}")
        print(f"base_exit={base_run.returncode}")
        print(f"extended_exit={extended_run.returncode}")
        print(f"complete_stdout_equal={base_run.stdout == extended_run.stdout}")
        print(f"complete_stderr_equal={base_run.stderr == extended_run.stderr}")
        print(f"complete_observable_state_equal={same}")
        if not same:
            failures.append(label)
            print(f"base_stdout={base_run.stdout!r}")
            print(f"extended_stdout={extended_run.stdout!r}")
            print(f"base_stderr={base_run.stderr!r}")
            print(f"extended_stderr={extended_run.stderr!r}")
    print(f"case_count={len(cases)}")
    print(f"failure_count={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
