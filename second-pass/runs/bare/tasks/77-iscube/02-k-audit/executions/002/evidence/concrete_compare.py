#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess


WORK = Path("/tmp/audit-work/rebuild")
CASES = [-65, -64, -63, -2, -1, 0, 1, 2, 7, 8, 9, 26, 27, 28, 63, 64, 65, 180]


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.iscube


def main() -> None:
    canonical = load_entry("trusted_canonical_kcmp", WORK / "trusted_canonical.py")
    generated = load_entry("generated_solution_kcmp", WORK / "solution.py")
    mismatches = 0
    for value in CASES:
        command = [
            "krun",
            "solution.mpy",
            f"-cN={value}",
            "--definition",
            "concrete-kompiled",
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        match = re.search(r"BoolVal \( (true|false) \)", completed.stdout)
        k_result = None if match is None else match.group(1) == "true"
        canonical_result = canonical(value)
        generated_result = generated(value)
        print("COMMAND: " + " ".join(command))
        print(
            f"EXIT_STATUS={completed.returncode} K={k_result} "
            f"generated_python={generated_result} canonical_python={canonical_result}"
        )
        if (
            completed.returncode != 0
            or k_result is None
            or k_result != generated_result
            or k_result != canonical_result
        ):
            mismatches += 1
            print("K_OUTPUT_BEGIN")
            print(completed.stdout.rstrip())
            print("K_OUTPUT_END")
    print(f"cases={CASES}")
    print(f"mismatch_count={mismatches}")
    if mismatches:
        raise SystemExit(1)
    print("CONCRETE_K_COMPARE: PASS")


if __name__ == "__main__":
    main()
