#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/159-eat-audit")
REBUILD = ROOT / "rebuild"


def import_from(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = import_from(ROOT / "trusted/canonical.py", "k_compare_canonical")
generated = import_from(REBUILD / "solution.py", "k_compare_solution")

cases = [
    (5, 6, 10),        # prompt normal, enough carrots
    (2, 11, 5),        # prompt normal, insufficient carrots
    (0, 0, 0),         # all lower bounds and equality branch
    (1000, 0, 1000),   # maximum stock, zero need
    (1000, 1000, 1000),# all upper bounds and equality branch
    (1000, 1000, 0),   # upper eaten/need, zero stock
    (37, 499, 500),    # immediately below a representative boundary
    (37, 500, 500),    # representative equality boundary
    (37, 501, 500),    # immediately above a representative boundary
]

pattern = re.compile(r"result\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")
mismatches: list[str] = []

for number, need, remaining in cases:
    args = f"args({number}, {need}, {remaining})"
    command = [
        "/usr/bin/krun",
        "solution.mpy",
        "--definition",
        "concrete-kompiled",
        f"-cARGS={args}",
    ]
    print("$ " + shlex.join(command))
    completed = subprocess.run(
        command,
        cwd=REBUILD,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    print(f"[exit={completed.returncode}]")
    match = pattern.search(completed.stdout)
    k_value = [int(match.group(1)), int(match.group(2))] if match else None
    canonical_value = canonical.eat(number, need, remaining)
    generated_value = generated.eat(number, need, remaining)
    print(
        f"compare input={[number, need, remaining]} k={k_value} "
        f"canonical={canonical_value} generated={generated_value}"
    )
    if (
        completed.returncode != 0
        or k_value != canonical_value
        or k_value != generated_value
    ):
        mismatches.append(
            f"{[number, need, remaining]}: k={k_value} "
            f"canonical={canonical_value} generated={generated_value}"
        )

print(f"cases={len(cases)} mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch}")
sys.exit(1 if mismatches else 0)
