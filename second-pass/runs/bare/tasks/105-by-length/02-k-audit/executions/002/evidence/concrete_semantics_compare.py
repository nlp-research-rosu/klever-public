#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with two Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
DEFINITION = SCRATCH / "audit-concrete-kompiled"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.by_length


def input_term(values: list[int]) -> str:
    if not values:
        return "pyList(.PyVals)"
    return "pyList(" + " :: ".join(map(str, values)) + " :: .PyVals)"


def expected_term(values: list[str]) -> str:
    if not values:
        return "pyList ( .PyVals )"
    quoted = [f'"{value}"' for value in values]
    return "pyList ( " + " :: ".join(quoted) + " :: .PyVals )"


def normalize(text: str) -> str:
    return " ".join(text.split())


def main() -> int:
    canonical = load_entry(
        "trusted_humaneval_105_canonical_concrete",
        SCRATCH / "trusted" / "canonical.py",
    )
    candidate = load_entry(
        "candidate_humaneval_105_concrete", SCRATCH / "solution.py"
    )
    cases = [
        [],
        [2, 1, 1, 4, 5, 8, 2, 3],
        [1, -1, 55],
        [0, 1],
        [9, 10],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [9, 9, 5, 5, 5, 1, -7, 55],
        [-(10**50), 10**50, 1, 9],
    ]
    failures = []
    for index, values in enumerate(cases):
        canonical_value = canonical(values)
        candidate_value = candidate(values)
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "audit-concrete-kompiled",
            f"-cINPUT={input_term(values)}",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=SCRATCH,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        match = re.search(r"<result>\s*(.*?)\s*</result>", completed.stdout, re.S)
        observed = normalize(match.group(1)) if match else "<missing-result-cell>"
        expected = normalize(expected_term(canonical_value))
        ok = (
            completed.returncode == 0
            and canonical_value == candidate_value
            and observed == expected
        )
        print(f"CASE {index}: input={values!r}")
        print(f"command={shlex.join(command)}")
        print(f"exit_status={completed.returncode}")
        print(f"canonical_python={canonical_value!r}")
        print(f"candidate_python={candidate_value!r}")
        print(f"k_result={observed}")
        print(f"case_result={'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(
                {
                    "index": index,
                    "command": command,
                    "output": completed.stdout,
                    "expected": expected,
                    "observed": observed,
                }
            )

    print(f"case_count={len(cases)}")
    print(f"failure_count={len(failures)}")
    print(f"RESULT={'PASS' if not failures else 'FAIL'}")
    if failures:
        for failure in failures:
            print(failure)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
