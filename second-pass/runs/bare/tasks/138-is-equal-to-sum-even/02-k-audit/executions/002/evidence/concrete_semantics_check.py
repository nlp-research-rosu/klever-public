#!/usr/bin/env python3
"""Compare fresh K concrete execution with both independent Python functions."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_equal_to_sum_even


def main() -> int:
    root = Path("/tmp/audit-work/138-audit")
    scratch = root / "scratch"
    definition = scratch / "fresh-semantic-kompiled"
    canonical = load_function(root / "canonical.py", "canonical_for_k_compare")
    generated = load_function(scratch / "solution.py", "solution_for_k_compare")
    inputs = [
        -100,
        -1,
        0,
        4,
        6,
        7,
        8,
        9,
        10,
        12,
        100,
        10**30,
        10**30 + 1,
    ]
    mismatches = []
    for n in inputs:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(definition),
            f"-cN={n}",
        ]
        completed = subprocess.run(
            command,
            cwd=scratch,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        match = re.search(r"BoolValue\s*\(\s*(true|false)\s*\)", completed.stdout)
        k_result = None if match is None else match.group(1) == "true"
        canonical_result = canonical(n)
        generated_result = generated(n)
        agrees = (
            completed.returncode == 0
            and k_result is not None
            and k_result == canonical_result == generated_result
        )
        if not agrees:
            mismatches.append(
                (n, completed.returncode, k_result, canonical_result, generated_result)
            )
        print("COMMAND:", shlex.join(command))
        print(
            f"INPUT={n} EXIT={completed.returncode} "
            f"K={k_result} CANONICAL={canonical_result} GENERATED={generated_result} "
            f"AGREES={agrees}"
        )
        if completed.returncode != 0 or k_result is None:
            print(completed.stdout[:4000])
    print("input_count:", len(inputs))
    print("mismatch_count:", len(mismatches))
    if mismatches:
        print("mismatches:", mismatches)
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
