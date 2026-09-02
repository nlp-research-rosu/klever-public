#!/usr/bin/env python3
"""Compare fresh K concrete execution against both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from generate_concrete_programs import CASES


def load_entry(module_name: str, path: Path) -> Callable[[str, str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


def python_outcome(
    function: Callable[[str, str], int], string: str, substring: str
) -> Any:
    try:
        return ("return", function(string, substring))
    except BaseException as exc:
        return ("exception", type(exc).__name__, str(exc))


def k_outcome(program_path: Path) -> tuple[Any, subprocess.CompletedProcess[str]]:
    command = [
        "krun",
        str(program_path),
        "--definition",
        "semantic-fresh-kompiled",
    ]
    process = subprocess.run(command, text=True, capture_output=True, check=False)
    if process.returncode != 0:
        return (
            ("tool-error", process.returncode, process.stderr.strip()),
            process,
        )
    match = re.search(r"<k>\s*intVal\s*\(\s*(-?[0-9]+)\s*\)", process.stdout)
    if match is None:
        return (("residual", process.stdout.strip()), process)
    return (("return", int(match.group(1))), process)


canonical = load_entry("trusted_canonical_k_compare", Path("/reference/canonical.py"))
candidate = load_entry(
    "submitted_solution_k_compare",
    Path("/tmp/audit-work/how-many-times/solution.py"),
)

mismatch_count = 0
for case_name, (string, substring) in CASES.items():
    program_path = (
        Path("/tmp/audit-work/how-many-times/concrete-programs")
        / f"{case_name}.mpy"
    )
    k_result, process = k_outcome(program_path)
    canonical_result = python_outcome(canonical, string, substring)
    candidate_result = python_outcome(candidate, string, substring)
    command = (
        f"krun {program_path} --definition semantic-fresh-kompiled"
    )
    print(f"CASE: {case_name}")
    print(f"COMMAND: {command}")
    print(f"KRUN EXIT: {process.returncode}")
    print(f"K RESULT: {k_result!r}")
    print(f"CANONICAL PYTHON: {canonical_result!r}")
    print(f"CANDIDATE PYTHON: {candidate_result!r}")
    if process.stderr:
        print(f"KRUN STDERR: {process.stderr.strip()}")
    if not (k_result == canonical_result == candidate_result):
        mismatch_count += 1
        print("COMPARISON: MISMATCH")
    else:
        print("COMPARISON: MATCH")

print(f"TOTAL CASES: {len(CASES)}")
print(f"MISMATCHES: {mismatch_count}")
sys.exit(1 if mismatch_count else 0)
