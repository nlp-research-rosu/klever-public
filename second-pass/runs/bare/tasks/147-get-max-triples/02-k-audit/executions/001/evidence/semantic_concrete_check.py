#!/usr/bin/env python3
"""Compare fresh krun executions with two independent Python entry points."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path

WORK = Path("/tmp/audit-work/audit147")
DEFINITION = WORK / "fresh-runtime-kompiled"
PROGRAM = WORK / "regenerated-solution.mpy"
INPUTS = [0, 1, 2, 3, 4, 5, 10, 29, 30, 31]


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_for_krun")
generated = load_entry(WORK / "solution.py", "generated_for_krun")

failures: list[str] = []
for n in INPUTS:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cN={n}",
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    combined = completed.stdout + completed.stderr
    match = re.search(r"<result>\s*result\s*\(\s*(-?\d+)\s*\)\s*</result>", combined)
    k_value = int(match.group(1)) if match else None
    canonical_value = canonical(n)
    generated_value = generated(n)
    print(f"$ {' '.join(command)}")
    print(f"n={n} exit={completed.returncode} K={k_value} "
          f"canonical={canonical_value} generated={generated_value}")
    if completed.returncode != 0 or k_value != canonical_value or k_value != generated_value:
        failures.append(
            f"n={n}: exit={completed.returncode}, K={k_value}, "
            f"canonical={canonical_value}, generated={generated_value}"
        )
        print(combined)

print(f"input_scope={INPUTS}")
print(f"mismatch_count={len(failures)}")
for failure in failures:
    print(f"MISMATCH {failure}")
if failures:
    raise SystemExit(1)
print("RESULT=PASS")
