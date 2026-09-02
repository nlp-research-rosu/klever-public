#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both CPython implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


SRC = Path("/tmp/audit-work/src")
DEFINITION = Path("/tmp/audit-work/build/semantic-llvm-kompiled")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib


def main() -> int:
    canonical = load_entry(
        "trusted_canonical_for_k", Path("/tmp/audit-work/trusted/canonical.py")
    )
    submitted = load_entry(
        "submitted_solution_for_k", Path("/tmp/audit-work/src/solution.py")
    )
    cases = [0, 1, 2, 3, 8, 10]
    mismatches = []
    print(f"cases={cases}")
    print("coverage=base-true, base-boundary, recursive-false, calls, +, -, <=")
    for n in cases:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            f"-cARG={n}",
            "--output",
            "pretty",
        ]
        print("COMMAND: " + " ".join(command))
        completed = subprocess.run(
            command,
            cwd=SRC,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        print(completed.stdout.rstrip())
        match = re.search(r"<k>\s*(-?[0-9]+)\s*~>\s*\.K\s*</k>", completed.stdout)
        k_value = int(match.group(1)) if match else None
        canonical_value = canonical(n)
        submitted_value = submitted(n)
        agrees = (
            completed.returncode == 0
            and k_value == canonical_value
            and k_value == submitted_value
        )
        print(
            f"RESULT: n={n} k={k_value} canonical={canonical_value} "
            f"submitted={submitted_value} agrees={agrees}"
        )
        if not agrees:
            mismatches.append(n)
    print(f"mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
