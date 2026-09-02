#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with two Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 6:
        print(
            f"usage: {sys.argv[0]} DEFINITION MPY SOLUTION.py CANONICAL.py INPUTS.json",
            file=sys.stderr,
        )
        return 64

    definition = Path(sys.argv[1]).resolve()
    mpy = Path(sys.argv[2]).resolve()
    candidate_path = Path(sys.argv[3]).resolve()
    canonical_path = Path(sys.argv[4]).resolve()
    inputs_path = Path(sys.argv[5]).resolve()
    inputs = json.loads(inputs_path.read_text(encoding="utf-8"))
    candidate = load_module("candidate_solution_concrete", candidate_path)
    canonical = load_module("trusted_canonical_concrete", canonical_path)

    failures = 0
    canonical_mismatches = 0
    for n in inputs:
        command = [
            "krun",
            str(mpy),
            "--definition",
            str(definition),
            "-cFUNCTION=\"sum_to_n\"",
            f"-cARG={n}",
        ]
        print("COMMAND:", shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        print(f"KRUN_EXIT_STATUS={completed.returncode}")
        print(completed.stdout.rstrip())
        if completed.stderr:
            print("KRUN_STDERR:")
            print(completed.stderr.rstrip())
        match = re.search(r"<result>\s*(-?\d+)\s*</result>", completed.stdout, re.S)
        k_value = int(match.group(1)) if match else None
        candidate_value = candidate.sum_to_n(n)
        canonical_value = canonical.sum_to_n(n)
        print(
            f"VALUES n={n} k={k_value} candidate={candidate_value} "
            f"canonical={canonical_value}"
        )
        if completed.returncode != 0 or k_value != candidate_value:
            failures += 1
            print(f"K_CANDIDATE_MISMATCH n={n}")
        if k_value != canonical_value:
            canonical_mismatches += 1
            print(f"K_CANONICAL_MISMATCH n={n}")

    print(f"TOTAL_CASES={len(inputs)}")
    print(f"K_CANDIDATE_FAILURES={failures}")
    print(f"K_CANONICAL_MISMATCHES={canonical_mismatches}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
