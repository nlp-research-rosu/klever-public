#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with two Python executions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_prime_factor


canonical = load_entry(Path("/reference/canonical.py"), "semantics_oracle")
generated = load_entry(
    Path("/tmp/audit-work/review-59/src/solution.py"), "semantics_generated"
)
program = "/tmp/audit-work/review-59/src/solution.mpy"
definition = "/tmp/audit-work/review-59/build/semantic-llvm-kompiled"

# 4 is the smallest intended input; 25 reaches factor*factor == n; 8 repeats
# the true division branch; 15 first takes the false branch; the prompt
# examples are normal cases.  Prime 2 is outside the prompt domain but exercises
# the initial loop-false boundary covered by the candidate's stronger claim.
inputs = [4, 8, 15, 25, 2048, 13195, 2]
mismatches = []

for n in inputs:
    cmd = [
        "krun",
        program,
        "--definition",
        definition,
        f"-cN={n}",
        "--output",
        "pretty",
    ]
    print("COMMAND:", " ".join(cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    print(f"KRUN EXIT: {proc.returncode}")
    if proc.stderr:
        print("KRUN STDERR:")
        print(proc.stderr.rstrip())
    match = re.search(r"result\s*\(\s*(-?\d+)\s*\)", proc.stdout)
    k_value = int(match.group(1)) if match else None
    py_value = generated(n)
    oracle_value = canonical(n)
    print(
        f"n={n} K={k_value} generated_python={py_value} "
        f"canonical_python={oracle_value}"
    )
    if proc.returncode != 0 or k_value != py_value or k_value != oracle_value:
        mismatches.append((n, proc.returncode, k_value, py_value, oracle_value))

print(f"semantic mismatches: {len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", mismatch)
raise SystemExit(1 if mismatches else 0)
