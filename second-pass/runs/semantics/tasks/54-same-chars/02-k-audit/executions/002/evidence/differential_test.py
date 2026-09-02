#!/usr/bin/env python3
"""Independent same_chars differential test against the trusted canonical code."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.same_chars


canonical = load_entry("trusted_canonical_54", Path("/reference/canonical.py"))
generated = load_entry("candidate_generated_54", Path("/candidate/solution.py"))

documented = [
    ("eabcdzzzz", "dddzzzzzzzddeddabc", True),
    ("abcd", "dddddddabc", True),
    ("dddddddabc", "abcd", True),
    ("eabcd", "dddddddabc", False),
    ("abcd", "dddddddabce", False),
    ("eabcdzzzz", "dddzzzzzzzddddabc", False),
]

boundary_and_unicode = [
    ("", "", True),
    ("", "a", False),
    ("a", "", False),
    ("a", "a", True),
    ("a", "aa", True),
    ("aa", "a", True),
    ("ab", "ba", True),
    ("ab", "aa", False),
    ("\0", "\0\0", True),
    ("é", "e", False),
    ("éa", "aéé", True),
    ("😀x", "x😀😀", True),
    ("😀", "😃", False),
    ("αβγ", "γβαβ", True),
]

mismatches: list[tuple[str, str, object, object]] = []
checked = 0


def check(left: str, right: str, expected: bool | None = None) -> None:
    global checked
    oracle = canonical(left, right)
    actual = generated(left, right)
    checked += 1
    if expected is not None and oracle != expected:
        raise AssertionError((left, right, expected, oracle))
    if oracle != actual:
        mismatches.append((left, right, oracle, actual))


for left, right, expected in documented + boundary_and_unicode:
    check(left, right, expected)

small_strings = [""]
for length in range(1, 5):
    small_strings.extend("".join(chars) for chars in itertools.product("abc", repeat=length))
for left, right in itertools.product(small_strings, repeat=2):
    check(left, right)

rng = random.Random(540054)
alphabet = ["a", "b", "z", "\0", "é", "α", "😀"]
for _ in range(2000):
    left = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
    right = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
    check(left, right)

print(f"documented_cases={len(documented)}")
print(f"boundary_and_unicode_cases={len(boundary_and_unicode)}")
print(f"exhaustive_small_strings={len(small_strings)}")
print(f"exhaustive_small_pairs={len(small_strings) ** 2}")
print("random_seed=540054")
print("random_pairs=2000")
print(f"total_comparisons={checked}")
print(f"mismatch_count={len(mismatches)}")
for left, right in [("", ""), ("ab", "baa"), ("a", "b")]:
    print(
        "ground_witness="
        f"{(left, right)!r},canonical={canonical(left, right)!r},generated={generated(left, right)!r}"
    )
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
