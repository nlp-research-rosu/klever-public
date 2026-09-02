#!/usr/bin/env python3
"""Execute the copied generated semantics and compare it with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work")
SOURCE = SCRATCH / "candidate-src"
RUN_DIR = SCRATCH / "fresh-run-terms"
DEFINITION = SCRATCH / "concrete-kompiled"


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


def main() -> int:
    RUN_DIR.mkdir(exist_ok=True)
    program = (SOURCE / "solution.mpy").read_text().strip()
    canonical = load_function(
        "concrete_test_canonical", SCRATCH / "reference" / "canonical.py"
    )
    candidate = load_function(
        "concrete_test_candidate", SOURCE / "solution.py"
    )
    cases = [
        (12, 15),  # documented nonempty example; odd upper with room
        (13, 12),  # documented empty example
        (1, 1),    # smallest positive odd singleton
        (1, 2),    # smallest even upper endpoint
        (2, 3),    # odd upper endpoint with room
        (3, 3),    # odd singleton
        (4, 3),    # adjacent empty interval
        (10**40 + 1, 10**40 + 9),  # unbounded-integer behavior
    ]
    failures = []
    for x, y in cases:
        term_file = RUN_DIR / f"run-{x}-{y}.mpy"
        term_file.write_text(f"Run(\n{program},\n  Int({x}), Int({y}))\n")
        command = [
            "krun",
            str(term_file),
            "--definition",
            str(DEFINITION),
        ]
        print("COMMAND: " + " ".join(command))
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"EXIT_STATUS: {completed.returncode}")
        print("STDOUT:")
        print(completed.stdout.rstrip())
        if completed.stderr:
            print("STDERR:")
            print(completed.stderr.rstrip())
        matches = re.findall(r"VInt\s*\(\s*(-?\d+)\s*\)", completed.stdout)
        k_value = int(matches[-1]) if matches else None
        canonical_value = canonical(x, y)
        candidate_value = candidate(x, y)
        print(
            f"COMPARE x={x} y={y} "
            f"k={k_value} canonical={canonical_value} candidate={candidate_value}"
        )
        if (
            completed.returncode != 0
            or k_value is None
            or not (k_value == canonical_value == candidate_value)
        ):
            failures.append((x, y, completed.returncode, k_value, canonical_value, candidate_value))
    print(f"case_count={len(cases)}")
    print(f"failure_count={len(failures)}")
    if failures:
        print("failures=" + repr(failures))
        return 1
    print("CONCRETE_SEMANTICS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
