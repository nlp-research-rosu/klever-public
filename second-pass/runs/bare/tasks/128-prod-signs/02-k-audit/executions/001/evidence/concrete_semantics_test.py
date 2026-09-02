#!/usr/bin/env python3
"""Run the scratch-built K semantics and compare with both Python programs."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


def k_input(values: list[int]) -> str:
    return "input(" + ",".join(str(value) for value in values) + ")"


def extract_result(output: str) -> str:
    match = re.search(
        r"<result>\s*result\s*\(\s*(none|-?[0-9]+)\s*\)\s*</result>",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        raise RuntimeError(f"no final result found in krun output:\n{output}")
    return match.group(1)


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: concrete_semantics_test.py "
            "DEFINITION SOLUTION.mpy CANONICAL.py SOLUTION.py",
            file=sys.stderr,
        )
        return 64

    definition, mpy_path, canonical_path, solution_path = sys.argv[1:]
    canonical = load_entry("trusted_canonical_for_k", Path(canonical_path))
    generated = load_entry("generated_solution_for_k", Path(solution_path))

    cases = [
        [],
        [1, 2, 2, -4],
        [0, 1],
        [-1],
        [0],
        [1],
        [-1, -2],
        [-1, -2, -3],
        [-1, 0, 1],
        [0, -1],
        [1, 0],
        [2_147_483_647, -2_147_483_648],
    ]

    for values in cases:
        command = [
            "krun",
            mpy_path,
            "--definition",
            definition,
            f"-cARGS={k_input(values)}",
        ]
        print("COMMAND:", " ".join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print("KRUN_EXIT:", completed.returncode)
        if completed.stderr:
            print("KRUN_STDERR:")
            print(completed.stderr.rstrip())
        if completed.returncode != 0:
            print(completed.stdout)
            return completed.returncode

        k_actual = extract_result(completed.stdout)
        canonical_actual = canonical(list(values))
        generated_actual = generated(list(values))
        expected_text = "none" if canonical_actual is None else str(canonical_actual)
        print(
            f"INPUT={values!r} K={k_actual} "
            f"CANONICAL={canonical_actual!r} GENERATED={generated_actual!r}"
        )
        if k_actual != expected_text or generated_actual != canonical_actual:
            print("MISMATCH")
            return 1

    print(f"SUMMARY cases={len(cases)} mismatches=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
