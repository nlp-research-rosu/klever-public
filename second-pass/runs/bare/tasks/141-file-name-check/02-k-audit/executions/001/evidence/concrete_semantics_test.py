#!/usr/bin/env python3
"""Compare fresh LLVM K execution with the submitted Python implementation."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


def load_entry(path: Path):
    spec = importlib.util.spec_from_file_location("submitted_solution_concrete", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: concrete_semantics_test.py SOLUTION.py SOLUTION.mpy DEFINITION"
        )
    solution_py = Path(sys.argv[1])
    solution_mpy = Path(sys.argv[2])
    definition = Path(sys.argv[3])
    python_entry = load_entry(solution_py)
    cases = [
        "example.txt",
        "1example.dll",
        "",
        "a",
        ".txt",
        "a.txt",
        "a..txt",
        "a.b.txt",
        "a.exe",
        "A.dll",
        "a.py",
        "a1b2c3.exe",
        "a1b2c3d4.exe",
        "@.txt",
        "A.txt",
        "Z.txt",
        "[.txt",
        "`.txt",
        "z.txt",
        "{.txt",
        "a\x00.txt",
    ]
    mismatches = 0
    print(f"CASE_COUNT={len(cases)}")
    for index, value in enumerate(cases):
        input_term = json.dumps(value, ensure_ascii=True)
        command = [
            "krun",
            str(solution_mpy),
            "--definition",
            str(definition),
            "-cINPUT=" + input_term,
        ]
        print("COMMAND:", " ".join(repr(arg) for arg in command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"KRUN_EXIT_STATUS={completed.returncode}")
        if completed.stdout:
            print("KRUN_STDOUT_BEGIN")
            print(completed.stdout.rstrip())
            print("KRUN_STDOUT_END")
        if completed.stderr:
            print("KRUN_STDERR_BEGIN")
            print(completed.stderr.rstrip())
            print("KRUN_STDERR_END")
        match = re.search(r'VStr\s*\(\s*"(Yes|No)"\s*\)', completed.stdout)
        k_result = match.group(1) if match else None
        python_result = python_entry(value)
        ok = completed.returncode == 0 and k_result == python_result
        if not ok:
            mismatches += 1
        print(
            f"CASE {index:02d} input={value!r} "
            f"python={python_result!r} k={k_result!r} match={ok}"
        )
    print(f"MISMATCH_COUNT={mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
