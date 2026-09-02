#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
submitted = load_function(
    "submitted_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

inputs = [
    "",
    "xyzXYZ",
    "Jerry",
    "AaBb!",
    "@A[Z{a",
    "Åå",
    "Éé",
    "Σσς",
    "ẞß",
    "𐐀𐐨",
    "😀😀A😀a",
]

result_pattern = re.compile(r"<result>\s*IntVal\s*\(\s*(-?\d+)\s*\)\s*</result>", re.S)
mismatches = 0
execution_failures = 0
for value in inputs:
    k_literal = json.dumps(value, ensure_ascii=False)
    command = [
        "krun",
        "/tmp/audit-work/build/solution.mpy",
        "--definition",
        "/tmp/audit-work/build/semantics-kompiled",
        f"-cINPUT={k_literal}",
    ]
    completed = subprocess.run(
        command,
        cwd="/tmp/audit-work/build",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    match = result_pattern.search(completed.stdout)
    kval = int(match.group(1)) if match else None
    cval = canonical(value)
    sval = submitted(value)
    equal = completed.returncode == 0 and kval == cval == sval
    if not equal:
        mismatches += 1
    if completed.returncode != 0 or match is None:
        execution_failures += 1
    print(
        "input="
        + ascii(value)
        + f" canonical={cval} submitted={sval} k={kval}"
        + f" krun_exit={completed.returncode} all_equal={equal}"
    )
    if completed.returncode != 0 or match is None:
        print("bounded_krun_output=" + repr(completed.stdout[-2000:]))

print(f"input_count={len(inputs)}")
print(f"execution_failure_count={execution_failures}")
print(f"semantic_mismatch_count={mismatches}")
raise SystemExit(1 if execution_failures or mismatches else 0)
