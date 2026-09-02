#!/usr/bin/env python3
"""Compare fresh LLVM K execution with the trusted Python program."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_sort(path: Path):
    spec = importlib.util.spec_from_file_location("trusted_canonical_for_krun", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


def ints_term(values: list[int]) -> str:
    if not values:
        return "listV(.Ints)"
    return "listV(" + " :: ".join(map(str, values)) + " :: .Ints)"


def parse_result(output: str) -> list[int]:
    match = re.search(r"listV\s*\(\s*(.*?)\s*\.Ints\s*\)", output, re.S)
    if match is None:
        raise ValueError(f"no listV result in output: {output!r}")
    return [int(value) for value in re.findall(r"-?\d+", match.group(1))]


root = Path("/tmp/audit-work")
work = root / "candidate"
canonical = load_sort(root / "reference/canonical.py")
cases = [
    ("empty", []),
    ("singleton-zero", [0]),
    ("pair-tie-break", [5, 3]),
    ("normal", [1, 5, 2, 3, 4]),
    ("duplicates", [3, 1, 3, 0, 1]),
    ("first-unproved-symbolic-length", [8, 7, 3, 0]),
    ("long-boundary", [2**63, 2**63 - 1, 0, 3, 1, 2, 4]),
    ("negative-supplement", [-2, -3, -4, -5, -6]),
]

failures = 0
for name, values in cases:
    command = [
        "krun",
        "solution.mpy",
        f"-cARGS={ints_term(values)}",
        "--definition",
        "semantic-concrete-kompiled",
    ]
    result = subprocess.run(command, cwd=work, text=True, capture_output=True)
    print(f"CASE {name}")
    print("COMMAND:", shlex.join(command))
    print(f"EXIT_STATUS: {result.returncode}")
    print("STDOUT:")
    print(result.stdout.rstrip())
    if result.stderr:
        print("STDERR:")
        print(result.stderr.rstrip())
    expected = canonical(list(values))
    try:
        actual = parse_result(result.stdout)
    except ValueError as error:
        actual = f"PARSE_ERROR: {error}"
    match = result.returncode == 0 and actual == expected
    print(f"PYTHON_EXPECTED: {expected!r}")
    print(f"K_ACTUAL: {actual!r}")
    print(f"MATCH: {match}")
    if not match:
        failures += 1

print(f"TOTAL_CASES: {len(cases)}")
print(f"MISMATCHES: {failures}")
raise SystemExit(1 if failures else 0)
