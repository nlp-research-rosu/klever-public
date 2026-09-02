#!/usr/bin/env python3
"""Compare freshly built K semantics with both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def int_list(values: list[int]) -> str:
    term = "Nil"
    for value in reversed(values):
        term = f"Cons({value}, {term})"
    return term


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical")
    parser.add_argument("candidate")
    parser.add_argument("program")
    parser.add_argument("definition")
    args = parser.parse_args()

    canonical = load_module("trusted_canonical_k_bridge", Path(args.canonical)).is_sorted
    candidate = load_module("candidate_solution_k_bridge", Path(args.candidate)).is_sorted
    cases = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [0, 1],
        [1, 0],
        [0, 1, 0],
        [1, 2, 3, 4, 5],
        [1, 3, 2, 4, 5],
        [1, 2, 2, 3, 3, 4],
        [1, 2, 2, 2, 3, 4],
        [0, 1_000_000],
        [1_000_000, 0],
        [7, 7],
        [7, 7, 7],
    ]
    mismatches = 0
    print(f"INPUTS={cases!r}")
    for index, values in enumerate(cases):
        argument = f"PyList({int_list(values)})"
        command = [
            "krun",
            args.program,
            "--definition",
            args.definition,
            f"-cARGS={argument}",
        ]
        print("COMMAND:", " ".join(command))
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        combined = completed.stdout + completed.stderr
        match = re.search(r"BoolVal\s*\(\s*(true|false)\s*\)", combined)
        k_value = None if match is None else match.group(1) == "true"
        canonical_value = canonical(list(values))
        candidate_value = candidate(list(values))
        ok = (
            completed.returncode == 0
            and k_value is not None
            and k_value == canonical_value
            and k_value == candidate_value
        )
        print(
            f"CASE={index} INPUT={values!r} KRUN_EXIT={completed.returncode} "
            f"K={k_value!r} CANONICAL={canonical_value!r} "
            f"CANDIDATE={candidate_value!r} MATCH={ok}"
        )
        print("KRUN_OUTPUT=" + combined.strip().replace("\n", "\\n"))
        mismatches += int(not ok)
    print(f"CASES={len(cases)}")
    print(f"MISMATCHES={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
