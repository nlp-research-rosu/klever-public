#!/usr/bin/env python3
"""Compare fresh concrete K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/reconstruction")
CANDIDATE = ROOT / "candidate"
DEFINITION = CANDIDATE / "concrete-kompiled"
PROGRAM = CANDIDATE / "solution.mpy"


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical_k_compare", ROOT / "trusted/canonical.py")
subject = load_module("candidate_subject_k_compare", CANDIDATE / "solution.py")
inputs = [-3, -2, -1, 0, 1, 2, 30, 100]
k_subject_mismatches: list[tuple[int, int, int]] = []
k_canonical_mismatches: list[tuple[int, int, int]] = []

for n in inputs:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        '-cFUNCTION="sum_to_n"',
        f"-cARG={n}",
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"COMMAND[{n}]: {' '.join(command)}")
    print(f"EXIT_STATUS[{n}]: {completed.returncode}")
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        sys.exit(completed.returncode)
    match = re.search(r"<result>\s*(-?[0-9]+)\s*</result>", completed.stdout)
    if match is None:
        print(completed.stdout)
        raise RuntimeError(f"could not parse result for n={n}")
    k_value = int(match.group(1))
    subject_value = subject.sum_to_n(n)
    canonical_value = canonical.sum_to_n(n)
    print(
        f"RESULT n={n} K={k_value} "
        f"candidate_python={subject_value} canonical_python={canonical_value}"
    )
    if k_value != subject_value:
        k_subject_mismatches.append((n, k_value, subject_value))
    if k_value != canonical_value:
        k_canonical_mismatches.append((n, k_value, canonical_value))

print(f"inputs={inputs}")
print(f"K_vs_candidate_mismatches={len(k_subject_mismatches)} {k_subject_mismatches}")
print(f"K_vs_canonical_mismatches={len(k_canonical_mismatches)} {k_canonical_mismatches}")
if k_subject_mismatches:
    sys.exit(1)
