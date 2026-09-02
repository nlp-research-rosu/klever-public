#!/usr/bin/env python3
"""Concrete fixed-generic versus priority-specialized semantics comparison."""

from __future__ import annotations

import hashlib
import re
import shlex
import subprocess
import sys
from pathlib import Path


def k_sequence(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return f"pyList({result})"


def run(program: Path, definition: Path, values: list[int]) -> subprocess.CompletedProcess[str]:
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cINPUT={k_sequence(values)}",
    ]
    print(f"COMMAND: {shlex.join(command)}")
    return subprocess.run(command, text=True, capture_output=True, check=False)


def result(stdout: str) -> int | None:
    match = re.search(r"<k>\s*pyInt \( (-?\d+) \) ~> \.K", stdout)
    return int(match.group(1)) if match else None


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: operational_bridge_compare.py PROGRAM SPECIALIZED_DEFINITION GENERIC_DEFINITION",
            file=sys.stderr,
        )
        return 64

    program, specialized_definition, generic_definition = map(Path, sys.argv[1:])
    cases = [
        ("len-nil-true", []),
        ("len-singleton-true", [11]),
        ("len-false-parity-even", [9, 8]),
        ("len-false-parity-odd", [9, 7]),
        ("negative-even-and-live-recursive-continuation", [-1, -2, -3, -4, -5]),
        ("multiple-live-add-and-call-continuations", [2, 3, 4, 6, 8, 10]),
    ]

    failures = 0
    for label, values in cases:
        print(f"CASE: {label}")
        print(f"VALUES: {values!r}")
        print("SPECIALIZED:")
        specialized = run(program, specialized_definition, values)
        print("GENERIC_BASELINE:")
        generic = run(program, generic_definition, values)
        specialized_hash = hashlib.sha256(specialized.stdout.encode()).hexdigest()
        generic_hash = hashlib.sha256(generic.stdout.encode()).hexdigest()
        equal = specialized.stdout == generic.stdout
        print(
            "RESULTS: "
            f"specialized_exit={specialized.returncode} generic_exit={generic.returncode} "
            f"specialized_result={result(specialized.stdout)!r} "
            f"generic_result={result(generic.stdout)!r}"
        )
        print(f"SPECIALIZED_STDOUT_SHA256: {specialized_hash}")
        print(f"GENERIC_STDOUT_SHA256: {generic_hash}")
        print(f"COMPLETE_FINAL_CONFIGURATION_EQUAL: {equal}")
        print(f"SPECIALIZED_STDERR: {specialized.stderr.strip()!r}")
        print(f"GENERIC_STDERR: {generic.stderr.strip()!r}")
        if specialized.returncode != 0 or generic.returncode != 0 or not equal:
            failures += 1
            print("CASE_STATUS: MISMATCH")
        else:
            print("CASE_STATUS: MATCH")

    print(f"SUMMARY: cases={len(cases)} mismatches={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
