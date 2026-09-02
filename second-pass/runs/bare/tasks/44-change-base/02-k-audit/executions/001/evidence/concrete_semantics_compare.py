#!/usr/bin/env python3
"""Compare fresh LLVM semantics with candidate Python and trusted canonical."""

from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
from typing import Callable


WORK = pathlib.Path("/tmp/audit-work/44-change-base.Cjtazd/candidate-src")
SOLUTION_MPY = WORK / "solution.mpy"
DEFINITION = WORK / "audit-semantic-kompiled"
CASES = [
    ("example", 8, 3),
    ("example", 8, 2),
    ("example", 7, 2),
    ("zero-boundary", 0, 2),
    ("base-case", 1, 2),
    ("recursive-boundary", 2, 2),
    ("recursive", 3, 2),
    ("zero-boundary", 0, 9),
    ("base-case", 8, 9),
    ("recursive-boundary", 9, 9),
    ("recursive", 10, 9),
    ("larger-recursive", 1234, 7),
    ("python-recursion-limit", 2**1100, 2),
]


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[int, int], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def parse_k_string(output: str) -> str:
    match = re.search(r'strVal\s*\(\s*("(?:[^"\\]|\\.)*")\s*\)', output)
    if match is None:
        raise ValueError(f"no terminal strVal in krun output: {output!r}")
    return json.loads(match.group(1))


def python_outcome(function: Callable[[int, int], str], x: int, base: int) -> tuple:
    try:
        return ("return", function(x, base))
    except Exception as error:  # noqa: BLE001 - exceptions are observable outcomes.
        return ("exception", type(error).__name__, str(error))


def main() -> int:
    candidate = load_entry(WORK / "solution.py", "candidate_solution_for_krun")
    canonical = load_entry(pathlib.Path("/reference/canonical.py"), "canonical_for_krun")
    candidate_mismatches = 0
    canonical_mismatches = 0

    for reason, x, base in CASES:
        command = [
            "krun",
            str(SOLUTION_MPY),
            f"-cX={x}",
            f"-cBASE={base}",
            "--definition",
            str(DEFINITION),
        ]
        print(f"KRUN_COMMAND: {shlex.join(command)}")
        completed = subprocess.run(
            command,
            cwd=WORK,
            env=os.environ.copy(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        print("KRUN_OUTPUT_BEGIN")
        print(completed.stdout.rstrip())
        print("KRUN_OUTPUT_END")
        if completed.returncode != 0:
            candidate_mismatches += 1
            canonical_mismatches += 1
            continue

        k_result = ("return", parse_k_string(completed.stdout))
        python_result = python_outcome(candidate, x, base)
        canonical_result = python_outcome(canonical, x, base)
        candidate_match = k_result == python_result
        canonical_match = k_result == canonical_result
        candidate_mismatches += int(not candidate_match)
        canonical_mismatches += int(not canonical_match)
        print(
            f"COMPARE reason={reason} x={x} base={base} "
            f"k={k_result!r} candidate_python={python_result!r} "
            f"canonical_python={canonical_result!r} "
            f"k_candidate_match={candidate_match} k_canonical_match={canonical_match}"
        )

    print(f"K_VS_CANDIDATE_MISMATCHES: {candidate_mismatches}")
    print(f"K_VS_CANONICAL_MISMATCHES: {canonical_mismatches}")
    return 0 if candidate_mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
