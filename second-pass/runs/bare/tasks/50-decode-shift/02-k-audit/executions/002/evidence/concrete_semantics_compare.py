#!/usr/bin/env python3
"""Compare fresh krun results against independent trusted Python execution."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_canonical():
    path = Path("/reference/canonical.py")
    spec = importlib.util.spec_from_file_location("trusted_canonical_for_k", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chars_term(text: str) -> str:
    term = "nil"
    for character in reversed(text):
        term = f"cons({ord(character)},{term})"
    return term


def result_payload(output: str) -> str:
    match = re.search(r"<result>(.*?)</result>", output, flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"no result cell in output:\n{output}")
    return "".join(match.group(1).split())


def main() -> None:
    canonical = load_canonical()
    inputs = ["", "a", "e", "f", "z", "abc", "xyz", "abcdefghijklmnopqrstuvwxyz"]
    mismatches = []
    for value in inputs:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "audit-kompiled",
            f"-cINPUT={chars_term(value)}",
        ]
        completed = subprocess.run(
            command,
            cwd="/tmp/audit-work/candidate",
            text=True,
            capture_output=True,
            check=False,
        )
        expected_text = canonical.decode_shift(value)
        expected_payload = f"VChars({chars_term(expected_text)})~>.K"
        actual_payload = result_payload(completed.stdout)
        matched = completed.returncode == 0 and actual_payload == expected_payload
        print(
            f"input={value!r} command={command!r} exit={completed.returncode} "
            f"expected={expected_payload} actual={actual_payload} matched={matched}"
        )
        if not matched:
            mismatches.append((value, completed.returncode, expected_payload, actual_payload))
    print(f"concrete_case_count={len(inputs)}")
    print(f"concrete_mismatch_count={len(mismatches)}")
    assert not mismatches
    print("CONCRETE_SEMANTICS_COMPARE=PASS")


if __name__ == "__main__":
    main()
