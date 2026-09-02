#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/63-fibfib")
CANDIDATE = SCRATCH / "candidate-src"
TRUSTED = SCRATCH / "trusted"
DEFINITION = CANDIDATE / "concrete-kompiled"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("concrete_trusted_canonical", TRUSTED / "canonical.py")
submitted = load_module("concrete_submitted_solution", CANDIDATE / "solution.py")

cases = [0, 1, 2, 3, 5, 8, 10, 20]
mismatches = []
for n in cases:
    command = [
        "krun",
        "solution.mpy",
        f"-cN={n}",
        "--definition",
        str(DEFINITION),
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=CANDIDATE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    match = re.search(r"<result>\s*(-?\d+)\s*</result>", completed.stdout)
    k_value = int(match.group(1)) if match else None
    canonical_value = canonical.fibfib(n)
    submitted_value = submitted.fibfib(n)
    agrees = (
        completed.returncode == 0
        and k_value == canonical_value
        and k_value == submitted_value
    )
    print(
        f"n={n} exit={completed.returncode} k={k_value}"
        f" canonical={canonical_value} submitted={submitted_value}"
        f" match={agrees}"
    )
    if not agrees:
        print("K_OUTPUT_BEGIN")
        print(completed.stdout[-6000:])
        print("K_OUTPUT_END")
        mismatches.append(n)

print(f"case_count={len(cases)} mismatch_count={len(mismatches)}")
raise SystemExit(0 if not mismatches else 1)
