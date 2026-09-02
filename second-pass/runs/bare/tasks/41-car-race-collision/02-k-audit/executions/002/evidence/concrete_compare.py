#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python functions."""

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
    return module.car_race_collision


canonical = load_entry("trusted_canonical_k_compare", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_solution_k_compare", Path("/tmp/audit-work/candidate/solution.py")
)

definition = Path("/tmp/audit-work/candidate/concrete-kompiled")
program = Path("/tmp/audit-work/candidate/solution.mpy")
cases = [0, 1, 3, 10, 41, -1]
mismatches = []

for n in cases:
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cN={n}",
    ]
    print("$", " ".join(command))
    completed = subprocess.run(
        command,
        cwd="/tmp/audit-work/candidate",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    print(f"[exit {completed.returncode}]")
    match = re.search(r"<result>\s*(-?[0-9]+)\s*</result>", completed.stdout)
    if completed.returncode != 0 or match is None:
        mismatches.append((n, "execution-or-parse-failure"))
        continue
    k_result = int(match.group(1))
    canonical_result = canonical(n)
    candidate_result = candidate(n)
    print(
        f"comparison n={n} "
        f"k={k_result} canonical={canonical_result} candidate={candidate_result}"
    )
    if k_result != canonical_result or k_result != candidate_result:
        mismatches.append((n, k_result, canonical_result, candidate_result))

print(f"cases={cases}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print("mismatches", mismatches)
    raise SystemExit(1)
