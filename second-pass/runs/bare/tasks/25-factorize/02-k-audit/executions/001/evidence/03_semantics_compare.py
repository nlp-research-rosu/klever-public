#!/usr/bin/env python3
"""Compare fresh generated-K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SOURCE_DIR = Path("/tmp/audit-work/25-factorize-audit/source")
DEFINITION = Path("/tmp/audit-work/25-factorize-audit/semantic-fresh-kompiled")
SOLUTION_MPY = SOURCE_DIR / "solution.mpy"
GENERATED_PY = SOURCE_DIR / "solution.py"
CANONICAL_PY = Path("/tmp/audit-work/25-factorize-audit/trusted/canonical.py")


def load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def python_outcome(fn: Any, value: int) -> tuple[str, Any]:
    try:
        return ("return", fn(value))
    except Exception as exc:
        return ("raise", type(exc).__name__)


def parse_k_result(stdout: str) -> tuple[str, Any]:
    match = re.search(r"<result>\s*(.*?)\s*</result>", stdout, re.DOTALL)
    if match is None:
        return ("parse-error", "missing <result>")
    body = match.group(1)
    if not body.lstrip().startswith("ListVal"):
        return ("return-non-list", " ".join(body.split()))
    return ("return", [int(value) for value in re.findall(r"IntVal\s*\(\s*(-?\d+)\s*\)", body)])


generated = load("generated_solution_for_k_compare", GENERATED_PY)
canonical = load("trusted_canonical_for_k_compare", CANONICAL_PY)

normal_and_boundary_inputs = [
    -1,
    0,
    1,
    2,
    3,
    4,
    5,
    8,
    9,
    15,
    16,
    24,
    25,
    26,
    49,
    70,
    97,
    100,
    999,
]
recursion_boundary_inputs = [999_983]
inputs = normal_and_boundary_inputs + recursion_boundary_inputs

print("fresh_definition=" + str(DEFINITION), flush=True)
print("normal_and_boundary_inputs=" + repr(normal_and_boundary_inputs), flush=True)
print("recursion_boundary_inputs=" + repr(recursion_boundary_inputs), flush=True)

normal_generated_mismatches = 0
normal_canonical_mismatches = 0
stress_timeouts = 0
for value in inputs:
    command = [
        "krun",
        str(SOLUTION_MPY),
        f"-cINPUT={value}",
        "--definition",
        str(DEFINITION),
    ]
    print("$ " + " ".join(command), flush=True)
    try:
        completed = subprocess.run(
            command,
            cwd=SOURCE_DIR,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=20,
        )
    except subprocess.TimeoutExpired as exc:
        print("[krun_timeout_seconds=20]", flush=True)
        if value in recursion_boundary_inputs:
            stress_timeouts += 1
            continue
        print(f"UNEXPECTED_NORMAL_TIMEOUT n={value}", flush=True)
        normal_generated_mismatches += 1
        normal_canonical_mismatches += 1
        continue
    print(f"[krun_exit_status={completed.returncode}]")
    k_outcome = (
        parse_k_result(completed.stdout)
        if completed.returncode == 0
        else ("krun-error", completed.returncode)
    )
    generated_outcome = python_outcome(generated.factorize, value)
    canonical_outcome = python_outcome(canonical.factorize, value)
    print(
        f"n={value} k={k_outcome!r} generated_python={generated_outcome!r} "
        f"canonical_python={canonical_outcome!r}"
    )
    if completed.returncode != 0 or k_outcome[0] in {"parse-error", "return-non-list"}:
        print("KRUN_OUTPUT_BEGIN")
        print(completed.stdout.rstrip())
        print("KRUN_OUTPUT_END")
    if value >= 0 and value in normal_and_boundary_inputs and k_outcome != generated_outcome:
        normal_generated_mismatches += 1
        print("POSITIVE_GENERATED_MISMATCH")
    if value >= 0 and value in normal_and_boundary_inputs and k_outcome != canonical_outcome:
        normal_canonical_mismatches += 1
        print("POSITIVE_CANONICAL_MISMATCH")

print(f"normal_generated_mismatch_count={normal_generated_mismatches}")
print(f"normal_canonical_mismatch_count={normal_canonical_mismatches}")
print(f"recursion_stress_timeout_count={stress_timeouts}")
if normal_generated_mismatches or normal_canonical_mismatches:
    sys.exit(1)
