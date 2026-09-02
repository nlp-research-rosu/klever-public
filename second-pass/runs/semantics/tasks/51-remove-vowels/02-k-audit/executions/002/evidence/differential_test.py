#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py versus solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_generated"
)

documented_and_boundary_cases = [
    "",
    "abcdef\nghijklm",
    "abcdef",
    "aaaaa",
    "aaBAA",
    "zbcd",
    "a",
    "A",
    "u",
    "U",
    "b",
    "Z",
    "aeiouAEIOU",
    "bcdfgBCDFG",
    "\0\t\n\r ",
    "a\0E\nu",
    "áéíóúÁÉÍÓÚ",
    "a\u0301A\u0308e\u0301",
    "İıſKΩÅå",
    "😀a𐐀E𝔘u",
    "the quick brown fox jumps over a lazy dog",
]

checked = 0
mismatches: list[tuple[str, str, str]] = []


def check(text: str) -> None:
    global checked
    expected = canonical(text)
    actual = generated(text)
    checked += 1
    if expected != actual or not isinstance(actual, str):
        mismatches.append((repr(text), repr(expected), repr(actual)))


for case in documented_and_boundary_cases:
    check(case)

# Every ASCII/Latin-1 value in one combined string and separately.
check("".join(chr(value) for value in range(256)))
for value in range(256):
    check(chr(value))

# Exhaust every Python Unicode code point as a one-character input, including
# surrogate code points (which Python str can represent even though UTF-8 cannot).
for value in range(0x110000):
    check(chr(value))

# Deterministic broader multi-character sample, with branch-heavy ASCII and
# arbitrary code points. The seed and exact generation algorithm preserve inputs.
prng = random.Random(0x51A0D17)
ascii_pool = "aeiouAEIOUbcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ\n\t\0"
for length in [0, 1, 2, 3, 10, 31, 100]:
    for _ in range(200):
        check("".join(prng.choice(ascii_pool) for _ in range(length)))
        check("".join(chr(prng.randrange(0x110000)) for _ in range(length)))

check(("aeioubcdfgAEIOUBCDFG" * 500))

print(f"documented_and_boundary_cases={len(documented_and_boundary_cases)}")
print("unicode_singletons=1114112")
print("seed=0x51A0D17 generated_multichar_cases=2800")
print(f"total_inputs_checked={checked}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH input={mismatch[0]} expected={mismatch[1]} actual={mismatch[2]}")
raise SystemExit(1 if mismatches else 0)
