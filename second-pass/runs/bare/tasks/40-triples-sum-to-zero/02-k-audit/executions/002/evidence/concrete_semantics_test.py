#!/usr/bin/env python3
"""Compare fresh concrete K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable


SOURCE_DIR = Path("/tmp/audit-work/candidate-src")
DEFINITION = Path("/tmp/audit-work/semantics-kompiled")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "semantics_oracle"
)
generated = load_entry(SOURCE_DIR / "solution.py", "semantics_candidate")

cases = [
    [],
    [1],
    [0, 0],
    [0, 0, 0],
    [1, 3, 5, 0],
    [1, 3, -2, 1],
    [1, 2, 3, 7],
    [2, 4, -5, 3, 9, 7],
    [1, -1, 0],
    [1, 1, -2],
    [1, 1, 1, -2],
    [5, -2, -2],
    [9, 8, 7, 6, -13],
    [10**50, -(10**50), 0],
]


def k_input(values: list[int]) -> str:
    ints = " ; ".join(map(str, values))
    return f"VList({ints + ' ; ' if ints else ''}.Ints)"


def run_k(values: list[int]) -> tuple[bool, list[str]]:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={k_input(values)}",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd=SOURCE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"K exit {completed.returncode}: {completed.stdout}\n{completed.stderr}"
        )
    matches = re.findall(r"result \( VBool \( (true|false) \) \)", completed.stdout)
    if matches not in (["true"], ["false"]):
        raise RuntimeError(f"unexpected K result in:\n{completed.stdout}")
    return matches[0] == "true", command


mismatches = 0
for number, values in enumerate(cases, 1):
    oracle = canonical(values)
    python_result = generated(values)
    k_result, command = run_k(values)
    same = type(oracle) is bool and oracle is python_result and oracle is k_result
    mismatches += not same
    print(
        f"case={number} values={values!r} oracle={oracle!r} "
        f"python={python_result!r} k={k_result!r} same={same}"
    )
    print(f"krun_command={shlex.join(command)}")

print(f"case_count={len(cases)} mismatch_count={mismatches}")
raise SystemExit(1 if mismatches else 0)
