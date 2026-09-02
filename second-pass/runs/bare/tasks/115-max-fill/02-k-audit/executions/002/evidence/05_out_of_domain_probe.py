#!/usr/bin/env python3
"""Witness the generated semantics' documented out-of-contract // limitation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shlex
import subprocess


WORK = Path("/tmp/audit-work/reconstruction")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_fill


canonical = load_entry(WORK / "reference/canonical.py", "negative_canonical")
candidate = load_entry(WORK / "solution.py", "negative_candidate")

grid = [[-2]]
capacity = 2
command = [
    "krun",
    "solution.mpy",
    "--definition",
    str(WORK / "semantic-clean-kompiled"),
    "-cARGS=gridVal(rowVal(-2)),intVal(2)",
]
completed = subprocess.run(
    command,
    cwd=WORK,
    capture_output=True,
    text=True,
    timeout=120,
)
output = completed.stdout + completed.stderr
matches = re.findall(
    r"<result>\s*intVal\s*\(\s*(-?\d+)\s*\)\s*</result>",
    output,
)
k_result = int(matches[-1]) if matches else None
canonical_result = canonical(grid, capacity)
candidate_result = candidate(grid, capacity)

print("OUT-OF-CONTRACT WITNESS: cells are not in {0,1}")
print(f"COMMAND: {shlex.join(command)}")
print(f"EXIT_STATUS: {completed.returncode}")
print(
    f"grid={grid!r} capacity={capacity} canonical={canonical_result} "
    f"candidate_python={candidate_result} generated_K={k_result}"
)
print("Python // floors; K /Int rounds toward zero.")
print("K_OUTPUT_BEGIN")
print(output.rstrip())
print("K_OUTPUT_END")

if not (
    completed.returncode == 0
    and canonical_result == -1
    and candidate_result == -1
    and k_result == 0
):
    raise SystemExit(1)
