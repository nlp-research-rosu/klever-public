#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python programs."""

from __future__ import annotations

import importlib.util
import os
import re
import shlex
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load_entry("trusted_canonical_kcheck", Path("/reference/canonical.py"))
candidate = load_entry(
    "scratch_candidate_kcheck", Path("/tmp/audit-work/candidate-src/solution.py")
)

cases = [
    [],
    [1],
    [0, 0],
    [0, 0, 0],
    [-1, 0, 1],
    [1, 1, -2],
    [1, -1],
    [1, 3, 5, 0],
    [1, 3, -2, 1],
    [1, 2, 3, 7],
    [2, 4, -5, 3, 9, 7],
    [5, 1, 7, -8],
    [9, 8, 1, 2, -3],
    [1000000000000, -1000000000000, 0],
    [-7, -6, -5, -4],
    [4, 5, 6, 7],
]

definition = os.environ.get(
    "AUDIT_K_DEFINITION", "/tmp/audit-work/build/semantic-llvm-r2"
)
program = "/tmp/audit-work/candidate-src/solution.mpy"
result_pattern = re.compile(
    r"<result>\s*result\s*\(\s*VBool\s*\(\s*(true|false)\s*\)\s*\)\s*</result>",
    re.MULTILINE,
)

failures: list[str] = []
for index, values in enumerate(cases):
    ints = ".Ints" if not values else " ; ".join(map(str, values)) + " ; .Ints"
    command = [
        "krun",
        program,
        "--definition",
        definition,
        f"-cINPUT=VList({ints})",
        "--output",
        "pretty",
    ]
    print(f"\nCASE {index}: {values!r}")
    print("$ " + shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"[exit {completed.returncode}]")
    if completed.stderr:
        print("stderr:")
        print(completed.stderr.rstrip())
    matches = result_pattern.findall(completed.stdout)
    result_lines = [
        line.strip()
        for line in completed.stdout.splitlines()
        if "<result>" in line or "result (" in line
    ]
    print("relevant K output:")
    for line in result_lines:
        print(line)

    oracle = canonical(values)
    py_candidate = candidate(values)
    k_value = None if len(matches) != 1 else matches[0] == "true"
    print(
        f"trusted_python={oracle} candidate_python={py_candidate} "
        f"generated_K={k_value}"
    )
    if (
        completed.returncode != 0
        or len(matches) != 1
        or type(oracle) is not bool
        or type(py_candidate) is not bool
        or oracle != py_candidate
        or oracle != k_value
    ):
        failures.append(
            f"case={index} input={values!r} exit={completed.returncode} "
            f"matches={matches!r} trusted={oracle!r} "
            f"candidate={py_candidate!r}"
        )

print(f"\ncases={len(cases)}")
print(f"mismatches={len(failures)}")
for failure in failures:
    print(f"FAIL {failure}")
raise SystemExit(1 if failures else 0)
