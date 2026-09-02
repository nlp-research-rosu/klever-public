#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_a_pile


canonical = load_function("trusted_canonical_for_k", Path("/reference/canonical.py"))
candidate = load_function("candidate_for_k", Path("/candidate/solution.py"))
work = Path("/tmp/audit-work/100-make-a-pile")
program = work / "source/solution.mpy"
definition = work / "build/semantic-llvm-kompiled"
cases = [-1, 0, 1, 2, 3, 6, 10]
failures = 0

for n in cases:
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cN={n}",
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    result_match = re.search(r"<result>\s*(.*?)\s*</result>", completed.stdout, re.S)
    if result_match:
        result_cell = result_match.group(1)
        k_values = [int(value) for value in re.findall(r"VInt\s*\(\s*(-?\d+)\s*\)", result_cell)]
    else:
        result_cell = "<missing>"
        k_values = []
    canonical_values = canonical(n)
    candidate_values = candidate(n)
    match = (
        completed.returncode == 0
        and result_match is not None
        and k_values == canonical_values == candidate_values
    )
    failures += int(not match)
    print(
        json.dumps(
            {
                "command": command,
                "n": n,
                "krun_exit": completed.returncode,
                "k_result_cell": result_cell,
                "k_values": k_values,
                "canonical_values": canonical_values,
                "candidate_values": candidate_values,
                "all_match": match,
                "stderr": completed.stderr,
            },
            sort_keys=True,
        )
    )

print(json.dumps({"cases": cases, "failures": failures}, sort_keys=True))
sys.exit(1 if failures else 0)
