#!/usr/bin/env python3
"""Compare fresh concrete K semantics with both Python implementations."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/119-audit.IbWUru")
DEFINITION = SCRATCH / "audit-semantic-kompiled"


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


canonical = load("/reference/canonical.py", "canonical_for_k_compare")
candidate = load("/candidate/solution.py", "candidate_for_k_compare")

cases = [
    ["()(", ")"],
    [")", ")"],
    ["", ""],
    ["(", ")"],
    [")", "("],
    ["()", ""],
    ["", "()"],
    ["(", "("],
    [")(", ""],
    ["())", "("],
    ["(((", ")))"],
    ["()()", ""],
]

mismatches = 0
for value in cases:
    k_input = f'ListExpr(Str("{value[0]}"), Str("{value[1]}"))'
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={k_input}",
    ]
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        capture_output=True,
        text=True,
        timeout=30,
    )
    k_result = (
        "Yes"
        if "strVal ( yesString )" in completed.stdout
        else "No"
        if "strVal ( noString )" in completed.stdout
        else f"<no-result exit={completed.returncode}>"
    )
    canonical_result = canonical(value)
    candidate_result = candidate(value)
    ok = (
        completed.returncode == 0
        and k_result == canonical_result
        and k_result == candidate_result
    )
    mismatches += not ok
    print(
        f"COMMAND: {command!r}\n"
        f"input={value!r} K={k_result!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r} exit={completed.returncode} ok={ok}"
    )
    if not ok:
        print(f"stdout_tail={completed.stdout[-1000:]!r}")
        print(f"stderr_tail={completed.stderr[-1000:]!r}")

print(f"cases={len(cases)} mismatch_count={mismatches}")
raise SystemExit(1 if mismatches else 0)
