#!/usr/bin/env python3
"""Compare freshly built K semantics with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/122-add-elements")
DEFINITION = SCRATCH / "auditor-semantic-kompiled"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_list(values: list[int]) -> str:
    return " ".join(f"ListItem({value})" for value in values) or ".List"


canonical = load("trusted_canonical_for_k", SCRATCH / "canonical.py")
candidate = load("candidate_for_k", SCRATCH / "solution.py")
cases = [
    ("documented-example", [111, 21, 3, 4000, 5, 6, 7, 8, 9], 4, True),
    ("empty-outside-contract", [], 0, False),
    ("lower-negative-boundary", [-100, -99], 2, True),
    (
        "all-branch-boundaries",
        [-101, -100, -99, -10, -9, -1, 0, 9, 10, 99, 100, 101],
        12,
        True,
    ),
    ("length-100", list(range(-50, 50)), 100, True),
]

failures = 0
for name, arr, k, in_domain in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARR={k_list(arr)}",
        f"-cN={k}",
    ]
    print("$", " ".join(repr(part) if " " in part else part for part in command))
    run = subprocess.run(command, cwd=SCRATCH, text=True, capture_output=True)
    print(f"KRUN_EXIT_STATUS={run.returncode}")
    print(run.stdout.rstrip())
    if run.stderr:
        print("STDERR:")
        print(run.stderr.rstrip())
    matches = re.findall(r"<result>\s*result\s*\(\s*(-?\d+)\s*\)\s*</result>", run.stdout)
    k_value = int(matches[-1]) if matches else None
    candidate_value = candidate.add_elements(arr, k)
    canonical_value = canonical.add_elements(arr, k)
    print(
        f"comparison {name}: K={k_value} candidate_python={candidate_value} "
        f"canonical_python={canonical_value} in_domain={in_domain} "
        f"K_matches_candidate={k_value == candidate_value} "
        f"K_matches_canonical={k_value == canonical_value}"
    )
    if run.returncode != 0 or k_value != candidate_value:
        failures += 1

print(f"k_candidate_comparison_failures={failures}")
raise SystemExit(1 if failures else 0)
