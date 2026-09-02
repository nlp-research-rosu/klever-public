#!/usr/bin/env python3
"""Independent differential test: trusted HumanEval oracle vs candidate source."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/candidate/solution.py"), "candidate_solution")

directed = [
    ([], "a", "documented empty-list example"),
    (["abc", "bcd", "cde", "array"], "a", "documented mixed example"),
    ([], "", "both arguments empty"),
    (["", "a", "ab"], "", "empty prefix matches every string"),
    (["", "a"], "a", "empty element does not match nonempty prefix"),
    (["a", "aa", "ba"], "aa", "exact, longer, and first-character mismatch"),
    (["ab", "ac", "a", "aba"], "ab", "later-character mismatch and short input"),
    (["a", "a", "b", "a"], "a", "duplicates and stable order"),
    (["éclair", "e\u0301clair", "😀x", "\x00a"], "é", "Unicode and NUL boundary"),
    (["\nabc", "\n", "abc"], "\n", "newline prefix"),
]

checked = 0
mismatches = []
for strings, prefix, label in directed:
    expected = canonical(strings, prefix)
    actual = candidate(strings, prefix)
    checked += 1
    if actual != expected:
        mismatches.append((label, strings, prefix, expected, actual))
    print(
        f"DIRECTED {label}: strings={strings!r} prefix={prefix!r} "
        f"expected={expected!r} actual={actual!r}"
    )

# Exhaust all lists through length 3 over all strings through length 2 formed
# from a compact alphabet.  The same set supplies prefixes.
alphabet = ("a", "b", "é")
small_strings = [""]
for length in (1, 2):
    small_strings.extend(
        "".join(chars) for chars in itertools.product(alphabet, repeat=length)
    )
for list_length in range(4):
    for values in itertools.product(small_strings, repeat=list_length):
        strings = list(values)
        for prefix in small_strings:
            expected = canonical(strings, prefix)
            actual = candidate(strings, prefix)
            checked += 1
            if actual != expected:
                mismatches.append(
                    ("exhaustive", strings, prefix, expected, actual)
                )

# A deterministic broader generated sample includes astral Unicode, combining
# characters, embedded NUL/newline, and prefixes not taken from an element.
rng = random.Random(290029)
characters = ["a", "b", "c", "é", "\u0301", "😀", "\x00", "\n"]
for _ in range(10_000):
    strings = [
        "".join(rng.choice(characters) for _ in range(rng.randrange(0, 9)))
        for _ in range(rng.randrange(0, 13))
    ]
    prefix = "".join(
        rng.choice(characters) for _ in range(rng.randrange(0, 6))
    )
    expected = canonical(strings, prefix)
    actual = candidate(strings, prefix)
    checked += 1
    if actual != expected:
        mismatches.append(("random", strings, prefix, expected, actual))

print(f"TOTAL_CASES={checked}")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
