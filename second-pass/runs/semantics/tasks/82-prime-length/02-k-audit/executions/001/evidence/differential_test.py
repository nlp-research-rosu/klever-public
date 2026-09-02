#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/82."""

from __future__ import annotations

import hashlib
import importlib.util
import math
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_prime_length(text: str) -> bool:
    """Independent sqrt-bound primality oracle for the string length."""
    n = len(text)
    if n < 2:
        return False
    return all(n % divisor for divisor in range(2, math.isqrt(n) + 1))


canonical = load_module("trusted_canonical_82", Path("/reference/canonical.py"))
generated = load_module(
    "candidate_solution_82", Path("/tmp/audit-work/82/solution.py")
)

cases: list[tuple[str, str]] = [
    ("example-Hello", "Hello"),
    ("example-palindrome", "abcdcba"),
    ("example-kittens", "kittens"),
    ("example-orange", "orange"),
    ("empty", ""),
    ("length-1", "a"),
    ("length-2-loop-not-entered", "ab"),
    ("length-3-prime-one-iteration", "abc"),
    ("length-4-first-divisor", "abcd"),
    ("length-5-prime-full-loop", "abcde"),
    ("length-6-first-divisor", "abcdef"),
    ("length-9-later-divisor", "abcdefghi"),
    ("length-11-prime", "abcdefghijk"),
    ("length-12-composite", "abcdefghijkl"),
    ("unicode-single-codepoint", "🙂"),
    ("unicode-two-codepoints", "é🙂"),
    ("combining-two-codepoints", "e\u0301"),
    ("embedded-nul-length-3", "a\x00b"),
]

# Exhaustive length coverage through 256, with deterministic varied contents.
alphabet = "aZ0é🙂"
for n in range(257):
    cases.append((f"generated-length-{n}", "".join(alphabet[i % len(alphabet)] for i in range(n))))

# Broader representative generated inputs with a fixed seed.
rng = random.Random(820082)
for index in range(160):
    n = rng.randrange(0, 401)
    text = "".join(rng.choice(alphabet) for _ in range(n))
    cases.append((f"seeded-{index}-length-{n}", text))

suite_hash = hashlib.sha256()
mismatches = 0
for index, (label, text) in enumerate(cases):
    expected = expected_prime_length(text)
    canonical_result = canonical.prime_length(text)
    generated_result = generated.prime_length(text)
    suite_hash.update(label.encode("utf-8"))
    suite_hash.update(b"\0")
    suite_hash.update(text.encode("utf-8"))
    suite_hash.update(b"\0")
    print(
        f"INPUT\t{index}\t{label}\tlen={len(text)}\t"
        f"sha256={hashlib.sha256(text.encode('utf-8')).hexdigest()}\t"
        f"canonical={canonical_result!r}\tcandidate={generated_result!r}\t"
        f"math={expected!r}"
    )
    if (
        type(canonical_result) is not bool
        or type(generated_result) is not bool
        or canonical_result != generated_result
        or generated_result != expected
    ):
        mismatches += 1
        print(f"MISMATCH\t{label}\t{text!r}")

print(f"TOTAL_CASES: {len(cases)}")
print(f"SUITE_SHA256: {suite_hash.hexdigest()}")
print(f"MISMATCHES: {mismatches}")
raise SystemExit(1 if mismatches else 0)
