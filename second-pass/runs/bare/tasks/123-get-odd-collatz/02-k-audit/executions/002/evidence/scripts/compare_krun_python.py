#!/usr/bin/env python3
"""Compare freshly rebuilt K execution with two independent Python modules."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate-src")
DEFINITION = WORK / "semantic-audit-kompiled"
CASES = [1, 2, 3, 5, 6, 27]


def load_function(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


canonical = load_function(Path("/tmp/audit-work/reference/canonical.py"), "canonical_for_krun")
candidate = load_function(WORK / "solution.py", "candidate_for_krun")
mismatches = []
for n in CASES:
    command = [
        "krun",
        "solution.mpy",
        f"-cN={n}",
        "--definition",
        str(DEFINITION),
        "--output",
        "pretty",
    ]
    run = subprocess.run(command, cwd=WORK, text=True, capture_output=True, timeout=120)
    print("COMMAND:", " ".join(command))
    print(f"krun_exit={run.returncode}")
    if run.returncode:
        print(run.stdout)
        print(run.stderr)
        raise SystemExit(run.returncode)
    result_match = re.search(r"<result>\s*result\s*\(\s*vl\s*\((.*?)\)\s*\)\s*</result>", run.stdout, re.S)
    assert result_match, run.stdout
    k_value = [int(value) for value in re.findall(r"(-?\d+)\s*::", result_match.group(1))]
    canonical_value = canonical(n)
    candidate_value = candidate(n)
    agrees = k_value == canonical_value == candidate_value
    print(
        f"n={n} K={k_value} canonical={canonical_value} "
        f"candidate={candidate_value} all_equal={agrees}"
    )
    if not agrees:
        mismatches.append((n, k_value, canonical_value, candidate_value))
print(f"cases={CASES} mismatch_count={len(mismatches)}")
raise SystemExit(1 if mismatches else 0)
