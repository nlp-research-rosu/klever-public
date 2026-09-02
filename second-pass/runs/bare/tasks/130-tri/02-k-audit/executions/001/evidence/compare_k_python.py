#!/usr/bin/env python3
"""Parse fresh krun results and compare them with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/130-tri")
DEFINITION = ROOT / "build" / "concrete-kompiled"
PROGRAM = ROOT / "candidate" / "solution.mpy"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_for_k", ROOT / "reference" / "canonical.py")
candidate = load("submitted_solution_for_k", ROOT / "candidate" / "solution.py")


def k_run(n: int):
    command = [
        "krun",
        str(PROGRAM),
        f"-cN={n}",
        "--definition",
        str(DEFINITION),
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    values = [int(value) for value in re.findall(r"cons\s*\(\s*(-?\d+)", completed.stdout)]
    returned = "returned" in completed.stdout and completed.returncode == 0
    return command, completed.returncode, returned, values, completed.stderr.strip()


def python_run(function, n: int):
    try:
        return "return", function(n)
    except Exception as error:
        return "raise", f"{type(error).__name__}: {error}"


overall = True
for n in [0, 1, 2, 3, 6, 10]:
    command, status, returned, k_values, stderr = k_run(n)
    canonical_status, canonical_value = python_run(canonical.tri, n)
    candidate_status, candidate_value = python_run(candidate.tri, n)
    equal = (
        status == 0
        and returned
        and canonical_status == "return"
        and candidate_status == "return"
        and k_values == canonical_value
        and k_values == candidate_value
    )
    overall = overall and equal
    print(
        "normal_case=",
        {
            "n": n,
            "command": command,
            "krun_status": status,
            "k_values": k_values,
            "canonical_status": canonical_status,
            "candidate_status": candidate_status,
            "equal": equal,
            "stderr": stderr,
        },
    )

# This is not counted as a normal-case mismatch: it records an adequacy boundary
# of the generated semantics versus the actual CPython execution environment.
n = 998
command, status, returned, k_values, stderr = k_run(n)
canonical_status, canonical_value = python_run(canonical.tri, n)
candidate_status, candidate_value = python_run(candidate.tri, n)
print(
    "resource_case=",
    {
        "n": n,
        "command": command,
        "krun_status": status,
        "k_returned": returned,
        "k_len": len(k_values),
        "k_last": k_values[-1] if k_values else None,
        "canonical_status": canonical_status,
        "canonical_len": len(canonical_value) if canonical_status == "return" else None,
        "candidate_status": candidate_status,
        "candidate_result": (
            candidate_value if candidate_status == "raise" else f"list[{len(candidate_value)}]"
        ),
        "stderr": stderr,
    },
)

raise SystemExit(0 if overall else 1)
