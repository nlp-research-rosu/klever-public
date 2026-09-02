#!/usr/bin/env python3
"""Compare freshly compiled generated K semantics with direct Python execution."""
import importlib.util
import re
import subprocess
from pathlib import Path

BUILD = Path("/tmp/audit-work/build")
DEFINITION = BUILD / "llvm-audit-kompiled"

spec = importlib.util.spec_from_file_location("generated_solution_for_krun", BUILD / "solution.py")
solution = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(solution)

cases = [
    ("negative-early-return", -1, 13, 29),
    ("zero-early-return", 0, 13, 29),
    ("one-early-return", 1, 13, 29),
    ("smallest-prime-loop-zero", 2, 13, 29),
    ("prime-loop-zero", 3, 13, 29),
    ("first-composite", 4, 13, 29),
    ("nondividing-then-dividing", 9, 13, 29),
    ("later-divisor", 25, 13, 29),
    ("prime-multiple-iterations", 97, 13, 29),
    ("square-boundary", 121, 13, 29),
]

mismatches = []
for label, n, x, y in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cN={n}",
        f"-cX={x}",
        f"-cY={y}",
    ]
    completed = subprocess.run(command, cwd=BUILD, text=True, capture_output=True)
    combined = completed.stdout + completed.stderr
    match = re.search(r"<result>\s*intVal\s*\(\s*(-?\d+)\s*\)", combined, re.DOTALL)
    k_value = int(match.group(1)) if match else None
    python_value = solution.x_or_y(n, x, y)
    ok = completed.returncode == 0 and k_value == python_value
    print(
        f"{label}: n={n} x={x} y={y} "
        f"krun_exit={completed.returncode} k_result={k_value} python_result={python_value} match={ok}"
    )
    if not ok:
        mismatches.append((label, command, combined))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
for label, command, output in mismatches:
    print("MISMATCH", label, command)
    print(output[-4000:])
raise SystemExit(1 if mismatches else 0)
