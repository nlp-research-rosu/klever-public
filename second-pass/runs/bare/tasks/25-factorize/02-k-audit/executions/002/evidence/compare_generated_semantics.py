#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both independent Python executions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


WORK = Path("/tmp/audit-work/25-factorize")
DEFINITION = WORK / "fresh-semantic-llvm-kompiled"
PROGRAM = WORK / "solution.mpy"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def python_outcome(function: Any, value: int) -> tuple[str, Any]:
    try:
        return ("return", function(value))
    except BaseException as error:
        return ("raise", type(error).__name__)


def parse_k_result(stdout: str) -> list[int]:
    result_match = re.search(r"<result>(.*?)</result>", stdout, re.DOTALL)
    if result_match is None:
        raise ValueError("K output has no <result> cell")
    body = result_match.group(1)
    if "ListVal" not in body:
        raise ValueError(f"K result is not ListVal: {body.strip()}")
    return [int(value) for value in re.findall(r"IntVal \( (-?[0-9]+) \)", body)]


def main() -> int:
    canonical = load_module("semantics_canonical", Path("/reference/canonical.py"))
    candidate = load_module("semantics_candidate", WORK / "solution.py")
    inputs = [-1, 0, 1, 2, 3, 4, 8, 9, 25, 70, 999, 1000003]
    k_failures = 0
    canonical_mismatches = 0
    candidate_mismatches = 0

    for value in inputs:
        command = [
            "krun",
            str(PROGRAM),
            f"-cINPUT={value}",
            "--definition",
            str(DEFINITION),
        ]
        print("$ " + " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        print(result.stdout.rstrip())
        if result.stderr:
            print("STDERR:")
            print(result.stderr.rstrip())
        print(f"EXIT STATUS: {result.returncode}")
        if result.returncode != 0:
            k_failures += 1
            continue
        k_outcome = ("return", parse_k_result(result.stdout))
        canonical_outcome = python_outcome(canonical.factorize, value)
        candidate_outcome = python_outcome(candidate.factorize, value)
        print(
            f"COMPARISON n={value}: K={k_outcome!r} "
            f"canonical={canonical_outcome!r} candidate={candidate_outcome!r}"
        )
        if value >= 1 and k_outcome != canonical_outcome:
            canonical_mismatches += 1
        if k_outcome != candidate_outcome:
            candidate_mismatches += 1

    print(f"K_EXECUTION_FAILURES={k_failures}")
    print(f"INTENDED_DOMAIN_K_VS_CANONICAL_MISMATCHES={canonical_mismatches}")
    print(f"K_VS_GENERATED_PYTHON_MISMATCHES={candidate_mismatches}")
    if k_failures or canonical_mismatches or candidate_mismatches:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
