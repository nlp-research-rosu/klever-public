#!/usr/bin/env python3
"""Independent differential test for HumanEval/154.

The oracle is the trusted /reference/canonical.py entry point.  The system
under test is the candidate's generated solution.py entry point.  Neither
implementation is copied or reimplemented here.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cycpattern_check


scratch = Path("/tmp/audit-work/154-cycpattern-check")
canonical = load_entry(scratch / "canonical.py", "trusted_canonical")
generated = load_entry(scratch / "solution.py", "candidate_solution")

documented = [
    ("abcd", "abd"),
    ("hello", "ell"),
    ("whassup", "psus"),
    ("abab", "baa"),
    ("efef", "eeff"),
    ("himenss", "simen"),
]

# Explicitly cover loop-skipped, first-rotation hit, later-rotation hit,
# complete miss, singleton, pattern longer than haystack, and empty strings.
boundaries = [
    ("", ""),
    ("anything", ""),
    ("", "a"),
    ("a", "a"),
    ("a", "b"),
    ("ab", "ba"),
    ("ba", "ab"),
    ("a", "aa"),
    ("abc", "bca"),
    ("abc", "cab"),
    ("abc", "acb"),
    ("éa", "aé"),
    ("🙂x", "x🙂"),
]


def words(alphabet: str, max_len: int):
    yield ""
    for size in range(1, max_len + 1):
        for chars in itertools.product(alphabet, repeat=size):
            yield "".join(chars)


generated_cases = [
    (a, b) for a in words("ab", 4) for b in words("ab", 4)
]

all_cases = []
seen = set()
for source, cases in [
    ("documented", documented),
    ("boundary", boundaries),
    ("generated", generated_cases),
]:
    for a, b in cases:
        if (a, b) not in seen:
            all_cases.append((source, a, b))
            seen.add((a, b))

mismatches = []
counts = {"documented": 0, "boundary": 0, "generated": 0}
for source, a, b in all_cases:
    counts[source] += 1
    expected = canonical(a, b)
    actual = generated(a, b)
    if expected != actual:
        mismatches.append((source, a, b, expected, actual))

print(f"oracle={scratch / 'canonical.py'}:cycpattern_check")
print(f"candidate={scratch / 'solution.py'}:cycpattern_check")
print(f"unique_cases={len(all_cases)}")
print(f"case_counts={counts}")
print(f"mismatch_count={len(mismatches)}")
for source, a, b, expected, actual in mismatches:
    print(
        "MISMATCH "
        f"source={source} a={a!r} b={b!r} "
        f"canonical={expected!r} candidate={actual!r}"
    )

raise SystemExit(1 if mismatches else 0)
