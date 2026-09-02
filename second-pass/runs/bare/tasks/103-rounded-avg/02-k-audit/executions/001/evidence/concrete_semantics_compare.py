#!/usr/bin/env python3
"""Compare freshly rebuilt generated K semantics with independent CPython execution."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/103-rounded-avg")
PROGRAM = SCRATCH / "candidate-src/solution.mpy"
DEFINITION = SCRATCH / "semantic-audit-kompiled"
CANDIDATE_PY = SCRATCH / "candidate-src/solution.py"
CANONICAL_PY = Path("/reference/canonical.py")

CASES = [
    ("normal", 1, 5),
    ("reversed-empty-interval", 7, 5),
    ("minimum-singleton", 1, 1),
    ("half-tie-lower-odd", 1, 2),
    ("half-tie-lower-even", 2, 3),
    ("equal-branch-boundary", 8, 8),
    ("adjacent-reversed-boundary", 9, 8),
    ("binary64-precision-boundary", 2**53 + 1, 2**53 + 1),
    ("binary64-overflow", 10**400, 10**400),
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


def python_outcome(function, n: int, m: int):
    try:
        value = function(n, m)
    except Exception as error:
        return ("exception", type(error).__name__, str(error))
    if isinstance(value, int):
        return ("intVal", value)
    if isinstance(value, str) and (value.startswith("0b") or value.startswith("-0b")):
        return ("binVal", int(value, 2), value)
    return ("other", type(value).__name__, repr(value))


def parse_k_result(stdout: str):
    compact = " ".join(stdout.split())
    match = re.search(r"<result> result \( (intVal|binVal) \( (-?[0-9]+) \) \) </result>", compact)
    if not match:
        return ("unparsed", compact)
    return (match.group(1), int(match.group(2)))


candidate = load(CANDIDATE_PY, "audit_candidate_solution")
canonical = load(CANONICAL_PY, "audit_trusted_canonical")
mismatches = 0
print(f"program={PROGRAM}")
print(f"definition={DEFINITION}")
print(f"candidate_python={CANDIDATE_PY}")
print(f"trusted_canonical={CANONICAL_PY}")

for label, n, m in CASES:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cN={n}",
        f"-cM={m}",
    ]
    print("\n$ " + " ".join(shlex.quote(part) for part in command))
    completed = subprocess.run(
        command,
        cwd=SCRATCH / "candidate-src",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"[exit {completed.returncode}]")
    print(completed.stdout.rstrip())
    k_result = parse_k_result(completed.stdout)
    generated_result = python_outcome(candidate, n, m)
    canonical_result = python_outcome(canonical, n, m)
    comparable_generated = generated_result[:2]
    agrees = completed.returncode == 0 and k_result == comparable_generated
    print(
        f"COMPARE label={label} n={n} m={m} "
        f"k={k_result!r} generated_python={generated_result!r} "
        f"canonical_python={canonical_result!r} agrees={agrees}"
    )
    if not agrees:
        mismatches += 1

print(f"\ncase_count={len(CASES)}")
print(f"k_vs_generated_python_mismatch_count={mismatches}")
sys.exit(1 if mismatches else 0)
