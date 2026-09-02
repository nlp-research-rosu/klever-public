#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/73-smallest-change-fresh")
DEFINITION = WORK / "semantic-kompiled-fresh"
PROGRAM = WORK / "solution.mpy"


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


def k_list(values: list[int]) -> str:
    if not values:
        return ".List"
    return " ".join(f"ListItem({value})" for value in values)


canonical = load_function(Path("/reference/canonical.py"), "semantic_canonical")
candidate = load_function(Path("/candidate/solution.py"), "semantic_candidate")
cases = [
    [],
    [7],
    [1, 1],
    [1, 2],
    [2, 9, 2],
    [2, 9, 3],
    [-5, 0, -5],
    [-5, 0, 6],
    [1, 2, 3, 5, 4, 7, 9, 6],
    [1, 2, 3, 4, 3, 2, 2],
    [1, 2, 3, 2, 1],
    [10**30, -2, 8, 10**30],
    [10**30, -2, 9, -(10**30)],
]

mismatches = []
for index, values in enumerate(cases):
    command = [
        "krun",
        str(PROGRAM),
        f"-cINPUT={k_list(values)}",
        "--definition",
        str(DEFINITION),
    ]
    print("COMMAND:", shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"CASE[{index}]={values!r}")
    print(f"KRUN_EXIT_STATUS={completed.returncode}")
    if completed.stderr:
        print("KRUN_STDERR:")
        print(completed.stderr.rstrip())
    print("KRUN_STDOUT:")
    print(completed.stdout.rstrip())
    match = re.search(
        r"<result>\s*(-?[0-9]+)(?:\s*~>\s*\.K)?\s*</result>",
        completed.stdout,
    )
    k_value = int(match.group(1)) if match else None
    py_candidate = candidate(list(values))
    py_canonical = canonical(list(values))
    print(
        f"VALUES k={k_value!r} candidate_python={py_candidate} "
        f"canonical_python={py_canonical}"
    )
    if completed.returncode or k_value != py_candidate or k_value != py_canonical:
        mismatches.append(index)

print(f"semantic_case_count={len(cases)}")
print(f"semantic_mismatch_count={len(mismatches)}")
raise SystemExit(1 if mismatches else 0)
