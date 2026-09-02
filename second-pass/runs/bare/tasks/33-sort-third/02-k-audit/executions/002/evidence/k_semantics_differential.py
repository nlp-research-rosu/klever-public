#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
import random
import re
import subprocess
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def vlist(values: list[int]) -> str:
    return "VList(" + ", ".join(map(str, values)) + ")"


def parse_result(stdout: str) -> list[int]:
    match = re.search(
        r"<result>\s*VList\s*\((.*?)\)\s*~>\s*\.K\s*</result>",
        stdout,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError(f"could not parse result cell:\n{stdout}")
    payload = match.group(1).replace(".Ints", "").strip(" ,\n")
    return [] if not payload else [int(item.strip()) for item in payload.split(",")]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path)
    parser.add_argument("definition", type=Path)
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical_k_bridge")
    candidate = load_entry(args.candidate, "candidate_solution_k_bridge")
    cases = [
        [],
        [7],
        [7, -1],
        [1, 2, 3],
        [3, 20, 10, 1],
        [9, 8, 7, 6, 5],
        [5, 6, 3, 4, 8, 9],
        [5, 6, 3, 4, 8, 9, 2],
        [-3, 9, 8, 0, 7, 6, 4],
        [9, 0, -1, 8, 7, 6, 2, 5, 4, 1],
        [2, 8, 7, 2, 6, 5, -1, 4, 3, 2],
        [10**18, 2, 3, -(10**18), 5, 6, 0],
    ]
    rng = random.Random(330034)
    for length in range(12):
        cases.append([rng.randrange(-100, 101) for _ in range(length)])

    mismatches = []
    failures = []
    for index, values in enumerate(cases):
        command = [
            "krun",
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cINPUT={vlist(values)}",
        ]
        run = subprocess.run(command, text=True, capture_output=True, check=False)
        if run.returncode != 0:
            failures.append((index, values, run.returncode, run.stderr[-500:]))
            continue
        actual = parse_result(run.stdout)
        expected_canonical = canonical(values)
        expected_candidate = candidate(values)
        if actual != expected_canonical or actual != expected_candidate:
            mismatches.append(
                (index, values, expected_canonical, expected_candidate, actual)
            )

    print("named_cases=12")
    print("seeded_length_cases=12 seed=330034 lengths=0..11")
    print(f"total_cases={len(cases)}")
    print(f"krun_failures={len(failures)}")
    print(f"mismatches={len(mismatches)}")
    if failures:
        print(f"first_krun_failure={failures[0]!r}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
    if failures or mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
