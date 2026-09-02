#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable


CASES = [
    [],
    [1, 2, 3],
    [1, 2, -4, 5],
    [-1],
    [0],
    [1],
    [1, -1],
    [1, -2],
    [5, -5],
    [5, -5, -1],
    [2, -1, -1, -1],
    [10**100, -(10**100)],
    [10**100, -(10**100) - 1],
]


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_zero


def int_list(values: list[int]) -> str:
    result = ".IntList"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--krun", required=True)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--results-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "kcheck_canonical")
    generated = load_entry(args.generated, "kcheck_generated")
    results: list[dict[str, object]] = []
    mismatch_count = 0

    for operations in CASES:
        encoded = int_list(operations)
        command = [
            args.krun,
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cOPERATIONS={encoded}",
        ]
        print("RUN:", shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"krun_exit={completed.returncode}")
        if completed.stderr:
            print("krun_stderr:", completed.stderr.strip())

        match = re.search(
            r"<result>\s*BoolV\s*\(\s*(true|false)\s*\)\s*</result>",
            completed.stdout,
        )
        k_result = None if match is None else match.group(1) == "true"
        canonical_result = canonical(list(operations))
        generated_result = generated(list(operations))
        agrees = (
            completed.returncode == 0
            and k_result is canonical_result
            and k_result is generated_result
        )
        mismatch_count += 0 if agrees else 1
        row = {
            "operations": operations,
            "k_exit": completed.returncode,
            "k_result": k_result,
            "canonical_result": canonical_result,
            "generated_result": generated_result,
            "match": agrees,
            "k_stdout": completed.stdout,
            "k_stderr": completed.stderr,
        }
        results.append(row)
        print(
            "RESULT:",
            json.dumps(
                {
                    "operations": operations,
                    "k": k_result,
                    "canonical": canonical_result,
                    "generated": generated_result,
                    "match": agrees,
                },
                separators=(",", ":"),
            ),
        )

    args.results_out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"cases={len(CASES)}")
    print(f"mismatches={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
