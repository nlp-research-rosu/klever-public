#!/usr/bin/env python3
"""Concrete generated-semantics versus both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_concrete")
generated = load_entry(Path("/candidate/solution.py"), "candidate_solution_concrete")
work = Path("/tmp/audit-work/75-is-multiply-prime/work")
inputs = [-7, 0, 7, 8, 10, 29, 30, 31, 98, 99, 100]
mismatches = []

for value in inputs:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "concrete-kompiled",
        f"-cARG={value}",
    ]
    print("$", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"exit={completed.returncode}")
    print(completed.stdout.rstrip())
    match = re.search(
        r"<result>\s*Bool\s*\(\s*(true|false)\s*\)\s*</result>",
        completed.stdout,
    )
    if completed.returncode != 0 or match is None:
        raise RuntimeError(f"krun failed or result missing for {value}")
    k_result = match.group(1) == "true"
    candidate_result = generated(value)
    canonical_result = canonical(value)
    print(
        f"COMPARE input={value} K={k_result} "
        f"candidate={candidate_result} canonical={canonical_result}"
    )
    if not (k_result == candidate_result == canonical_result):
        mismatches.append((value, k_result, candidate_result, canonical_result))

print("inputs", inputs)
print("mismatch_count", len(mismatches))
if mismatches:
    print("mismatches", mismatches)
raise SystemExit(1 if mismatches else 0)
