#!/usr/bin/env python3
"""Independent differential test: trusted canonical versus submitted solution."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cycpattern_check


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(Path("/tmp/audit-work/fresh/solution.py"), "candidate_solution")

prompt_examples = [
    ("abcd", "abd", False),
    ("hello", "ell", True),
    ("whassup", "psus", False),
    ("abab", "baa", True),
    ("efef", "eeff", False),
    ("himenss", "simen", True),
]

boundary_cases = [
    ("", "", True),
    ("a", "", True),
    ("abc", "", True),
    ("", "a", False),
    ("a", "a", True),
    ("a", "aa", False),
    ("ab", "ba", True),
    ("ab", "aba", False),
    ("abc", "cab", True),
    ("abc", "cba", False),
    ("aaaa", "aaaa", True),
    ("aaaa", "aaaab", False),
    ("x🙂éy", "é🙂", True),
    ("\x00ab", "b\x00", False),
]

mismatches: list[tuple[str, str, object, object, str]] = []
checked = 0


def check(a: str, b: str, source: str) -> None:
    global checked
    checked += 1
    try:
        expected = canonical(a, b)
    except Exception as err:  # pragma: no cover - evidence capture
        expected = (type(err).__name__, str(err))
    try:
        actual = generated(a, b)
    except Exception as err:  # pragma: no cover - evidence capture
        actual = (type(err).__name__, str(err))
    if expected != actual:
        mismatches.append((a, b, expected, actual, source))


for a, b, documented in prompt_examples:
    expected = canonical(a, b)
    actual = generated(a, b)
    print(
        f"PROMPT a={a!r} b={b!r} documented={documented!r} "
        f"canonical={expected!r} generated={actual!r}"
    )
    if expected != documented or actual != expected:
        mismatches.append((a, b, expected, actual, "prompt"))
    checked += 1

for a, b, documented in boundary_cases:
    expected = canonical(a, b)
    actual = generated(a, b)
    print(
        f"BOUNDARY a={a!r} b={b!r} documented={documented!r} "
        f"canonical={expected!r} generated={actual!r}"
    )
    if expected != documented:
        print("BOUNDARY_ORACLE_NOTE documented expectation differs from canonical")
    if expected != actual:
        mismatches.append((a, b, expected, actual, "boundary"))
    checked += 1

alphabet = "ab"
for a_length in range(6):
    for b_length in range(6):
        for a_chars in itertools.product(alphabet, repeat=a_length):
            a = "".join(a_chars)
            for b_chars in itertools.product(alphabet, repeat=b_length):
                check(a, "".join(b_chars), "exhaustive-ab-lengths-0-through-5")

rng = random.Random(154)
sample_alphabet = "abcé🙂\x00 "
for _ in range(5000):
    a_length = rng.randrange(0, 41)
    b_length = rng.randrange(0, 41)
    a = "".join(rng.choice(sample_alphabet) for _ in range(a_length))
    b = "".join(rng.choice(sample_alphabet) for _ in range(b_length))
    check(a, b, "seeded-random-unicode-lengths-0-through-40")

print(f"TOTAL_CHECKED={checked}")
print(f"MISMATCH_COUNT={len(mismatches)}")
for index, (a, b, expected, actual, source) in enumerate(mismatches[:100], 1):
    print(
        f"MISMATCH[{index}] source={source} a={a!r} b={b!r} "
        f"canonical={expected!r} generated={actual!r}"
    )

# This script reports mismatches but exits successfully so all evidence is retained.
raise SystemExit(0)
