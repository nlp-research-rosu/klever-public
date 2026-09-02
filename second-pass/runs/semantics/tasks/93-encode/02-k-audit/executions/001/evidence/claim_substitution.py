#!/usr/bin/env python3
"""Concrete substitutions for the formal result functions and both Python entries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def swap_ascii(code: int) -> int:
    if 65 <= code <= 90:
        return code + 32
    if 97 <= code <= 122:
        return code - 32
    return code


def encode_code(code: int) -> int:
    swapped = swap_ascii(code)
    if swapped in {65, 69, 73, 79, 85, 97, 101, 105, 111, 117}:
        return swapped + 2
    return swapped


def k_summary(value: str, accumulator: str = "") -> str:
    codes = [ord(char) for char in accumulator]
    codes.extend(encode_code(ord(char)) for char in value)
    return "".join(chr(code) for code in codes)


canonical = load_module("trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py"))
submitted = load_module(
    "submitted_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

cases = ["", "test", "This is a message", "aeiouAEIOU", "xyz XYZ"]
for value in cases:
    summary = k_summary(value)
    trusted = canonical.encode(value)
    actual = submitted.encode(value)
    print(f"INPUT: {value!r}")
    print(f"  INPUT_CODES: {[ord(char) for char in value]}")
    print(f"  FORMAL_SUMMARY: {summary!r}")
    print(f"  SUMMARY_CODES: {[ord(char) for char in summary]}")
    print(f"  CANONICAL: {trusted!r}")
    print(f"  SUBMITTED: {actual!r}")
    if not (summary == trusted == actual):
        raise SystemExit(1)

print(f"LOOP_WITNESS: INPUT='test' ACC='P' RESULT={k_summary('test', 'P')!r}")
print("MISMATCHES: 0")
