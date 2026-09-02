#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/154-cycpattern-check")
DEFINITION = SCRATCH / "semantic-llvm-kompiled"
PROGRAM = SCRATCH / "solution.mpy"

CASES = [
    ("abcd", "abd"),       # documented negative
    ("hello", "ell"),      # direct rotation match
    ("abab", "baa"),       # later rotation match
    ("whassup", "psus"),   # all rotations miss
    ("abc", "cab"),        # final rotation match
    ("anything", ""),      # zero loop iterations / contract divergence
    ("", ""),              # both empty
    ("", "a"),             # empty haystack
    ("a", "a"),            # singleton hit
    ("a", "b"),            # singleton miss
    ("a", "aa"),           # pattern longer than haystack
    ("éa", "aé"),          # non-ASCII code points
    ("🙂x", "x🙂"),         # supplementary Unicode code point
]


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cycpattern_check


candidate = load_entry(SCRATCH / "solution.py", "candidate_for_k_compare")
canonical = load_entry(SCRATCH / "canonical.py", "canonical_for_k_compare")

k_candidate_mismatches = 0
k_canonical_mismatches = 0

for a, b in CASES:
    args_term = (
        f"pyStr({json.dumps(a, ensure_ascii=False)}) "
        f"pyStr({json.dumps(b, ensure_ascii=False)})"
    )
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cARGS={args_term}",
    ]
    print("COMMAND:", " ".join(repr(part) for part in command))
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"krun_exit={completed.returncode}")
    print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    match = re.search(
        r"<out>\s*Result\s*\(\s*pyBool\s*\(\s*(true|false)\s*\)\s*\)\s*</out>",
        completed.stdout,
    )
    if match is None:
        raise RuntimeError("could not parse final <out> cell")
    k_result = match.group(1) == "true"
    candidate_result = candidate(a, b)
    canonical_result = canonical(a, b)
    if k_result != candidate_result:
        k_candidate_mismatches += 1
    if k_result != canonical_result:
        k_canonical_mismatches += 1
    print(
        f"RESULT a={a!r} b={b!r} K={k_result!r} "
        f"candidate={candidate_result!r} canonical={canonical_result!r}"
    )

print(f"case_count={len(CASES)}")
print(f"k_candidate_mismatch_count={k_candidate_mismatches}")
print(f"k_canonical_mismatch_count={k_canonical_mismatches}")
raise SystemExit(1 if k_candidate_mismatches else 0)
