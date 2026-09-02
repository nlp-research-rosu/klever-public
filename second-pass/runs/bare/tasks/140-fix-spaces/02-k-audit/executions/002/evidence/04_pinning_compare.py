#!/usr/bin/env python3
"""Mechanically compare loaded submitted functions with solutionFuns."""

from __future__ import annotations

import hashlib
import json
import subprocess


def find_label(term, name: str):
    if isinstance(term, dict):
        label = term.get("label")
        if (
            term.get("node") == "KApply"
            and isinstance(label, dict)
            and label.get("name") == name
        ):
            return term
        for value in term.values():
            found = find_label(value, name)
            if found is not None:
                return found
    elif isinstance(term, list):
        for value in term:
            found = find_label(value, name)
            if found is not None:
                return found
    return None


def run(program: str):
    command = [
        "krun",
        program,
        "--definition",
        "/tmp/audit-work/build/pinning2-kompiled",
        '-cINPUT=""',
        "--output",
        "json",
    ]
    print(f"COMMAND_JSON={json.dumps(command)}")
    result = subprocess.run(command, text=True, capture_output=True)
    print(f"EXIT_STATUS={result.returncode}")
    if result.stderr:
        print(f"STDERR={result.stderr[:4000]}")
    parsed = json.loads(result.stdout) if result.returncode == 0 else None
    funs_cell = find_label(parsed, "<funs>") if parsed else None
    canonical = json.dumps(funs_cell, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    print(f"FUNS_CELL_SHA256={digest}")
    print(f"FUNS_CELL_JSON_BYTES={len(canonical.encode())}")
    return result.returncode, canonical


submitted_status, submitted = run(
    "/tmp/audit-work/build/regenerated-solution.mpy"
)
proof_status, proof_term = run(
    "/tmp/audit-work/pinning/verify-empty.mpy"
)
print(f"constructor_level_identity={submitted == proof_term}")
raise SystemExit(
    0
    if submitted_status == 0 and proof_status == 0 and submitted == proof_term
    else 1
)
