#!/usr/bin/env python3
"""Fresh generated-semantics executions compared with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


work = Path("/tmp/audit-work/reconstruction")
canonical = load_module("trusted_canonical_stage3", work / "canonical.py")
generated = load_module("candidate_solution_stage3", work / "solution.py")
cases = ["", "a", "abc", "é", "😀", "a😀é", "e\u0301"]

mismatches = 0
for value in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "semantic-llvm-kompiled",
        f'-cINPUT="{value}"',
    ]
    result = subprocess.run(command, cwd=work, text=True, capture_output=True)
    combined = result.stdout + result.stderr
    matches = re.findall(r"<result>\s*Int\s*\(\s*(-?\d+)\s*\)\s*</result>", combined)
    if result.returncode != 0 or len(matches) != 1:
        print(f"COMMAND: {shlex.join(command)}")
        print(f"EXIT_STATUS: {result.returncode}")
        print(combined)
        raise SystemExit("could not obtain unique concrete K result")
    k_value = int(matches[0])
    canonical_value = canonical.strlen(value)
    generated_value = generated.strlen(value)
    case_mismatch = k_value != canonical_value or k_value != generated_value
    mismatches += int(case_mismatch)
    print(f"COMMAND: {shlex.join(command)}")
    print(f"EXIT_STATUS: {result.returncode}")
    print(
        f"input={value!r} utf8_bytes={len(value.encode('utf-8'))} "
        f"canonical={canonical_value} candidate={generated_value} "
        f"k_result={k_value} mismatch={case_mismatch}"
    )

print(f"TOTAL_CASES={len(cases)}")
print(f"K_VS_PYTHON_MISMATCHES={mismatches}")
# Exit zero when the experiment ran correctly; mismatches are an audit finding.
