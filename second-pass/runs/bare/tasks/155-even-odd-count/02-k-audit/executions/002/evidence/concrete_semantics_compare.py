#!/usr/bin/env python3
"""Compare fresh K execution with independent Python executions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/155-even-odd-count-audit/reconstruction")
SOLUTION = Path("/tmp/audit-work/155-even-odd-count-audit/source/solution.py")


def load_entry(path: Path):
    spec = importlib.util.spec_from_file_location("candidate_for_semantics", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_count


python_entry = load_entry(SOLUTION)
result_pattern = re.compile(
    r"<result>\s*pairVal \( intVal \( (-?\d+) \) , "
    r"intVal \( (-?\d+) \) \)\s*</result>",
    re.MULTILINE,
)
cases = [-12, 123, 0, -1, 1, -2, 2, 9, 10, 11, -78, 346211]

print(f"definition={ROOT / 'semantic-fresh-kompiled'}")
print(f"program={ROOT / 'solution.mpy'}")
print(f"inputs={cases}")
mismatches = 0
for value in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "semantic-fresh-kompiled",
        f"-cNUM={value}",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    print(f"command={' '.join(command)}")
    print(f"krun_exit_status={completed.returncode}")
    if completed.stderr:
        print(f"krun_stderr={completed.stderr.rstrip()}")
    match = result_pattern.search(completed.stdout)
    k_result = (int(match.group(1)), int(match.group(2))) if match else None
    py_result = python_entry(value)
    print(f"input={value} k_result={k_result} python_result={py_result}")
    if completed.returncode != 0 or k_result != py_result:
        mismatches += 1

print(f"mismatch_count={mismatches}")
if mismatches:
    raise SystemExit(1)
