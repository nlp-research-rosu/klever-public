#!/usr/bin/env python3
"""Compare fresh LLVM-semantics executions with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Callable


DEFINITION = Path("/tmp/audit-work/135-can-arrange/build/concrete-kompiled")
PROGRAM = Path("/tmp/audit-work/135-can-arrange/source/solution.mpy")
CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/135-can-arrange/source/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


def k_seq(values: list[int]) -> str:
    return "seq(" + ",".join(str(value) for value in values) + ")"


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical_concrete")
    generated = load_entry(GENERATED_PATH, "submitted_solution_concrete")
    cases = [
        ("empty", [], 0, 0),
        ("singleton", [7], 0, 1),
        ("length-2-no-drop", [-1, 4], 0, 2),
        ("length-2-drop", [4, -1], 0, 2),
        ("documented-drop", [1, 2, 4, 3, 5], 0, 5),
        ("all-drops", [5, 4, 3, 2, 1], 0, 5),
        ("multiple-drops", [9, 1, 8, 2, 7, 3], 0, 6),
        ("negative-values", [-8, -3, -4, -1], 0, 4),
        ("nonzero-view-offset", [99, 1, 2, 4, 3, 5, 88], 1, 5),
        ("zero-length-view-at-end", [10, 20], 2, 0),
    ]
    failures = 0
    pattern = re.compile(r"value \( intVal \( (-?\d+) \) \)")

    for label, backing, offset, length in cases:
        view = backing[offset : offset + length]
        canonical_result = canonical(list(view))
        generated_result = generated(list(view))
        args = f"arrayVal({k_seq(backing)},{offset},{length})"
        command = [
            "krun",
            str(PROGRAM),
            f"-cARGS={args}",
            "--definition",
            str(DEFINITION),
        ]
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        matches = pattern.findall(completed.stdout)
        k_result = int(matches[-1]) if matches else None
        ok = (
            completed.returncode == 0
            and k_result == canonical_result
            and k_result == generated_result
        )
        failures += int(not ok)
        print(f"CASE: {label}")
        print(f"COMMAND: {shlex.join(command)}")
        print(
            "RESULT: "
            f"exit={completed.returncode} k={k_result} "
            f"canonical={canonical_result} generated={generated_result} ok={ok}"
        )
        if not ok:
            print("STDOUT:")
            print(completed.stdout)
            print("STDERR:")
            print(completed.stderr)

    print(f"SUMMARY: cases={len(cases)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
