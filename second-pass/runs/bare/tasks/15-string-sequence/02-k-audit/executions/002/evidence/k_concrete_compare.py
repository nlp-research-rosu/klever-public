#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both independent Python implementations."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
DEFINITION = SCRATCH / "semantic-llvm-kompiled"
INPUTS = [-3, -1, 0, 1, 5, 12, 50]


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load_entry("trusted_canonical_k_compare", Path("/reference/canonical.py"))
candidate = load_entry("candidate_k_compare", SCRATCH / "solution.py")
env = os.environ.copy()
env["PYTHONDONTWRITEBYTECODE"] = "1"
result_pattern = re.compile(r'SVal\s*\(\s*("(?:\\.|[^"\\])*")\s*\)\s*~>\s*\.K')

print("COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 "
      "/audit-output/evidence/k_concrete_compare.py")
print(f"definition={DEFINITION}")
print(f"inputs={json.dumps(INPUTS)}")
mismatches = []
for value in INPUTS:
    command = [
        "krun",
        "solution.mpy",
        f"-cARG={value}",
        "--definition",
        str(DEFINITION),
    ]
    print("COMMAND: cd /tmp/audit-work/reconstruction && " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    print(f"krun_exit={completed.returncode}")
    match = result_pattern.search(completed.stdout)
    if completed.returncode != 0 or match is None:
        print("stdout=" + completed.stdout[:4000])
        print("stderr=" + completed.stderr[:4000])
        mismatches.append({"n": value, "reason": "execution or parse failure"})
        continue
    k_value = json.loads(match.group(1))
    canonical_value = canonical(value)
    candidate_value = candidate(value)
    print(
        f"n={value}; k={k_value!r}; canonical={canonical_value!r}; "
        f"candidate={candidate_value!r}"
    )
    if not (k_value == canonical_value == candidate_value):
        mismatches.append(
            {
                "n": value,
                "k": k_value,
                "canonical": canonical_value,
                "candidate": candidate_value,
            }
        )
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print("mismatches=" + json.dumps(mismatches))
    raise SystemExit(1)
print("SCRIPT_EXIT=0")
