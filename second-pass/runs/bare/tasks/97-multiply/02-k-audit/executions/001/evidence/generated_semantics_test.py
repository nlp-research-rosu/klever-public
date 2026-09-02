#!/usr/bin/env python3
"""Concrete cross-check of the rebuilt generated K semantics."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

WORK = Path("/tmp/audit-work/97-multiply/candidate-source")
PROGRAM = WORK / "solution.mpy"
DEFINITION = WORK / "semantic-kompiled"
SOLUTION = WORK / "solution.py"
CANONICAL = Path("/tmp/audit-work/97-multiply/trusted/canonical.py")
RESULTS = Path("/audit-output/evidence/generated_semantics_results.json")

CASES = [
    (148, 412, "documented-normal"),
    (19, 28, "documented-normal"),
    (2020, 1851, "zero-unit-digit"),
    (14, -15, "documented-negative"),
    (-1, -1, "both-negative-branch-boundary"),
    (-1, 0, "a-negative-b-zero-boundary"),
    (-1, 1, "a-negative-only-boundary"),
    (0, -1, "a-zero-b-negative-boundary"),
    (0, 0, "both-zero-boundary"),
    (0, 1, "a-zero-b-positive-boundary"),
    (1, -1, "b-negative-only-boundary"),
    (1, 0, "b-zero-boundary"),
    (1, 1, "both-positive-boundary"),
    (-14, 15, "negative-modulo-distinguishing"),
    (14, -14, "negative-modulo-distinguishing"),
    (-14, -15, "both-negative-representative"),
    (10**60 + 7, -(10**50 + 3), "unbounded-integer-representative"),
]


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


def main() -> int:
    candidate = load_entry(SOLUTION, "semantics_candidate_solution")
    canonical = load_entry(CANONICAL, "semantics_trusted_canonical")
    rows = []
    failures = []

    for a, b, category in CASES:
        command = [
            "krun",
            str(PROGRAM),
            f"-cA={a}",
            f"-cB={b}",
            "--definition",
            str(DEFINITION),
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        match = re.search(r"<result>\s*(-?\d+)\s*</result>", completed.stdout)
        k_result = int(match.group(1)) if match else None
        python_result = candidate(a, b)
        canonical_result = canonical(a, b)
        row = {
            "category": category,
            "a": a,
            "b": b,
            "command": command,
            "krun_exit_status": completed.returncode,
            "k_result": k_result,
            "candidate_python_result": python_result,
            "trusted_canonical_result": canonical_result,
            "k_matches_candidate_python": (
                completed.returncode == 0 and k_result == python_result
            ),
            "full_krun_output": completed.stdout,
        }
        rows.append(row)
        if not row["k_matches_candidate_python"]:
            failures.append(row)
        print(
            f"COMMAND={json.dumps(command)} "
            f"EXIT={completed.returncode} "
            f"INPUT=({a},{b}) "
            f"K={k_result} "
            f"CANDIDATE_PYTHON={python_result} "
            f"CANONICAL={canonical_result} "
            f"MATCH_CANDIDATE={row['k_matches_candidate_python']}"
        )

    RESULTS.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"case_count={len(rows)}")
    print(f"k_vs_candidate_mismatch_count={len(failures)}")
    print(f"results={RESULTS}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
