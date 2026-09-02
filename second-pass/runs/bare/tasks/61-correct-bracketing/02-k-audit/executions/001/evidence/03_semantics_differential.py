#!/usr/bin/env python3
"""Compare freshly built generated K semantics with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_entry("trusted_canonical_kcheck", "/reference/canonical.py")
generated = load_entry(
    "scratch_generated_kcheck", "/tmp/audit-work/candidate-src/solution.py"
)
scratch = Path("/tmp/audit-work/candidate-src")
program = " ".join((scratch / "solution.mpy").read_text().split())
definition = scratch / "semantic-audit-kompiled"

cases = [
    "",
    "(",
    ")",
    "()",
    "(()())",
    ")(()",
    ")(",
    "((",
    "))",
    "((()))",
    "()()",
    "(()",
    "())",
    "(" * 16 + ")" * 16,
]

mismatches = []
records = []
for case in cases:
    term = (
        f"Run({program}, "
        f'{json.dumps("correct_bracketing")}, {json.dumps(case)})'
    )
    command = [
        "krun",
        "--definition",
        str(definition),
        f"-cPGM={term}",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd=scratch,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
        check=False,
    )
    matches = re.findall(r"boolVal\s*\(\s*(true|false)\s*\)", completed.stdout)
    k_value = None if not matches else matches[-1] == "true"
    canonical_value = canonical(case)
    generated_value = generated(case)
    ok = (
        completed.returncode == 0
        and k_value is not None
        and k_value == canonical_value == generated_value
    )
    record = {
        "input": case,
        "canonical": canonical_value,
        "generated_python": generated_value,
        "generated_k_semantics": k_value,
        "krun_exit": completed.returncode,
        "match": ok,
        "krun_output": completed.stdout.strip(),
    }
    records.append(record)
    if not ok:
        mismatches.append(record)

print(
    json.dumps(
        {
            "definition": str(definition),
            "case_count": len(cases),
            "mismatch_count": len(mismatches),
            "cases": records,
        },
        indent=2,
    )
)
raise SystemExit(1 if mismatches else 0)
