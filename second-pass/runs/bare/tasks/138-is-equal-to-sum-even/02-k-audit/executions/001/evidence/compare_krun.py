#!/usr/bin/env python3
"""Run the fresh generated semantics and compare it with both Python entries."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


DEFINITION = Path("/tmp/audit-work/review-138/build/semantic-kompiled")
PROGRAM = Path("/tmp/audit-work/review-138/candidate-src/solution.mpy")
CANONICAL_PATH = Path("/tmp/audit-work/review-138/reference-src/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/review-138/candidate-src/solution.py")
CASES = [-11, -10, -3, -2, 0, 4, 6, 7, 8, 9, 10, 12, 10**18]


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_equal_to_sum_even


def main() -> None:
    canonical = load_function(CANONICAL_PATH, "fresh_canonical_138")
    candidate = load_function(CANDIDATE_PATH, "fresh_candidate_138")
    mismatches = []

    print(f"CASES={CASES}")
    for n in CASES:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cN={n}",
        ]
        print("$ " + shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        print(completed.stdout.rstrip())
        if completed.stderr:
            print(completed.stderr.rstrip())
        print(f"[exit {completed.returncode}]")

        match = re.search(r"BoolValue\s*\(\s*(true|false)\s*\)", completed.stdout)
        parsed = None if match is None else match.group(1) == "true"
        expected_canonical = canonical(n)
        expected_candidate = candidate(n)
        print(
            f"COMPARE n={n} krun={parsed} "
            f"canonical={expected_canonical} candidate={expected_candidate}"
        )
        if (
            completed.returncode != 0
            or parsed is None
            or parsed != expected_canonical
            or parsed != expected_candidate
        ):
            mismatches.append(
                (n, completed.returncode, parsed, expected_canonical, expected_candidate)
            )

    print(f"MISMATCHES={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
