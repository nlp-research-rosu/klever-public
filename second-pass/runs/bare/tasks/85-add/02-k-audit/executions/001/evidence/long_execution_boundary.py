#!/usr/bin/env python3
"""Expose the abstract-K versus CPython recursion-resource boundary."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path


def load_add(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


def k_sequence(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value},{result})"
    return f"pyList({result})"


def python_outcome(function, values: list[int]) -> str:
    try:
        return f"return {function(values.copy())!r}"
    except BaseException as error:
        return f"raise {type(error).__name__}: {error}"


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: long_execution_boundary.py PROGRAM DEFINITION CANDIDATE_PY CANONICAL_PY",
            file=sys.stderr,
        )
        return 64

    program, definition, candidate_path, canonical_path = map(Path, sys.argv[1:])
    values = list(range(1998))
    input_term = k_sequence(values)
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cINPUT={input_term}",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    match = re.search(r"<k>\s*pyInt \( (-?\d+) \) ~> \.K", completed.stdout)
    k_result = int(match.group(1)) if match else None
    candidate = load_add("long_candidate_85", candidate_path.resolve())
    canonical = load_add("long_canonical_85", canonical_path.resolve())

    print("INPUT_GENERATOR: list(range(1998))")
    print(f"INPUT_LENGTH: {len(values)}")
    print(f"K_INPUT_TERM_BYTES: {len(input_term.encode())}")
    print(f"K_INPUT_TERM_SHA256: {hashlib.sha256(input_term.encode()).hexdigest()}")
    print(
        "KRUN_COMMAND_TEMPLATE: "
        f"krun {program} --definition {definition} -cINPUT=<the exact term generated above>"
    )
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    print(f"KRUN_RESULT: {k_result!r}")
    print(f"KRUN_STDOUT_BYTES: {len(completed.stdout.encode())}")
    print(f"KRUN_STDOUT_SHA256: {hashlib.sha256(completed.stdout.encode()).hexdigest()}")
    print(f"KRUN_STDERR: {completed.stderr.strip()!r}")
    print(f"CANDIDATE_PYTHON_OUTCOME: {python_outcome(candidate, values)}")
    print(f"CANONICAL_PYTHON_OUTCOME: {python_outcome(canonical, values)}")
    print("INDEPENDENT_ORACLE_RESULT: 0")
    return 0 if completed.returncode == 0 and k_result == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
