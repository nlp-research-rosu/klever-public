#!/usr/bin/env python3
"""Compare freshly compiled generated semantics with both Python implementations."""

from __future__ import annotations

import importlib.util
import shlex
import subprocess
from pathlib import Path
from typing import Callable


WORK = Path("/tmp/audit-work/110-exchange")


def load_exchange(path: Path, name: str) -> Callable[[list[int], list[int]], str]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


def pylist(values: list[int]) -> str:
    term = "Nil"
    for value in reversed(values):
        term = f"Cons({value}, {term})"
    return term


def main() -> int:
    oracle = load_exchange(Path("/reference/canonical.py"), "stage3_oracle")
    candidate = load_exchange(WORK / "solution.py", "stage3_candidate")
    cases = [
        ("prompt-yes", [1, 2, 3, 4], [1, 2, 3, 4]),
        ("prompt-no", [1, 2, 3, 4], [1, 5, 3, 4]),
        ("both-empty-boundary", [], []),
        ("empty-right-odd", [1], []),
        ("strictly-below-threshold", [1, 1], [2]),
        ("exact-threshold", [1, 1], [2, 4]),
        ("negative-integers", [-4, -3, -2, -1], [-8, -7]),
        ("single-zero", [0], [1]),
    ]

    failures = 0
    for label, left, right in cases:
        oracle_result = oracle(list(left), list(right))
        candidate_result = candidate(list(left), list(right))
        command = [
            "krun",
            "solution.mpy",
            "-d",
            "concrete-search-kompiled",
            f"-cLST1={pylist(left)}",
            f"-cLST2={pylist(right)}",
            "--pattern",
            f'<result> "{oracle_result}" </result>',
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"CASE: {label}")
        print(f"INPUT: lst1={left!r} lst2={right!r}")
        print(f"PYTHON_ORACLE: {oracle_result!r}")
        print(f"PYTHON_CANDIDATE: {candidate_result!r}")
        print(f"COMMAND: {shlex.join(command)}")
        print("K_OUTPUT:")
        print(completed.stdout.rstrip())
        print(f"K_EXIT_STATUS: {completed.returncode}")
        print("---")
        if candidate_result != oracle_result or completed.returncode != 0:
            failures += 1

    print(f"TOTAL_CASES: {len(cases)}")
    print(f"FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
