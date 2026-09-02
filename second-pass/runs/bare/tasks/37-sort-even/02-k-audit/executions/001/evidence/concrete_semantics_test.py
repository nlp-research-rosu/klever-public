#!/usr/bin/env python3
"""Run clean-built K semantics and compare the result with two Python oracles."""

from __future__ import annotations

import importlib.util
import hashlib
import re
import shlex
import subprocess
import sys
from pathlib import Path


CASES = [
    [],
    [0],
    [2, 9],
    [1, 2, 3],
    [5, 6, 3, 4],
    [-1, 7, -3, 6, 0],
    [2, 9, 2, 8, 1, 7],
    list(range(2000, 0, -1)),
]


def load_sort_even(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


def pylist(values: list[int]) -> str:
    body = " ".join(f"ListItem({value})" for value in values)
    return f"pyList({body or '.List'})"


def parse_k_result(stdout: str) -> list[int]:
    match = re.search(r"<k>\s*pyList\s*\((.*?)\)\s*~>\s*\.K\s*</k>", stdout, re.S)
    if not match:
        raise ValueError("final <k> cell was not a pyList result")
    return [
        int(value)
        for value in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", match.group(1))
    ]


def summary(values):
    if not isinstance(values, list) or len(values) <= 30:
        return values
    return {
        "length": len(values),
        "first_five": values[:5],
        "last_five": values[-5:],
    }


def main() -> int:
    work = Path("/tmp/audit-work/37-sort-even")
    candidate = load_sort_even("candidate_for_k_compare", work / "solution.py")
    canonical = load_sort_even("canonical_for_k_compare", Path("/reference/canonical.py"))
    failures = []
    for case_number, values in enumerate(CASES):
        command = [
            "krun",
            "solution.mpy",
            f"-cINPUT={pylist(values)}",
            "--definition",
            "semantic-audit-kompiled",
            "--output",
            "pretty",
        ]
        print(f"CASE {case_number} INPUT={summary(values)}")
        if len(values) <= 30:
            print(f"COMMAND: {shlex.join(command)}")
        else:
            input_term = pylist(values)
            print(
                "COMMAND: krun solution.mpy "
                f"-cINPUT=<generated-pyList-sha256:{hashlib.sha256(input_term.encode()).hexdigest()}> "
                "--definition semantic-audit-kompiled --output pretty"
            )
        completed = subprocess.run(
            command, cwd=work, text=True, capture_output=True, check=False
        )
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        if completed.stderr:
            print("KRUN_STDERR:")
            print(completed.stderr.rstrip())
        try:
            k_result = parse_k_result(completed.stdout)
        except Exception as err:
            k_result = None
            print(f"K_PARSE_ERROR: {err}")
            print(completed.stdout[:4000])
        try:
            candidate_result = candidate(list(values))
        except Exception as err:
            candidate_result = f"{type(err).__name__}: {err}"
        try:
            canonical_result = canonical(list(values))
        except Exception as err:
            canonical_result = f"{type(err).__name__}: {err}"
        direct_result = list(values)
        direct_result[::2] = sorted(values[::2])
        print(f"K_RESULT={summary(k_result)}")
        print(f"CANDIDATE_PYTHON_RESULT={summary(candidate_result)}")
        print(f"TRUSTED_CANONICAL_RESULT={summary(canonical_result)}")
        print(f"DIRECT_CONTRACT_RESULT={summary(direct_result)}")
        ok = (
            completed.returncode == 0
            and k_result == candidate_result == canonical_result == direct_result
        )
        print(f"MATCH={str(ok).lower()}")
        if not ok:
            failures.append(case_number)
    print(f"CASE_COUNT={len(CASES)}")
    print(f"FAILURE_COUNT={len(failures)}")
    print(f"FAILED_CASES={failures}")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
