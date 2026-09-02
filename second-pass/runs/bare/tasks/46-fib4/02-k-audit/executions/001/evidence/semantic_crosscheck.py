#!/usr/bin/env python3
"""Compare fresh LLVM K execution with independent Python execution."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/46-fib4")
SOLUTION = SCRATCH / "solution.py"
PROGRAM = SCRATCH / "solution.mpy"
DEFINITION = SCRATCH / "semantic-llvm-kompiled"
INPUTS = [0, 1, 2, 3, 4, 5, 6, 7, 10, 20]


def load_fib4():
    spec = importlib.util.spec_from_file_location("scratch_solution_for_k", SOLUTION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SOLUTION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


def main() -> int:
    fib4 = load_fib4()
    records = []
    mismatches = 0
    for n in INPUTS:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cARG={n}",
        ]
        print("COMMAND:", " ".join(command), flush=True)
        proc = subprocess.run(command, text=True, capture_output=True, timeout=60)
        print(proc.stdout, end="")
        if proc.stderr:
            print("STDERR:")
            print(proc.stderr, end="")
        print(f"EXIT: {proc.returncode}")
        match = re.search(r"<result>\s*result\s*\(\s*(-?\d+)\s*\)\s*</result>", proc.stdout)
        k_value = int(match.group(1)) if match else None
        python_value = fib4(n)
        equal = proc.returncode == 0 and k_value == python_value
        if not equal:
            mismatches += 1
        records.append(
            {
                "n": n,
                "python": python_value,
                "k": k_value,
                "krun_exit": proc.returncode,
                "equal": equal,
            }
        )
    print(
        json.dumps(
            {
                "inputs": INPUTS,
                "records": records,
                "mismatch_count": mismatches,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
