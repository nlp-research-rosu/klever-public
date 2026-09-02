#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/80."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module("candidate_solution", Path("/tmp/audit-work/fresh/solution.py"))

cases: list[tuple[str, str]] = [
    ("example-a", "a"),
    ("example-aa", "aa"),
    ("example-abcd", "abcd"),
    ("example-aabb", "aabb"),
    ("example-adb", "adb"),
    ("example-xyy", "xyy"),
    ("empty", ""),
    ("boundary-len1", "z"),
    ("boundary-len2-distinct", "az"),
    ("boundary-len2-equal", "zz"),
    ("boundary-len3-distinct", "abc"),
    ("eq-positions-0-1", "aac"),
    ("eq-positions-0-2", "aba"),
    ("eq-positions-1-2", "abb"),
    ("later-window-failure", "abcdde"),
    ("unicode-distinct", "a🙂β"),
    ("unicode-repeat", "🙂β🙂"),
    ("embedded-nul", "a\x00b"),
]

# Exhaust all small strings over a mixed ASCII/Unicode alphabet. This covers
# every length split and every equality branch many times.
for size in range(0, 8):
    for chars in itertools.product(("a", "b", "🙂"), repeat=size):
        cases.append((f"exhaustive-mixed-len-{size}", "".join(chars)))

# Add a reproducible broader generated sample.
rng = random.Random(80080)
alphabet = ("a", "b", "c", "x", "\x00", "β", "🙂")
for number in range(600):
    size = rng.randrange(0, 80)
    cases.append(
        (f"random-{number:03d}", "".join(rng.choice(alphabet) for _ in range(size)))
    )

# This is a valid finite string for the stated contract. Every triple is
# distinct, so the canonical loop returns True, while the recursive rewrite
# crosses CPython's recursion limit.
cases.append(("long-happy-recursion-boundary", ("abc" * 400)))

mismatches: list[tuple[str, str, object, object]] = []
candidate_exceptions = 0
canonical_exceptions = 0

for label, value in cases:
    try:
        expected: object = canonical.is_happy(value)
    except Exception as exc:  # pragma: no cover - retained as audit evidence
        expected = f"{type(exc).__name__}: {exc}"
        canonical_exceptions += 1
    try:
        actual: object = candidate.is_happy(value)
    except Exception as exc:
        actual = f"{type(exc).__name__}: {exc}"
        candidate_exceptions += 1
    if actual != expected:
        mismatches.append((label, value, expected, actual))

print(f"python={sys.version.split()[0]}")
print(f"recursion_limit={sys.getrecursionlimit()}")
print(
    "scope=documented examples + explicit empty/boundary/equality cases + "
    "all strings over {a,b,🙂} of lengths 0..7 + 600 seeded strings of "
    "lengths 0..79 + one length-1200 valid string"
)
print(f"case_count={len(cases)}")
print(f"canonical_exceptions={canonical_exceptions}")
print(f"candidate_exceptions={candidate_exceptions}")
print(f"mismatch_count={len(mismatches)}")
for label, value, expected, actual in mismatches:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    print(
        f"MISMATCH label={label} length={len(value)} sha256_utf8={digest} "
        f"expected={expected!r} actual={actual!r}"
    )

raise SystemExit(1 if mismatches else 0)
