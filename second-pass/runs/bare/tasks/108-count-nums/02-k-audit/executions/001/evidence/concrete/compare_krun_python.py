#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with two Python executions."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import subprocess
import sys


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 5:
        print(
            f"usage: {sys.argv[0]} DEFINITION SOLUTION.mpy SOLUTION.py CANONICAL.py",
            file=sys.stderr,
        )
        return 64
    definition, mpy_path, solution_path, canonical_path = sys.argv[1:]
    solution = load_module("concrete_solution", solution_path)
    canonical = load_module("concrete_canonical", canonical_path)
    cases = [
        [],
        [-1, 11, -11],
        [11, -11],
        [-11, 11],
        [1, 1, 2],
        [-123, -100, -99, 0, 10],
        [-10, -9, 9, 10],
        [-99, -98, 99, 100],
        [-1000, 0, 1000],
        [-101, -100, -20, -19, -11],
    ]
    mismatches = 0
    for values in cases:
        arg = "list(" + ", ".join(map(str, values)) + ")"
        command = [
            "krun",
            mpy_path,
            "--definition",
            definition,
            f"-cARG={arg}",
        ]
        process = subprocess.run(command, text=True, capture_output=True, check=False)
        matches = re.findall(r"<k>\s*IntV \( (-?\d+) \) ~> \.K\s*</k>", process.stdout)
        k_value = int(matches[0]) if process.returncode == 0 and len(matches) == 1 else None
        solution_value = solution.count_nums(values)
        canonical_value = canonical.count_nums(values)
        ok = (
            process.returncode == 0
            and k_value == solution_value
            and solution_value == canonical_value
        )
        if not ok:
            mismatches += 1
        print(
            json.dumps(
                {
                    "command": command,
                    "arr": values,
                    "krun_exit": process.returncode,
                    "k_value": k_value,
                    "solution_value": solution_value,
                    "canonical_value": canonical_value,
                    "match": ok,
                    "stderr": process.stderr.strip(),
                },
                sort_keys=True,
            )
        )
    print(f"CASES: {len(cases)}")
    print(f"MISMATCHES: {mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
