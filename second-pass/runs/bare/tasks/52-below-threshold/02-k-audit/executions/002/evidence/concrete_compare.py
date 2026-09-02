#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with independent Python."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/rebuild-52")
DEFINITION = WORK / "semantic-llvm-kompiled"


def load_solution():
    spec = importlib.util.spec_from_file_location("scratch_solution", WORK / "solution.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


def intseq(items: list[int]) -> str:
    term = "nil"
    for item in reversed(items):
        term = f"cons({item}, {term})"
    return term


def main() -> int:
    solution = load_solution()
    cases = [
        ("prompt-true", [1, 2, 4, 10], 100),
        ("prompt-false", [1, 20, 4, 10], 5),
        ("empty", [], -100),
        ("equality-boundary", [5], 5),
        ("negative-pass", [-3, -2], -1),
        ("first-fails", [0, -2, -3], 0),
        ("last-fails", [-3, -2, 0], 0),
        ("large-int-pass", [-(10**100), 10**100 - 1], 10**100),
    ]
    mismatches = 0
    for label, items, threshold in cases:
        command = [
            "/usr/bin/krun",
            str(WORK / "solution.mpy"),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={intseq(items)}",
            f"-cTHRESHOLD={threshold}",
        ]
        print(f"CASE {label}")
        print("command:", shlex.join(command))
        completed = subprocess.run(
            command, cwd=WORK, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        print(completed.stdout.rstrip())
        print("krun_exit:", completed.returncode)
        match = re.search(
            r"<result>\s*result\s*\(\s*(true|false)\s*\)\s*</result>",
            completed.stdout,
            flags=re.DOTALL,
        )
        k_value = None if match is None else match.group(1) == "true"
        python_value = solution(list(items), threshold)
        math_value = all(item < threshold for item in items)
        k_cell_final = bool(
            re.search(r"<k>\s*\.K\s*</k>", completed.stdout, re.DOTALL)
        )
        print(
            f"observed: k={k_value} python={python_value} math={math_value} "
            f"k_cell_final={k_cell_final}"
        )
        if (
            completed.returncode != 0
            or k_value is None
            or k_value is not python_value
            or k_value is not math_value
        ):
            mismatches += 1
    print("cases:", len(cases))
    print("mismatches:", mismatches)
    assert mismatches == 0
    print("CONCRETE_COMPARE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
