#!/usr/bin/env python3
"""Differentially compare the trusted HumanEval oracle and submitted Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random
import sys


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


oracle = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(
    Path("/tmp/audit-work/candidate/solution.py"), "submitted_solution"
)


documented = [
    "",
    "abcdef\nghijklm",
    "abcdef",
    "aaaaa",
    "aaBAA",
    "zbcd",
]

boundaries = [
    "a",
    "A",
    "u",
    "U",
    "b",
    "z",
    "AEIOUaeiou",
    "bAEIOUaeiouz",
    "\n\t\r\0",
    "café naïve résumé",
    "İıſK",
    "a\u0301e\u0301i\u0301o\u0301u\u0301",
    "😀A🚀e終",
    "x" * 4096,
    ("AEIOUaeiouxyz" * 512),
    "\ud800A\udfff",
]

rng = random.Random(510026)
alphabets = [
    "AEIOUaeioubcdfghjklmnpqrstvwxyz",
    "AEIOUaeiou\n\t 0123456789!@#$%^&*()",
    "AEIOUaeiouáéíóúÄËÏÖÜİıſK😀🚀終",
]
generated: list[str] = []
for alphabet in alphabets:
    for length in (0, 1, 2, 9, 31, 128, 1024):
        for _ in range(40):
            generated.append("".join(rng.choice(alphabet) for _ in range(length)))
for _ in range(5000):
    length = rng.randrange(0, 257)
    generated.append(
        "".join(chr(rng.randrange(0x20, 0xD800)) for _ in range(length))
    )

mismatches: list[tuple[str, str, str]] = []
for value in documented + boundaries + generated:
    expected = oracle(value)
    observed = candidate(value)
    if observed != expected:
        mismatches.append((repr(value), repr(expected), repr(observed)))
        if len(mismatches) >= 10:
            break

removed_codepoints: list[int] = []
unicode_singletons_checked = 0
if not mismatches:
    for codepoint in range(sys.maxunicode + 1):
        value = chr(codepoint)
        expected = oracle(value)
        observed = candidate(value)
        unicode_singletons_checked += 1
        if expected == "":
            removed_codepoints.append(codepoint)
        if observed != expected:
            mismatches.append((repr(value), repr(expected), repr(observed)))
            if len(mismatches) >= 10:
                break

expected_removed = [ord(char) for char in "AEIOUaeiou"]
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"generated_cases={len(generated)} seed=510026")
print(f"unicode_singletons_checked={unicode_singletons_checked}")
print("canonical_removed_codepoints=" + ",".join(f"U+{cp:04X}" for cp in removed_codepoints))
print("expected_removed_codepoints=" + ",".join(f"U+{cp:04X}" for cp in expected_removed))
print(f"mismatch_count={len(mismatches)}")
for value, expected, observed in mismatches:
    print(f"MISMATCH input={value} oracle={expected} candidate={observed}")

if removed_codepoints != expected_removed:
    print("ERROR canonical removal set was not exactly the ten ASCII vowels")
    raise SystemExit(1)
raise SystemExit(1 if mismatches else 0)
