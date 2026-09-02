#!/usr/bin/env python3
"""Concrete alias/source equality and source body-sensitivity checks."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/46-fib4")
DEFINITION = SCRATCH / "semantic-llvm-kompiled"
PROGRAM = SCRATCH / "solution.mpy"
ALIAS = SCRATCH / "solution-alias.mpy"
MUTATED = SCRATCH / "solution-mutated.mpy"
INPUTS = [0, 2, 3, 4, 7, 10]


def run(program: Path, n: int) -> dict[str, object]:
    command = [
        "krun",
        str(program),
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
    return {
        "exit": proc.returncode,
        "result": int(match.group(1)) if match else None,
        "stdout": proc.stdout,
    }


def main() -> int:
    comparisons = []
    failures = 0
    for n in INPUTS:
        direct = run(PROGRAM, n)
        alias = run(ALIAS, n)
        same_full_configuration = direct == alias
        if not same_full_configuration:
            failures += 1
        comparisons.append(
            {
                "n": n,
                "direct_result": direct["result"],
                "alias_result": alias["result"],
                "same_full_configuration": same_full_configuration,
            }
        )

    original_at_2 = run(PROGRAM, 2)
    mutation_at_2 = run(MUTATED, 2)
    mutation_sensitive = (
        original_at_2["exit"] == 0
        and mutation_at_2["exit"] == 0
        and original_at_2["result"] == 2
        and mutation_at_2["result"] == 3
    )
    if not mutation_sensitive:
        failures += 1

    print(
        json.dumps(
            {
                "comparison_inputs": INPUTS,
                "alias_comparisons": comparisons,
                "body_mutation": {
                    "change": "n == 2 branch Return(Int(2)) -> Return(Int(3))",
                    "original_result": original_at_2["result"],
                    "mutated_result": mutation_at_2["result"],
                    "sensitive": mutation_sensitive,
                },
                "failure_count": failures,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
