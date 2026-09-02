#!/usr/bin/env python3
"""Compare fresh generated-semantics runs with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/rebuild")
INPUTS = [0, 1, 2, 3, 4, 5, 6, 10, 11, 100]


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


candidate = load_entry("scratch_candidate", WORK / "solution.py")
canonical = load_entry("trusted_canonical_for_krun", Path("/reference/canonical.py"))

for n in INPUTS:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "audit-runtime-kompiled",
        f"-cN={n}",
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print("EXIT:", completed.returncode)
    print(completed.stdout.rstrip())
    assert completed.returncode == 0
    matches = re.findall(r"result\s*\(\s*(-?\d+)\s*\)", completed.stdout)
    assert len(matches) == 1, (n, matches, completed.stdout)
    k_result = int(matches[0])
    candidate_result = candidate(n)
    canonical_result = canonical(n)
    print(
        f"COMPARE n={n}: K={k_result} candidate={candidate_result} "
        f"canonical={canonical_result}"
    )
    assert k_result == candidate_result == canonical_result

print("FRESH CONCRETE SEMANTICS COMPARISON: PASS")
