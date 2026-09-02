#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/rebuild")
CANONICAL = Path("/reference/canonical.py")
GENERATED = WORK / "solution.py"
DEFINITION = WORK / "concrete-kompiled"


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


canonical = load_entry("concrete_oracle_canonical", CANONICAL)
generated = load_entry("concrete_oracle_generated", GENERATED)

cases = [
    "",
    "AB",
    "1077E",
    "ABED1A33",
    "123456789ABCDEF0",
    "2020",
    *list("0123456789ABCDEF"),
    "BD" * 32,
    "ACEF" * 32,
    "0123456789ABCDEF" * 8,
]

mismatches = 0
for value in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={json.dumps(value)}",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    match = re.search(r"intVal\s*\(\s*(-?\d+)\s*\)", completed.stdout)
    k_result = int(match.group(1)) if match else None
    canonical_result = canonical(value)
    generated_result = generated(value)
    ok = (
        completed.returncode == 0
        and k_result == canonical_result
        and k_result == generated_result
    )
    print(f"COMMAND={shlex.join(command)}")
    print(
        "CASE="
        + repr(value)
        + f" K={k_result} canonical={canonical_result} "
        + f"generated={generated_result} krun_exit={completed.returncode} "
        + f"status={'PASS' if ok else 'FAIL'}"
    )
    if not ok:
        mismatches += 1
        print("KRUN_OUTPUT_BEGIN")
        print(completed.stdout.rstrip())
        print("KRUN_OUTPUT_END")

print(f"case_count={len(cases)}")
print(f"mismatch_count={mismatches}")
if mismatches:
    raise SystemExit(1)
print("CONCRETE_SEMANTICS_TEST_PASS")
