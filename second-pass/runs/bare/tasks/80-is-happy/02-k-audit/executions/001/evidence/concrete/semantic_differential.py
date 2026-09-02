#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pstring(value: str) -> str:
    result = "eps"
    for char in reversed(value):
        result = f"ch({ord(char)}, {result})"
    return result


canonical = load_module("trusted_canonical_k_compare", Path("/reference/canonical.py"))
candidate = load_module(
    "candidate_solution_k_compare", Path("/tmp/audit-work/fresh/solution.py")
)

cases = [
    ("empty", ""),
    ("len1", "a"),
    ("len2", "aa"),
    ("len3-distinct", "abc"),
    ("eq-01", "aac"),
    ("eq-02", "aba"),
    ("eq-12", "abb"),
    ("recursive-true", "abcd"),
    ("recursive-late-false", "abcdd"),
    ("unicode-true", "a🙂βx"),
    ("unicode-false", "a🙂a"),
    ("longer-true", "abc" * 7),
]

definition = "/tmp/audit-work/fresh/semantic-audit-kompiled"
program = "/tmp/audit-work/fresh/solution.mpy"
pattern = re.compile(r"pyBool\s*\(\s*(true|false)\s*\)")
mismatches = 0

print(f"definition={definition}")
print(f"program={program}")
print(f"case_count={len(cases)}")
for label, value in cases:
    command = [
        "krun",
        program,
        f"-cINPUT={pstring(value)}",
        "--definition",
        definition,
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    combined = completed.stdout + completed.stderr
    match = pattern.search(combined)
    k_value = None if match is None else match.group(1) == "true"
    canonical_value = canonical.is_happy(value)
    candidate_value = candidate.is_happy(value)
    agrees = (
        completed.returncode == 0
        and k_value == canonical_value
        and k_value == candidate_value
    )
    if not agrees:
        mismatches += 1
    print(
        f"CASE label={label} input={value!r} k_ast={pstring(value)} "
        f"command={command!r} exit={completed.returncode} "
        f"k={k_value!r} canonical={canonical_value!r} "
        f"candidate={candidate_value!r} agrees={agrees}"
    )
    if not agrees:
        print("K_OUTPUT_BEGIN")
        print(combined.rstrip())
        print("K_OUTPUT_END")

print(f"mismatch_count={mismatches}")
raise SystemExit(1 if mismatches else 0)
