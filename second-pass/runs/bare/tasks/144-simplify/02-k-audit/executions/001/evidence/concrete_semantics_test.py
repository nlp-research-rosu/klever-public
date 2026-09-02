#!/usr/bin/env python3
"""Run the fresh base semantics and compare it with independent Python."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


SOLUTION_PATH = Path("/tmp/audit-work/review-144/source/solution.py")
PROGRAM_PATH = Path("/tmp/audit-work/review-144/source/solution.mpy")
DEFINITION_PATH = Path(
    "/tmp/audit-work/review-144/build/semantic-kompiled"
)


def load_solution():
    spec = importlib.util.spec_from_file_location("solution_for_k_comparison", SOLUTION_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SOLUTION_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def k_string(text: str) -> str:
    return json.dumps(text)


def main() -> int:
    solution = load_solution()
    cases = [
        ("example_true", "1/5", "5/1"),
        ("example_false_one", "1/6", "2/1"),
        ("example_false_two", "7/10", "10/2"),
        ("minimum_positive", "1/1", "1/1"),
        ("remainder_zero_boundary", "1/2", "2/1"),
        ("remainder_nonzero_boundary", "1/2", "3/1"),
        ("cross_cancel_true", "2/3", "3/2"),
        ("ordinary_false", "17/19", "23/29"),
        ("large_precision_boundary", "9007199254740993/2", "1/1"),
        ("large_true", "9007199254740993/3", "3/1"),
        ("large_denominator", "1/9007199254740993", "1/1"),
        ("very_large_integer", f"{10**400}/3", "1/1"),
    ]
    failures = []
    for label, x, n in cases:
        expected = solution(x, n)
        args = f"strVal({k_string(x)}),strVal({k_string(n)})"
        command = [
            "krun",
            str(PROGRAM_PATH),
            f"-cARGS={args}",
            "--definition",
            str(DEFINITION_PATH),
        ]
        run = subprocess.run(command, text=True, capture_output=True, check=False)
        match = re.search(
            r"result\s*\(\s*boolVal\s*\(\s*(true|false)\s*\)\s*\)",
            run.stdout,
        )
        actual = None if match is None else match.group(1) == "true"
        print(f"case={label}")
        print(f"command={shlex.join(command)}")
        print(f"input={(x, n)!r}")
        print(f"python_result={expected!r}")
        print(f"k_exit={run.returncode}")
        print(f"k_result={actual!r}")
        if run.returncode != 0 or actual != expected:
            failures.append(label)
            print(f"k_stdout={run.stdout!r}")
            print(f"k_stderr={run.stderr!r}")

    print(f"case_count={len(cases)}")
    print(f"failure_count={len(failures)}")
    print(f"failures={failures!r}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
