#!/usr/bin/env python3
"""Run the clean generated K semantics and compare its results with Python."""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decimal_to_binary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()

    canonical = load(args.canonical, "canonical_concrete")
    generated = load(args.generated, "generated_concrete")
    values = [
        -((1 << 100) + 3),
        -17,
        -2,
        -1,
        0,
        1,
        2,
        3,
        15,
        32,
        1024,
        (1 << 100) + 3,
    ]
    mismatches = 0
    for value in values:
        command = [
            "krun",
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cARG={value}",
        ]
        print("COMMAND:", " ".join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="")
        print(f"EXIT_STATUS {completed.returncode}")
        matches = re.findall(
            r'<result>\s*strVal\s*\(\s*"((?:[^"\\]|\\.)*)"\s*\)'
            r'(?:\s*~>\s*\.K)?\s*</result>',
            completed.stdout,
            flags=re.DOTALL,
        )
        k_result = bytes(matches[-1], "utf-8").decode("unicode_escape") if matches else None
        expected = canonical(value)
        generated_result = generated(value)
        passed = (
            completed.returncode == 0
            and k_result == expected
            and generated_result == expected
        )
        print(
            f"COMPARE input={value} k={k_result!r} canonical={expected!r} "
            f"generated={generated_result!r} pass={passed}"
        )
        mismatches += not passed
    print(f"CONCRETE_CASE_COUNT={len(values)}")
    print(f"CONCRETE_MISMATCH_COUNT={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
