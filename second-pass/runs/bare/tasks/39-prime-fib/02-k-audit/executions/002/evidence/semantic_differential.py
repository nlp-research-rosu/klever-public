#!/usr/bin/env python3
"""Compare fresh generated K semantics with the submitted Python program."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/39-prime-fib/src")
DEFINITION = ROOT / "audit-semantic-llvm-kompiled"


def load_solution():
    path = ROOT / "solution.py"
    spec = importlib.util.spec_from_file_location("audit_semantic_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_result(n: int) -> tuple[int, str]:
    command = [
        "krun",
        str(ROOT / "solution.mpy"),
        "--definition",
        str(DEFINITION),
        f"-cN={n}",
        "--output",
        "pretty",
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    print(f"KRUN_COMMAND n={n}: {' '.join(command)}")
    print(f"KRUN_EXIT n={n}: {result.returncode}")
    if result.stderr:
        print(f"KRUN_STDERR n={n}: {result.stderr.strip()}")
    if result.returncode != 0:
        raise AssertionError((n, result.returncode, result.stdout, result.stderr))
    if not re.search(r"<k>\s*\.K\s*</k>", result.stdout):
        raise AssertionError(f"n={n}: residual computation:\n{result.stdout}")
    match = re.search(r"<result>\s*(-?[0-9]+)\s*</result>", result.stdout)
    if match is None:
        raise AssertionError(f"n={n}: missing integer result:\n{result.stdout}")
    return int(match.group(1)), result.stdout


def main() -> None:
    solution = load_solution()
    inputs = [-1, 0, 1, 2, 3, 4, 5]
    mismatches = []
    print(f"INPUTS {inputs}")
    for n in inputs:
        observed, output = k_result(n)
        expected = solution.prime_fib(n)
        env_match = re.search(r"<env>(.*?)</env>", output, re.DOTALL)
        env = " ".join(env_match.group(1).split()) if env_match else "MISSING"
        print(
            f"COMPARE n={n} k={observed} python={expected} "
            f"final_env={env}"
        )
        if observed != expected:
            mismatches.append((n, observed, expected))
    print(f"MISMATCHES {len(mismatches)}")
    assert not mismatches, mismatches


if __name__ == "__main__":
    main()
