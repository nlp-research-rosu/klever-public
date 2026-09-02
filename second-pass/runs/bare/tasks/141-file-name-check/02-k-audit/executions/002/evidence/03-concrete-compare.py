#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with Python execution."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/141-file-name-check")
DEFINITION = ROOT / "audit-semantics-kompiled"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


generated = load_entry("generated_solution_for_k_compare", ROOT / "solution.py")
canonical = load_entry("trusted_canonical_for_k_compare", ROOT / "canonical.py")

cases = [
    "example.txt",       # documented valid
    "1example.dll",      # first-character rejection
    "",                  # empty / zero length
    ".txt",              # empty stem
    "a",                 # zero dots
    "a.b.txt",           # two dots
    "a123.txt",          # three ASCII digits
    "a1234.txt",         # four ASCII digits
    "A.exe",             # uppercase ASCII boundary
    "z.dll",             # lowercase ASCII boundary
    "a.TXT",             # suffix case mismatch
    "a.txtx",            # suffix extension mismatch
    "é.txt",             # non-ASCII starting letter
    "a١٢٣٤.txt",         # Unicode digits are not prompt digits 0-9
    "a😀.dll",            # non-BMP interior character
]

failures: list[str] = []
for value in cases:
    encoded = json.dumps(value, ensure_ascii=False)
    cmd = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        "-cINPUT=" + encoded,
    ]
    print("$", shlex.join(cmd))
    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    print("[exit", completed.returncode, "]")
    python_value = generated(value)
    canonical_value = canonical(value)
    match = re.search(r'VStr\s*\(\s*"(Yes|No)"\s*\)', completed.stdout)
    k_value = match.group(1) if match else None
    print(
        "comparison:",
        repr(value),
        "K=", repr(k_value),
        "generated_python=", repr(python_value),
        "canonical_python=", repr(canonical_value),
    )
    if completed.returncode != 0 or k_value != python_value:
        failures.append(value)

print("case_count:", len(cases))
print("k_vs_generated_python_failure_count:", len(failures))
raise SystemExit(1 if failures else 0)
