#!/usr/bin/env python3
"""Compare freshly rebuilt K execution with independent generated Python."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_generated():
    path = Path("/tmp/audit-work/source/solution.py")
    spec = importlib.util.spec_from_file_location("generated_solution_for_k", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


generated = load_generated()
definition = "/tmp/audit-work/source/fresh-semantic-kompiled"
program = "/tmp/audit-work/source/solution.mpy"
cases = [
    (-1, 2),
    (0, 2),
    (1, -2),
    (1, 1),
    (1, 4),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, -2),
    (5, 3),
    (8, 2),
    (9, 3),
    (10, 3),
    (64, 4),
    (65, 4),
]

rows = []
errors = []
for x, n in cases:
    command = [
        "krun",
        program,
        f"-cX={x}",
        f"-cN={n}",
        "--definition",
        definition,
    ]
    completed = subprocess.run(command, text=True, capture_output=True, timeout=30)
    match = re.search(r"<result>\s*(true|false)\s*</result>", completed.stdout)
    k_value = None if match is None else match.group(1) == "true"
    py_value = generated(x, n)
    row = (x, n, completed.returncode, k_value, py_value)
    rows.append(row)
    if completed.returncode != 0 or match is None or k_value != py_value:
        errors.append(
            {
                "row": row,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )

print("columns=(x,n,krun_exit,k_result,generated_python_result)")
for row in rows:
    print(row)
print(f"case_count={len(rows)}")
print(f"mismatch_or_execution_error_count={len(errors)}")
for error in errors:
    print(error)

if errors:
    raise SystemExit(1)
