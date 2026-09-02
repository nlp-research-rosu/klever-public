#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 48."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_palindrome


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_48")
generated = load_entry(Path("/candidate/solution.py"), "candidate_solution_48")


def direct_contract(text: str) -> bool:
    """Definition independent of both submitted implementations."""
    return all(text[index] == text[len(text) - 1 - index] for index in range(len(text)))


named_cases = [
    ("documented-empty", "", True),
    ("documented-odd-palindrome", "aba", True),
    ("documented-long-palindrome", "aaaaa", True),
    ("documented-first-mismatch", "zbcd", False),
    ("one-character", "x", True),
    ("two-equal", "xx", True),
    ("two-mismatch", "xy", False),
    ("even-palindrome", "abccba", True),
    ("odd-middle-free", "abcdcba", True),
    ("late-mismatch", "abca", False),
    ("embedded-nul", "a\x00a", True),
    ("newline-mismatch", "a\nb", False),
    ("combining-codepoints", "e\u0301\u0301e", True),
    ("emoji-palindrome", "🙂é🙂", True),
    ("max-codepoint-pair", "\U0010ffff\U0010ffff", True),
]

cases: list[tuple[str, str, bool | None]] = list(named_cases)
alphabet = ("a", "b", "é", "🙂")
for length in range(0, 7):
    for chars in itertools.product(alphabet, repeat=length):
        cases.append((f"exhaustive-{length}", "".join(chars), None))

rng = random.Random(480048)
random_alphabet = (
    "a",
    "b",
    "c",
    "\x00",
    "\n",
    "é",
    "\u0301",
    "🙂",
    "\U0010ffff",
)
for index in range(2000):
    length = rng.randrange(0, 65)
    text = "".join(rng.choice(random_alphabet) for _ in range(length))
    cases.append((f"random-{index}", text, None))

mismatches = []
for label, text, documented_expected in cases:
    trusted = canonical(text)
    actual = generated(text)
    contract = direct_contract(text)
    if documented_expected is not None and trusted != documented_expected:
        mismatches.append((label, text, "canonical-vs-documented", trusted, documented_expected))
    if trusted != actual or trusted != contract:
        mismatches.append((label, text, "triple", trusted, actual, contract))

print("COMMAND: python3 /audit-output/evidence/differential_audit.py")
print(
    "SCOPE: 15 named boundary/branch/Unicode cases; exhaustive lengths 0..6 "
    "over 4 symbols; 2000 deterministic random strings of lengths 0..64"
)
print(f"TOTAL_CASES={len(cases)}")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(repr(mismatch))
    raise SystemExit(1)
print("DIFFERENTIAL_RESULT=PASS")
