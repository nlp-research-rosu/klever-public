#!/usr/bin/env python3
"""Compare freshly rebuilt generated K semantics with both Python functions."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable, List


SCRATCH = Path("/tmp/audit-work/7-filter-by-substring")
DEFINITION = SCRATCH / "semantic-llvm-kompiled"
PROGRAM = SCRATCH / "solution.mpy"


def load_entry(path: Path, name: str) -> Callable[[List[str], str], List[str]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


def k_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def k_list(values: List[str]) -> str:
    result = "Nil"
    for value in reversed(values):
        result = f"Cons({k_string(value)},{result})"
    return result


def normalize_final_k(stdout: str) -> str:
    compact = re.sub(r"\s+", "", stdout)
    match = re.fullmatch(r"<k>(.*)~>\.K</k>", compact)
    if not match:
        raise AssertionError(f"unexpected final configuration: {stdout!r}")
    return match.group(1)


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_k")
    candidate = load_entry(SCRATCH / "solution.py", "scratch_candidate_k")
    cases = [
        ("empty-list", [], "a"),
        ("prompt-normal", ["abc", "bacd", "cde", "array"], "a"),
        ("empty-substring", ["x", "x", ""], ""),
        ("all-drop", ["bbb", "", "cccc"], "a"),
        ("exact-and-boundaries", ["ab", "abx", "xab", "xaby", "x"], "ab"),
        ("needle-longer", ["a", "ab", ""], "abc"),
    ]

    mismatches = 0
    for label, strings, substring in cases:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            "-cFUNCTION=" + k_string("filter_by_substring"),
            "-cINPUT=" + k_list(strings),
            "-cSUBSTRING=" + k_string(substring),
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"CASE: {label}")
        print(f"COMMAND: {shlex.join(command)}")
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        print("KRUN_STDOUT:")
        print(completed.stdout.rstrip())
        if completed.stderr:
            print("KRUN_STDERR:")
            print(completed.stderr.rstrip())

        expected = canonical(strings, substring)
        candidate_result = candidate(strings, substring)
        expected_term = k_list(expected)
        try:
            actual_term = normalize_final_k(completed.stdout)
        except AssertionError as error:
            actual_term = f"<PARSE-ERROR: {error}>"
        print(f"CANONICAL_PYTHON: {expected!r}")
        print(f"CANDIDATE_PYTHON: {candidate_result!r}")
        print(f"EXPECTED_K_TERM: {expected_term}")
        print(f"ACTUAL_K_TERM: {actual_term}")
        agrees = (
            completed.returncode == 0
            and candidate_result == expected
            and actual_term == expected_term
        )
        print(f"AGREES: {str(agrees).lower()}")
        print()
        if not agrees:
            mismatches += 1

    print(f"case_count={len(cases)}")
    print(f"mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
