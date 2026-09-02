#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with Python and a loop oracle."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Callable


def load_add(module_name: str, path: Path) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


def oracle(values: list[int]) -> int:
    result = 0
    for index in range(1, len(values), 2):
        if values[index] % 2 == 0:
            result += values[index]
    return result


def k_sequence(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return f"pyList({result})"


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: generated_semantics_compare.py PROGRAM DEFINITION CANDIDATE_PY CANONICAL_PY",
            file=sys.stderr,
        )
        return 64

    program, definition, candidate_path, canonical_path = map(Path, sys.argv[1:])
    candidate = load_add("semantics_candidate_85", candidate_path.resolve())
    canonical = load_add("semantics_canonical_85", canonical_path.resolve())
    cases = [
        ("empty-extension", []),
        ("singleton-base", [1]),
        ("length-two-even", [9, 8]),
        ("length-two-odd", [9, 7]),
        ("length-two-negative-even", [9, -8]),
        ("documented", [4, 2, 6, 7]),
        ("two-contributions", [2, 3, 4, 6, 8, 10]),
        ("negative", [-1, -2, -3, -4, -5]),
        ("large-integers", [10**50, -(10**50), 7, 10**50 + 2]),
    ]

    failures = 0
    for label, values in cases:
        command = [
            "krun",
            str(program),
            "--definition",
            str(definition),
            f"-cINPUT={k_sequence(values)}",
        ]
        print(f"CASE: {label}")
        print(f"VALUES: {values!r}")
        print(f"COMMAND: {shlex.join(command)}")
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        print(f"KRUN_STDOUT_SHA256: {hashlib.sha256(completed.stdout.encode()).hexdigest()}")
        print(f"KRUN_STDERR: {completed.stderr.strip()!r}")

        match = re.search(r"<k>\s*pyInt \( (-?\d+) \) ~> \.K", completed.stdout)
        k_value = int(match.group(1)) if match else None
        oracle_value = oracle(values)
        candidate_value = candidate(values.copy())
        canonical_value = canonical(values.copy())
        print(
            "RESULTS: "
            f"k={k_value!r} candidate_python={candidate_value!r} "
            f"canonical_python={canonical_value!r} oracle={oracle_value!r}"
        )
        if (
            completed.returncode != 0
            or k_value != oracle_value
            or candidate_value != oracle_value
            or canonical_value != oracle_value
        ):
            failures += 1
            print("CASE_STATUS: MISMATCH")
        else:
            print("CASE_STATUS: MATCH")

    print(f"SUMMARY: cases={len(cases)} mismatches={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
