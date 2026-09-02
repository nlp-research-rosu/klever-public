#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval/18."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/review/trusted/canonical.py")
CANDIDATE = Path("/tmp/audit-work/review/candidate-src/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


canonical = load_entry(TRUSTED, "trusted_canonical_how_many_times")
generated = load_entry(CANDIDATE, "generated_how_many_times")

documented = [
    ("", "a"),
    ("aaa", "a"),
    ("aaaa", "aa"),
]

boundaries = [
    ("", ""),
    ("a", ""),
    ("abc", ""),
    ("", "abc"),
    ("a", "a"),
    ("a", "aa"),
    ("aa", "a"),
    ("aa", "aa"),
    ("aa", "aaa"),
    ("ababa", "aba"),
    ("aaaaa", "aaa"),
    ("abab", "ba"),
    ("abc", "c"),
    ("abc", "d"),
    ("\x00\x00", "\x00"),
    ("\n\n", "\n"),
    ("ééé", "éé"),
    ("🙂🙂🙂", "🙂🙂"),
    ("e\u0301e\u0301", "e\u0301"),
]

alphabet = ("a", "b", "🙂")
generated_exhaustive = []
for source_len in range(6):
    for source_chars in itertools.product(alphabet, repeat=source_len):
        source = "".join(source_chars)
        for pattern_len in range(5):
            for pattern_chars in itertools.product(alphabet, repeat=pattern_len):
                generated_exhaustive.append((source, "".join(pattern_chars)))

rng = random.Random(180018)
random_alphabet = ("a", "b", "é", "🙂", "\x00", "\n", "\u0301")
generated_random = [
    (
        "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 25))),
        "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 9))),
    )
    for _ in range(2000)
]

groups = [
    ("documented", documented),
    ("boundaries", boundaries),
    ("generated_exhaustive", generated_exhaustive),
    ("generated_random", generated_random),
]

seen = set()
mismatches = []
group_counts = {}
for group_name, cases in groups:
    checked = 0
    for source, pattern in cases:
        key = (source, pattern)
        if key in seen:
            continue
        seen.add(key)
        checked += 1
        expected = canonical(source, pattern)
        actual = generated(source, pattern)
        if type(actual) is not type(expected) or actual != expected:
            mismatches.append(
                {
                    "group": group_name,
                    "source": repr(source),
                    "pattern": repr(pattern),
                    "canonical": repr(expected),
                    "generated": repr(actual),
                }
            )
    group_counts[group_name] = checked

print(f"TRUSTED_ENTRY={TRUSTED}")
print(f"CANDIDATE_ENTRY={CANDIDATE}")
for name, count in group_counts.items():
    print(f"{name.upper()}_UNIQUE_CASES={count}")
print(f"TOTAL_UNIQUE_CASES={len(seen)}")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(mismatch)
    raise SystemExit(1)
