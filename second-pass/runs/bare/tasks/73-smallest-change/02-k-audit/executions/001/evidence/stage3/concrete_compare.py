#!/usr/bin/env python3
"""Compare fresh generated K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import os
import re
import shlex
import subprocess
from collections.abc import Callable


def load_entry(path: str, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


def k_list(values: list[int]) -> str:
    if not values:
        return ".List"
    return " ".join(f"ListItem({value})" for value in values)


candidate = load_entry(
    "/tmp/audit-work/73-smallest-change/solution.py", "candidate_concrete"
)
canonical = load_entry("/reference/canonical.py", "canonical_concrete")
definition = os.environ.get(
    "AUDIT_K_DEFINITION",
    "/tmp/audit-work/73-smallest-change/semantic-haskell-kompiled",
)
program = "/tmp/audit-work/73-smallest-change/solution.mpy"

cases = [
    ("empty", []),
    ("singleton", [-7]),
    ("equal-pair", [4, 4]),
    ("unequal-pair", [4, 5]),
    ("odd-equal-ends", [1, 9, 1]),
    ("odd-unequal-ends", [1, 9, 2]),
    ("nested-mismatch", [-1, 2, 3, -1]),
    ("prompt-1", [1, 2, 3, 5, 4, 7, 9, 6]),
    ("prompt-2", [1, 2, 3, 4, 3, 2, 2]),
    ("prompt-3", [1, 2, 3, 2, 1]),
]

failures = 0
for name, values in cases:
    command = [
        "krun",
        program,
        f"-cINPUT={k_list(values)}",
        "--definition",
        definition,
    ]
    print(f"CASE: {name}")
    print(f"INPUT: {values!r}")
    print(f"COMMAND: {shlex.join(command)}")
    run = subprocess.run(command, text=True, capture_output=True, check=False)
    print(run.stdout, end="")
    if run.stderr:
        print("STDERR:")
        print(run.stderr, end="")
    print(f"KRUN_EXIT_STATUS: {run.returncode}")

    match = re.search(r"<result>\s*(-?[0-9]+)", run.stdout)
    k_value = int(match.group(1)) if match else None
    candidate_value = candidate(values)
    canonical_value = canonical(values)
    print(
        f"VALUES: K={k_value!r} candidate_python={candidate_value!r} "
        f"canonical_python={canonical_value!r}"
    )
    passed = (
        run.returncode == 0
        and k_value == candidate_value
        and candidate_value == canonical_value
    )
    print(f"CASE_MATCH: {passed}")
    if not passed:
        failures += 1

print(f"TOTAL_CASES: {len(cases)}")
print(f"MISMATCH_COUNT: {failures}")
raise SystemExit(1 if failures else 0)
