#!/usr/bin/env python3
"""Run fresh LLVM K semantics and compare results to both Python programs."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


canonical = load_entry(
    "trusted_canonical_for_k", Path("/tmp/audit-work/reference-src/canonical.py")
)
generated = load_entry(
    "submitted_solution_for_k", Path("/tmp/audit-work/candidate-src/solution.py")
)

workdir = Path("/tmp/audit-work/rebuild")
cases = [0, 1, 2, 3, 5, 8, 10, 15, 20]
print(f"cases={cases}")

mismatches = []
for n in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "concrete-kompiled",
        f"-cN={n}",
    ]
    print("$ " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=workdir,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    print(f"exit={completed.returncode}")
    match = re.search(r"<result>\s*(-?[0-9]+)\s*</result>", completed.stdout)
    if completed.returncode != 0 or match is None:
        mismatches.append((n, "K execution/parse failure"))
        continue
    k_value = int(match.group(1))
    canonical_value = canonical(n)
    generated_value = generated(n)
    equal = k_value == canonical_value == generated_value
    print(
        f"comparison n={n} k={k_value} canonical={canonical_value} "
        f"generated={generated_value} equal={equal}"
    )
    if not equal:
        mismatches.append((n, k_value, canonical_value, generated_value))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    print(f"mismatch_details={mismatches}")
    raise SystemExit(1)
