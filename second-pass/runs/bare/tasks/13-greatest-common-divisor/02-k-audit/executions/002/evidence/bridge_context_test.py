#!/usr/bin/env python3
"""Compare fixed semantics with the loop-summary definition in continuations."""

from __future__ import annotations

import subprocess
from pathlib import Path

work = Path("/tmp/audit-work/reconstruction")
tests = [
    ("solution.mpy", 25, 15),
    ("solution.mpy", 7, 0),
    ("solution.mpy", -25, -15),
    ("bridge-continuation.mpy", 25, 15),
    ("bridge-continuation.mpy", 21, 14),
    ("bridge-continuation.mpy", 0, 0),
    ("bridge-continuation.mpy", -25, -15),
]


def run(program: str, definition: str, a: int, b: int) -> str:
    command = [
        "krun",
        program,
        "--definition",
        definition,
        f"-cA={a}",
        f"-cB={b}",
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"EXIT_STATUS: {completed.returncode}")
    if completed.returncode != 0:
        print(completed.stdout)
        raise SystemExit(f"krun failed: {command}")
    return completed.stdout


mismatches: list[tuple[str, int, int]] = []
for program, a, b in tests:
    fixed = run(program, "semantic-llvm-audit", a, b)
    bridged = run(program, "verification-haskell-audit", a, b)
    same = fixed == bridged
    print(
        f"COMPARISON program={program} input=({a},{b}) "
        f"complete_configuration_equal={same}"
    )
    if not same:
        print("FIXED:")
        print(fixed)
        print("BRIDGED:")
        print(bridged)
        mismatches.append((program, a, b))

print(f"comparison_count={len(tests)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    raise SystemExit(f"bridge mismatches: {mismatches}")
