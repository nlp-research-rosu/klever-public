#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test.

The input scope is intentionally explicit:
* documented examples;
* branch and empty-string boundaries;
* Unicode and punctuation cases;
* exhaustive strings over {"a", "b"} through lengths 6 (haystack) and 4
  (needle);
* 1,000 deterministic generated pairs through length 64; and
* a recursion-depth stress boundary on the candidate's recursive algorithm.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any


def load_entry(module_name: str, path: Path) -> Callable[[str, str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


def outcome(fn: Callable[[str, str], int], string: str, substring: str) -> Any:
    try:
        return ("return", fn(string, substring))
    except BaseException as exc:  # The exception class is observable behavior.
        return ("exception", type(exc).__name__, str(exc))


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry(
    "submitted_solution", Path("/tmp/audit-work/how-many-times/solution.py")
)

cases: list[tuple[str, str, str]] = [
    ("documented-empty", "", "a"),
    ("documented-single", "aaa", "a"),
    ("documented-overlap", "aaaa", "aa"),
    ("both-empty", "", ""),
    ("empty-needle", "abc", ""),
    ("needle-longer", "ab", "abc"),
    ("equal-match", "abc", "abc"),
    ("equal-miss", "abc", "abd"),
    ("prefix-match", "abab", "ab"),
    ("prefix-miss", "baba", "ab"),
    ("overlap-multiple", "abababa", "aba"),
    ("no-match", "abc", "z"),
    ("unicode-codepoints", "🙂🙂🙂", "🙂🙂"),
    ("combining-codepoints", "e\u0301e\u0301", "\u0301e"),
    ("punctuation", "\\0 a\\0 a", "\\0 a"),
]

alphabet = "ab"
for string_length in range(7):
    for string_tuple in itertools.product(alphabet, repeat=string_length):
        string = "".join(string_tuple)
        for substring_length in range(5):
            for substring_tuple in itertools.product(
                alphabet, repeat=substring_length
            ):
                cases.append(
                    (
                        "exhaustive-ab",
                        string,
                        "".join(substring_tuple),
                    )
                )

rng = random.Random(180018)
generated_alphabet = "abc xyz🙂"
for _ in range(1_000):
    string = "".join(
        rng.choice(generated_alphabet) for _ in range(rng.randrange(65))
    )
    substring = "".join(
        rng.choice(generated_alphabet) for _ in range(rng.randrange(17))
    )
    cases.append(("generated-seed-180018", string, substring))

# This is still in the documented str × str domain and probes the most obvious
# implementation boundary introduced by replacing the canonical loop with
# recursion.
cases.append(("recursion-depth-stress", "a" * 1_100, "z"))

mismatches: list[tuple[int, str, str, str, Any, Any]] = []
for index, (label, string, substring) in enumerate(cases):
    expected = outcome(canonical, string, substring)
    actual = outcome(candidate, string, substring)
    if expected != actual:
        mismatches.append((index, label, string, substring, expected, actual))

print("ORACLE: /reference/canonical.py::how_many_times")
print("CANDIDATE: /tmp/audit-work/how-many-times/solution.py::how_many_times")
print("EXHAUSTIVE ALPHABET: 'ab'; haystack lengths 0..6; needle lengths 0..4")
print("GENERATED: 1000 pairs; seed=180018; haystack length 0..64; needle 0..16")
print("STRESS: haystack length 1100, needle='z'")
print(f"TOTAL CASES: {len(cases)}")
print(f"MISMATCHES: {len(mismatches)}")
for index, label, string, substring, expected, actual in mismatches:
    print(
        "MISMATCH "
        f"index={index} label={label} "
        f"string={string!r} substring={substring!r} "
        f"canonical={expected!r} candidate={actual!r}"
    )

sys.exit(1 if mismatches else 0)
