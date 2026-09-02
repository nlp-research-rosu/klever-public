#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with Python executions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


submitted = load_module(
    "submitted_solution",
    Path("/tmp/audit-work/rebuild/candidate-src/solution.py"),
)
canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))

program = "/tmp/audit-work/rebuild/candidate-src/solution.mpy"
definition = "/tmp/audit-work/rebuild/candidate-src/semantic-fresh-kompiled"
inputs = [-12, 123, 0, -1, 1, -2, 2, -10, 10, 101, 222]
pair_pattern = re.compile(
    r"<result>\s*pairVal\s*\(\s*intVal\s*\(\s*(-?\d+)\s*\)\s*,"
    r"\s*intVal\s*\(\s*(-?\d+)\s*\)\s*\)\s*</result>",
    re.DOTALL,
)

failures = 0
for value in inputs:
    command = ["krun", program, "--definition", definition, f"-cNUM={value}"]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    print("$ " + " ".join(command))
    print(f"[exit {completed.returncode}]")
    if completed.stderr:
        print(completed.stderr.rstrip())
    match = pair_pattern.search(completed.stdout)
    if completed.returncode != 0 or match is None:
        print("parse_status=FAILED")
        print(completed.stdout.rstrip())
        failures += 1
        continue
    k_result = (int(match.group(1)), int(match.group(2)))
    submitted_result = submitted.even_odd_count(value)
    canonical_result = canonical.even_odd_count(value)
    agrees = k_result == submitted_result
    print(
        f"input={value} k={k_result!r} submitted_python={submitted_result!r} "
        f"canonical_python={canonical_result!r} "
        f"k_matches_submitted={str(agrees).lower()}"
    )
    if not agrees:
        failures += 1

print(f"case_count={len(inputs)}")
print(f"k_vs_submitted_failure_count={failures}")
sys.exit(1 if failures else 0)
