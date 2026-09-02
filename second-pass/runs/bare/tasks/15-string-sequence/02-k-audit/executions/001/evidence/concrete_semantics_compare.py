#!/usr/bin/env python3
"""Compare fresh generated-semantics execution to both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load_entry(Path("/reference/canonical.py"), "concrete_canonical")
candidate = load_entry(Path("/tmp/audit-work/rebuild/solution.py"), "concrete_candidate")
cwd = Path("/tmp/audit-work/rebuild")
program = cwd / "regenerated-solution.mpy"
definition = cwd / "semantic-llvm-kompiled"
inputs = [-3, -1, 0, 1, 5, 12]
pattern = re.compile(r"<k>\s*SVal\s*\(\s*(\"(?:[^\"\\]|\\.)*\")\s*\)", re.DOTALL)
mismatches = []

for n in inputs:
    command = [
        "krun",
        str(program),
        f"-cARG={n}",
        "--definition",
        str(definition),
    ]
    run = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    print(f"COMMAND: {shlex.join(command)}")
    print(f"EXIT_STATUS: {run.returncode}")
    if run.returncode != 0:
        print(run.stdout)
        print(run.stderr)
        mismatches.append((n, "krun failure", run.returncode))
        continue
    match = pattern.search(run.stdout)
    if match is None:
        print(run.stdout)
        mismatches.append((n, "unparseable final <k>", None))
        continue
    k_value = json.loads(match.group(1))
    canonical_value = canonical(n)
    candidate_value = candidate(n)
    equal = k_value == canonical_value == candidate_value
    print(
        f"n={n} k={k_value!r} canonical={canonical_value!r} "
        f"candidate={candidate_value!r} equal={equal}"
    )
    if not equal:
        mismatches.append((n, k_value, canonical_value, candidate_value))

print(f"inputs={inputs}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch!r}")
raise SystemExit(1 if mismatches else 0)
