#!/usr/bin/env python3
"""Compare fresh concrete K execution with two independent Python executions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction-135")
DEFINITION = WORK / "concrete-fresh-kompiled"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


canonical = load(Path("/reference/canonical.py"), "concrete_oracle_canonical")
generated = load(WORK / "solution.py", "concrete_oracle_generated")

cases = [
    ("empty", []),
    ("singleton", [9]),
    ("two_ascending", [1, 2]),
    ("two_descending", [2, 1]),
    ("documented_drop", [1, 2, 4, 3, 5]),
    ("documented_sorted", [1, 2, 3]),
    ("multiple_drops", [5, 1, 4, 2, 3]),
    ("negative_values", [-1, -5, -3, -9]),
]

result_pattern = re.compile(
    r"value\s*\(\s*intVal\s*\(\s*(-?\d+)\s*\)\s*\)"
)
mismatches = 0
for label, values in cases:
    members = ",".join(str(value) for value in values)
    args = f"arrayVal(seq({members}),0,{len(values)})"
    command = [
        "krun",
        str(WORK / "solution.regenerated.mpy"),
        f"-cARGS={args}",
        "--definition",
        str(DEFINITION),
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    matches = result_pattern.findall(completed.stdout)
    k_result = int(matches[-1]) if completed.returncode == 0 and matches else None
    canonical_result = canonical(values)
    generated_result = generated(values)
    agrees = (
        completed.returncode == 0
        and k_result == canonical_result
        and k_result == generated_result
    )
    mismatches += int(not agrees)
    print(
        f"CASE label={label} input={values!r} command={command!r} "
        f"krun_exit={completed.returncode} k={k_result!r} "
        f"canonical={canonical_result!r} generated={generated_result!r} "
        f"agree={agrees}"
    )
    if not agrees:
        print(f"KRUN_OUTPUT_BEGIN\n{completed.stdout}\nKRUN_OUTPUT_END")

print(f"SUMMARY cases={len(cases)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
