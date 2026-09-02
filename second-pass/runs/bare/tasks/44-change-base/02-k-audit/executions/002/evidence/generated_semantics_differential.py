#!/usr/bin/env python3
"""Compare fresh generated K semantics with submitted and canonical Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shlex
import subprocess
import sys


SCRATCH = Path("/tmp/audit-work/change-base-audit-20260726")
CANDIDATE = SCRATCH / "candidate"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


canonical = load_entry(SCRATCH / "reference/canonical.py", "kdiff_canonical")
generated = load_entry(CANDIDATE / "solution.py", "kdiff_generated")

cases = [
    (8, 3),
    (8, 2),
    (7, 2),
    (1234, 7),
    (0, 2),
    (0, 9),
    (1, 2),
    (8, 9),
    (9, 9),
    (10, 9),
    (511, 2),
    (10**12, 9),
    (-1, 2),
    (-17, 9),
]

k_mismatches = 0
canonical_mismatches = 0
for index, (x, base) in enumerate(cases, 1):
    submitted_result = generated(x, base)
    canonical_result = canonical(x, base)
    pattern = f'<k> strVal("{submitted_result}") ~> .K </k>'
    command = [
        "krun",
        "solution.mpy",
        f"-cX={x}",
        f"-cBASE={base}",
        "--definition",
        "semantic-llvm-search-kompiled",
        "--pattern",
        pattern,
    ]
    process = subprocess.run(
        command,
        cwd=CANDIDATE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    k_match = process.returncode == 0 and process.stdout.strip() == "#Top"
    canonical_match = submitted_result == canonical_result
    k_mismatches += not k_match
    canonical_mismatches += not canonical_match
    print(f"case[{index}] x={x} base={base}")
    print(f"command={shlex.join(command)}")
    print(f"k_exit={process.returncode} k_output={process.stdout.strip()!r}")
    print(
        f"submitted={submitted_result!r} canonical={canonical_result!r} "
        f"k_matches_submitted={k_match} submitted_matches_canonical={canonical_match}"
    )

print(f"case_count={len(cases)}")
print(f"k_vs_submitted_mismatch_count={k_mismatches}")
print(f"submitted_vs_canonical_mismatch_count={canonical_mismatches}")
sys.exit(1 if k_mismatches else 0)
