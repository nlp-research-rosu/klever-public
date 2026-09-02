#!/usr/bin/env python3
"""Run clean generated semantics and compare final results with both Pythons."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/36-fizz-buzz-audit-002")
WORK = SCRATCH / "candidate"
DEFINITION = WORK / "concrete-kompiled"
PROGRAM = WORK / "solution.mpy"


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


candidate = load_function("candidate_solution_stage3", WORK / "solution.py")
canonical = load_function(
    "trusted_canonical_stage3", SCRATCH / "trusted" / "canonical.py"
)
inputs = [-3, 0, 1, 11, 13, 77, 78, 79, 117, 178, 777]

for value in inputs:
    command = [
        "krun",
        str(PROGRAM),
        f"-cN={value}",
        "--definition",
        str(DEFINITION),
    ]
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command, cwd=WORK, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    print(f"EXIT_STATUS: {completed.returncode}")
    if completed.returncode != 0:
        print(completed.stdout)
        raise SystemExit(completed.returncode)

    match = re.search(r"<result>\s*(-?\d+)\s*</result>", completed.stdout)
    if match is None:
        print(completed.stdout)
        raise SystemExit(f"could not parse <result> for n={value}")
    k_result = int(match.group(1))
    candidate_result = candidate(value)
    canonical_result = canonical(value)
    print(
        f"n={value} k={k_result} candidate_python={candidate_result} "
        f"canonical_python={canonical_result}"
    )
    if not k_result == candidate_result == canonical_result:
        print(completed.stdout)
        raise SystemExit(1)

print(f"comparison_count={len(inputs)} mismatch_count=0")
