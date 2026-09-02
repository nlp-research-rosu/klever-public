#!/usr/bin/env python3
"""Compare K's unbounded call stack with the actual CPython boundary."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path


N = 1001
WORK = Path("/tmp/audit-work/candidate-src")
DEFINITION = WORK / "audit-concrete-kompiled"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.special_factorial


def main() -> int:
    command = [
        "krun",
        "solution.mpy",
        f"-cN={N}",
        "--definition",
        str(DEFINITION),
        "--output",
        "pretty",
    ]
    print("COMMAND: " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        check=False,
        capture_output=True,
        text=True,
    )
    print(f"K_EXIT: {completed.returncode}")
    print(
        f"K_OUTPUT_BYTES: stdout={len(completed.stdout.encode())} "
        f"stderr={len(completed.stderr.encode())}"
    )
    match = re.search(r"result \( ([0-9]+) \)", completed.stdout)
    if completed.returncode or match is None:
        print("K_RESULT_PARSE: FAIL")
        print(completed.stderr[-2000:])
        return 1
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    k_value = int(match.group(1))
    print(
        f"K_RESULT: digits={len(match.group(1))} bits={k_value.bit_length()} "
        f"mod_1000000007={k_value % 1_000_000_007}"
    )

    canonical = load(
        "trusted_canonical_139_recursion_boundary",
        Path("/tmp/audit-work/trusted/canonical.py"),
    )
    candidate = load(
        "candidate_139_recursion_boundary",
        Path("/tmp/audit-work/candidate-src/solution.py"),
    )
    canonical_value = canonical(N)
    print(
        f"CANONICAL_RESULT: bits={canonical_value.bit_length()} "
        f"mod_1000000007={canonical_value % 1_000_000_007}"
    )
    print(f"K_EQUALS_CANONICAL: {k_value == canonical_value}")
    try:
        generated_value = candidate(N)
    except Exception as error:
        print(f"CANDIDATE_CPYTHON: raises {type(error).__name__}: {error}")
    else:
        print(
            f"CANDIDATE_CPYTHON: returns bits={generated_value.bit_length()} "
            f"equals_K={generated_value == k_value}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
