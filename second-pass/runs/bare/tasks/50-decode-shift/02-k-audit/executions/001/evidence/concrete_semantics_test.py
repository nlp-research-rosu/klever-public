#!/usr/bin/env python3
"""Compare fresh K execution with independent trusted Python execution."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chars_term(value: str) -> str:
    term = "nil"
    for char in reversed(value):
        term = f"cons({ord(char)}, {term})"
    return term


def result_codes(output: str) -> list[int]:
    match = re.search(r"<result>\s*VChars\s*\((.*?)\)\s*~>\s*\.K\s*</result>", output, re.S)
    if match is None:
        raise ValueError("could not find completed VChars result cell")
    return [int(item) for item in re.findall(r"-?\d+", match.group(1))]


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: concrete_semantics_test.py DEFINITION PROGRAM CANONICAL BACKEND_LABEL"
        )
        return 64

    definition = Path(sys.argv[1]).resolve()
    program = Path(sys.argv[2]).resolve()
    canonical_path = Path(sys.argv[3]).resolve()
    backend_label = sys.argv[4]
    canonical = load_module("trusted_canonical_for_k", canonical_path)

    cases = {
        "empty": "",
        "decode_wrap_a": "a",
        "decode_wrap_e": "e",
        "decode_no_wrap_f": "f",
        "upper_boundary_z": "z",
        "all_letters": "abcdefghijklmnopqrstuvwxyz",
        "normal_encoded_helloworld": "mjqqtbtwqi",
        "mixed_boundaries": "aefzfae",
    }

    failures = []
    for label, encoded in cases.items():
        command = [
            "krun",
            str(program),
            "--definition",
            str(definition),
            f"-cINPUT={chars_term(encoded)}",
        ]
        print(f"CASE {label}")
        print(f"COMMAND {shlex.join(command)}")
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"KRUN_EXIT_STATUS {completed.returncode}")
        if completed.stderr:
            print("KRUN_STDERR")
            print(completed.stderr.rstrip())
        if completed.returncode != 0:
            failures.append((label, "nonzero krun exit", completed.returncode))
            continue
        try:
            actual_codes = result_codes(completed.stdout)
        except ValueError as error:
            print("KRUN_STDOUT")
            print(completed.stdout.rstrip())
            failures.append((label, str(error), None))
            continue
        expected_text = canonical.decode_shift(encoded)
        expected_codes = [ord(char) for char in expected_text]
        print(f"INPUT_TEXT {encoded!r}")
        print(f"EXPECTED_TEXT {expected_text!r}")
        print(f"EXPECTED_CODES {expected_codes}")
        print(f"K_RESULT_CODES {actual_codes}")
        match = actual_codes == expected_codes
        print(f"MATCH {str(match).lower()}")
        if not match:
            print("KRUN_STDOUT")
            print(completed.stdout.rstrip())
            failures.append((label, expected_codes, actual_codes))

    print(f"BACKEND_LABEL {backend_label}")
    print(f"CASE_COUNT {len(cases)}")
    print(f"MISMATCH_COUNT {len(failures)}")
    if failures:
        print(f"FAILURES {failures!r}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
