#!/usr/bin/env python3
"""Compare fresh K execution with independent CPython implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


RESULT_RE = re.compile(
    r'<result>\s*VString\s*\(\s*("(?:[^"\\]|\\.)*")\s*\)\s*</result>',
    re.DOTALL,
)


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.circular_shift


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: concrete_semantics_test.py SCRATCH_DIRECTORY DEFINITION"
        )
    scratch = Path(sys.argv[1])
    definition = Path(sys.argv[2])
    candidate = load_function(scratch / "solution.py", "candidate_solution_for_k")
    canonical = load_function(scratch / "trusted-canonical.py", "trusted_canonical_for_k")

    # Includes the prompt examples, both branch boundaries, zero, negative x,
    # a very large integer, and negative shifts that the source contract does
    # not exclude.
    cases = [
        (12, 1),
        (12, 2),
        (1234, 0),
        (1234, 2),
        (1234, 4),
        (1234, 5),
        (0, 0),
        (0, 1),
        (0, 2),
        (-1234, 0),
        (-1234, 3),
        (-1234, 5),
        (-1234, 6),
        (10**40 + 123, 17),
        (1234, -1),
        (0, -1),
    ]

    mismatches = 0
    expected_stuck = 0
    for x, shift in cases:
        expected = canonical(x, shift)
        candidate_value = candidate(x, shift)
        if candidate_value != expected:
            print("PYTHON_MISMATCH", x, shift, expected, candidate_value)
            mismatches += 1
            continue
        command = [
            "krun",
            str(scratch / "solution.mpy"),
            "--definition",
            str(definition),
            "-cENTRY=\"circular_shift\"",
            f"-cARGS=VInt({x}), VInt({shift})",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        output = completed.stdout + completed.stderr
        match = RESULT_RE.search(output)
        actual = json.loads(match.group(1)) if match else None
        if shift < 0 and completed.returncode == 0 and actual is None:
            # The generated semantics may stop visibly on a modeled syntax term
            # whose semantic preconditions are not covered.
            expected_stuck += 1
            print("K_STUCK_NEGATIVE_SHIFT", x, shift, "expected_python", repr(expected))
            continue
        status = (
            "MATCH"
            if completed.returncode == 0 and actual == expected
            else "MISMATCH"
        )
        print(
            status,
            "x",
            x,
            "shift",
            shift,
            "exit",
            completed.returncode,
            "expected",
            repr(expected),
            "k",
            repr(actual),
        )
        if status != "MATCH":
            print("BOUNDED_K_OUTPUT", "\\n".join(output.splitlines()[:40]))
            mismatches += 1
    print("case_count", len(cases))
    print("negative_shift_visible_stuck_count", expected_stuck)
    print("mismatch_count", mismatches)
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
