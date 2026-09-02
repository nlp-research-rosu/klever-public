#!/usr/bin/env python3
"""Compare fresh K concrete execution with trusted Python on boundary cases."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


def load_canonical():
    path = Path("/reference/canonical.py")
    spec = importlib.util.spec_from_file_location("trusted_canonical_k_compare", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


canonical = load_canonical()
program = "/tmp/audit-work/src/solution.mpy"
definition = "/tmp/audit-work/fresh-semantic-kompiled"
cases = [
    (2, 8),
    (8, 2),
    (10, 14),
    (3, 7),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 4),
    (4, 3),
    (5, 6),
    (6, 5),
    (7, 8),
    (8, 7),
    (8, 8),
    (8, 9),
    (9, 8),
    (9, 9),
    (1, 10**40),
    (10**40, 1),
]

results = []
mismatches = []
for a, b in cases:
    command = [
        "krun",
        program,
        "--definition",
        definition,
        f"-cA={a}",
        f"-cB={b}",
    ]
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    result_match = re.search(
        r"<result>\s*listVal \((.*?)\)\s*</result>", proc.stdout, re.DOTALL
    )
    got = (
        [int(x) for x in re.findall(r"ListItem \( (-?\d+) \)", result_match.group(1))]
        if result_match
        else None
    )
    want = canonical(a, b)
    terminated = bool(re.search(r"<k>\s*\.K\s*</k>", proc.stdout, re.DOTALL))
    record = {
        "a": str(a),
        "b": str(b),
        "exit": proc.returncode,
        "terminated": terminated,
        "k_result": got,
        "python_result": want,
    }
    results.append(record)
    if proc.returncode != 0 or not terminated or got != want:
        record["stderr"] = proc.stderr[-2000:]
        record["stdout_tail"] = proc.stdout[-4000:]
        mismatches.append(record)

print(json.dumps({"case_count": len(cases), "cases": results}, sort_keys=True))
print(json.dumps({"mismatch_count": len(mismatches), "mismatches": mismatches}))
raise SystemExit(1 if mismatches else 0)
