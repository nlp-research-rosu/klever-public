#!/usr/bin/env python3
"""Compare fresh K execution with both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
import re
import shlex
import subprocess
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("inputs", nargs="+", type=int)
    args = parser.parse_args()

    canonical = load_module("concrete_oracle_139", args.canonical)
    candidate = load_module("concrete_candidate_139", args.candidate)
    failures = 0

    for n in args.inputs:
        command = [
            "krun",
            str(args.program),
            f"-cN={n}",
            "--definition",
            str(args.definition),
            "--output",
            "pretty",
        ]
        print("COMMAND:", shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"EXIT_STATUS: {completed.returncode}")
        if completed.stdout:
            print(completed.stdout.rstrip())
        if completed.stderr:
            print("--- STDERR ---")
            print(completed.stderr.rstrip())

        matches = re.findall(r"result\s*\(\s*(-?[0-9]+)\s*\)", completed.stdout)
        k_value = int(matches[-1]) if matches else None
        canonical_value = canonical.special_factorial(n)
        candidate_value = candidate.special_factorial(n)
        same = (
            completed.returncode == 0
            and k_value == canonical_value
            and k_value == candidate_value
        )
        failures += int(not same)
        print(
            f"COMPARE n={n} k={k_value} canonical={canonical_value} "
            f"candidate={candidate_value} status={'MATCH' if same else 'MISMATCH'}"
        )

    print(f"SUMMARY cases={len(args.inputs)} mismatches={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
