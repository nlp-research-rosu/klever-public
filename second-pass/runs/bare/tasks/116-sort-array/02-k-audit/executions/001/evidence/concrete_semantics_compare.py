#!/usr/bin/env python3
"""Run the freshly built generated semantics and compare with Python."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


def k_list(values: list[int]) -> str:
    if not values:
        return "listV(.Ints)"
    return "listV(" + " :: ".join(map(str, values)) + " :: .Ints)"


def parse_k_list(output: str) -> list[int]:
    match = re.search(r"listV\s*\(\s*(.*?)\s*\.Ints\s*\)", output, re.DOTALL)
    if match is None:
        raise ValueError(f"no final listV found in output: {output!r}")
    return [int(item) for item in re.findall(r"-?\d+", match.group(1))]


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: concrete_semantics_compare.py "
            "DEFINITION SOLUTION.mpy CANDIDATE.py CANONICAL.py",
            file=sys.stderr,
        )
        return 64

    definition, program, candidate_path, canonical_path = sys.argv[1:]
    candidate = load_entry(Path(candidate_path), "candidate_semantics_oracle")
    canonical = load_entry(Path(canonical_path), "canonical_semantics_oracle")
    cases = [
        [],
        [0],
        [1],
        [1, 2],
        [2, 1],
        [1, 3],
        [3, 1],
        [1, 5, 2, 3, 4],
        [1, 0, 2, 3, 4],
        [3, 1, 3, 0, 1],
        [7, 8, 3, 2, 1, 0],
        [-2, -3, -4, -5, -6],
        [2**63 - 1, 2**63, 0, 2**31 - 1, 2**31],
    ]

    failures = 0
    for index, values in enumerate(cases):
        command = [
            "krun",
            program,
            "-cARGS=" + k_list(values),
            "--definition",
            definition,
        ]
        print(f"CASE {index} INPUT {values}")
        print("COMMAND:", " ".join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        print("KRUN_STDOUT:")
        print(completed.stdout.rstrip())
        if completed.stderr:
            print("KRUN_STDERR:")
            print(completed.stderr.rstrip())

        try:
            k_result = parse_k_list(completed.stdout)
        except ValueError as error:
            print(f"PARSE_ERROR: {error}")
            failures += 1
            continue
        candidate_result = candidate(values.copy())
        canonical_result = canonical(values.copy())
        print(f"K_RESULT: {k_result}")
        print(f"CANDIDATE_PYTHON_RESULT: {candidate_result}")
        print(f"TRUSTED_CANONICAL_RESULT: {canonical_result}")
        agrees = (
            completed.returncode == 0
            and k_result == candidate_result
            and k_result == canonical_result
        )
        print(f"ALL_AGREE: {agrees}")
        if not agrees:
            failures += 1

    print(f"SUMMARY cases={len(cases)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
