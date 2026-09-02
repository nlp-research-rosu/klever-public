#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python programs."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


PROGRAM = Path("/tmp/audit-work/source/solution.mpy")
DEFINITION = Path("/tmp/audit-work/build/semantic-kompiled-fresh")
CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/source/solution.py")

CASES = [
    [],
    [7],
    [1, 2, 3, 4],
    [-2, 0, 5],
    [-3, -2, -1],
    [10**20, -2],
]

RESULT_PATTERN = re.compile(
    r"PyTuple\s*\(\s*"
    r"PyInt\s*\(\s*(-?\d+)\s*\)\s*,\s*"
    r"PyInt\s*\(\s*(-?\d+)\s*\)\s*\)"
)


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


def encode(values: list[int]) -> str:
    body = ", ".join(str(value) for value in values)
    suffix = f"{body}, .Ints" if body else ".Ints"
    return f"PyList({suffix})"


canonical = load_entry("trusted_canonical_for_k", CANONICAL)
generated = load_entry("generated_python_for_k", GENERATED)
mismatches = 0

for index, values in enumerate(CASES):
    command = [
        "krun",
        str(PROGRAM),
        f"-cINPUT={encode(values)}",
        "--definition",
        str(DEFINITION),
    ]
    print(f"CASE {index}: input={values!r}")
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    if completed.stderr:
        print(f"KRUN_STDERR: {completed.stderr.rstrip()}")
    match = RESULT_PATTERN.search(completed.stdout)
    k_result = (
        (int(match.group(1)), int(match.group(2))) if match is not None else None
    )
    canonical_result = canonical(values)
    generated_result = generated(values)
    print(
        f"k_result={k_result!r} canonical_result={canonical_result!r} "
        f"generated_result={generated_result!r}"
    )
    if (
        completed.returncode != 0
        or k_result != canonical_result
        or k_result != generated_result
    ):
        mismatches += 1
        print("CASE_RESULT: MISMATCH")
        print(completed.stdout)
    else:
        print("CASE_RESULT: MATCH")

print(f"cases={len(CASES)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
