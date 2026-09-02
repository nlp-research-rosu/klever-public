#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python programs."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plist(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_module(
        "scratch_candidate", Path("/tmp/audit-work/src/solution.py")
    )
    cases = [
        ("empty/base-branch", []),
        ("singleton/base-branch", [7]),
        ("two/even-recursion-boundary", [2, 1]),
        ("prompt/even", [1, 2, 3, 4]),
        ("duplicates-negative/odd", [3, -1, 2, 3, 0]),
        ("outside-symbolic-claim-domain/even", [9, -9, 8, -8, 7, -7]),
        ("outside-symbolic-claim-domain/odd", [6, 0, 5, 1, 4, 2, 3]),
        ("arbitrary-precision", [10**100, 0, -(10**100)]),
    ]

    failures = 0
    for label, values in cases:
        canonical_result = canonical.strange_sort_list(values.copy())
        candidate_result = candidate.strange_sort_list(values.copy())
        expected_term = f"pList({plist(canonical_result)})"
        command = [
            "krun",
            "/tmp/audit-work/src/solution.mpy",
            "--definition",
            "/tmp/audit-work/build/semantic-kompiled",
            '-cENTRY="strange_sort_list"',
            f"-cINPUT={plist(values)}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        result_match = re.search(
            r"<result>\s*(.*?)\s*</result>", completed.stdout, re.DOTALL
        )
        actual_term = result_match.group(1) if result_match else "<missing-result>"
        matched = (
            completed.returncode == 0
            and candidate_result == canonical_result
            and normalized(actual_term) == normalized(expected_term)
        )
        failures += not matched
        print(f"CASE={label}")
        print(f"INPUT={values!r}")
        print(f"COMMAND={shlex.join(command)}")
        print(f"EXIT={completed.returncode}")
        print(f"PYTHON_CANONICAL={canonical_result!r}")
        print(f"PYTHON_CANDIDATE={candidate_result!r}")
        print(f"K_RESULT={actual_term.strip()}")
        print(f"MATCH={str(matched).lower()}")
        if completed.stderr:
            print(f"STDERR={completed.stderr.strip()}")

    print(f"CASES={len(cases)}")
    print(f"FAILURES={failures}")
    print(f"RESULT={'PASS' if failures == 0 else 'FAIL'}")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
