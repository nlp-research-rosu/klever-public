#!/usr/bin/env python3
"""Compare fresh concrete K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/19-sort-numbers")
DEFINITION = SCRATCH / "semantics-haskell-kompiled"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


canonical = load_entry("trusted_canonical_k_bridge", Path("/reference/canonical.py"))
generated = load_entry("generated_solution_k_bridge", SCRATCH / "solution.py")

cases = [
    "",
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "three one five",
    "two two one zero two",
    "nine eight seven six five four three two one zero",
    "zero zero zero zero",
    "nine zero nine zero",
    " one",
    "one ",
    "one  zero",
]

value_pattern = re.compile(r'VStr \( ("(?:[^"\\]|\\.)*") \) ~> \.K')
mismatches = []

for case in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARG={json.dumps(case)}",
    ]
    result = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        capture_output=True,
        check=False,
    )
    match = value_pattern.search(result.stdout)
    k_value = json.loads(match.group(1)) if match else None
    canonical_value = canonical(case)
    generated_value = generated(case)
    ok = (
        result.returncode == 0
        and k_value == canonical_value
        and k_value == generated_value
    )
    print(f"COMMAND: {shlex.join(command)}")
    print(
        f"EXIT: {result.returncode} INPUT: {case!r} "
        f"K: {k_value!r} CANONICAL: {canonical_value!r} "
        f"GENERATED: {generated_value!r} MATCH: {ok}"
    )
    if not ok:
        print(f"STDOUT: {result.stdout!r}")
        print(f"STDERR: {result.stderr!r}")
        mismatches.append(case)

print(f"concrete_cases={len(cases)} mismatch_count={len(mismatches)}")
raise SystemExit(1 if mismatches else 0)
