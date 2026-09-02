#!/usr/bin/env python3
"""Execute the fresh generated K semantics and compare with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "semantic-kompiled"
PROGRAM = WORK / "solution.mpy"

CASES = [
    ("", ""),
    ("", "a"),
    ("a", ""),
    ("a", "aaaa"),
    ("ab", "ba"),
    ("ab", "aa"),
    ("eabcdzzzz", "dddzzzzzzzddeddabc"),
    ("eabcd", "dddddddabc"),
    ("é", "éé"),
    ("é", "e\u0301"),
    ("😀😀", "😀"),
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_string(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def main() -> int:
    oracle = load(
        Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical_for_k"
    ).same_chars
    subject = load(WORK / "solution.py", "candidate_solution_for_k").same_chars

    mismatches = []
    for index, (left, right) in enumerate(CASES, start=1):
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cS0={k_string(left)}",
            f"-cS1={k_string(right)}",
        ]
        print(f"CASE={index} INPUT={left!r},{right!r}")
        print(f"+ {shlex.join(command)}")
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"EXIT_STATUS={completed.returncode}")
        output = completed.stdout + completed.stderr
        match = re.search(r"result\s*\(\s*boolValue\s*\(\s*(true|false)", output)
        k_result = None if match is None else match.group(1) == "true"
        oracle_result = oracle(left, right)
        subject_result = subject(left, right)
        print(
            f"K_RESULT={k_result!r} "
            f"CANONICAL_RESULT={oracle_result!r} "
            f"SOLUTION_RESULT={subject_result!r}"
        )
        if completed.returncode != 0 or k_result is None:
            print("K_OUTPUT_BEGIN")
            print(output.rstrip())
            print("K_OUTPUT_END")
        if not (
            completed.returncode == 0
            and k_result == oracle_result
            and k_result == subject_result
        ):
            mismatches.append(
                (index, left, right, completed.returncode, k_result,
                 oracle_result, subject_result)
            )

    print(f"cases={len(CASES)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
