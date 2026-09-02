#!/usr/bin/env python3
"""Independent differential tests for HumanEval/82 prime_length."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prime_length


def independent_oracle(value: str) -> bool:
    n = len(value)
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


canonical = load_entry("trusted_canonical_82", Path("/reference/canonical.py"))
candidate = load_entry("candidate_solution_82", Path("/candidate/solution.py"))

documented = ["Hello", "abcdcba", "kittens", "orange"]
boundaries = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "abcdefg",
    "abcdefgh",
    "a" * 9,
    "a" * 10,
    "a" * 11,
    "a" * 12,
    "é",
    "éé",
    "😀😀😀",
    "e\u0301",
    "e\u0301e\u0301",
    "\x00\x00",
]

# One ASCII and one non-ASCII case at each length exercises all loop/if
# boundaries up through 300, including primes, composites, and repeated
# post-divisor iterations after `prime` first becomes false.
systematic = ["x" * n for n in range(301)]
systematic += ["λ" * n for n in range(301)]

rng = random.Random(820082)
alphabet = ["a", "Z", "0", "é", "λ", "😀", "\u0301", "\x00"]
generated = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 301)))
    for _ in range(250)
]

cases = documented + boundaries + systematic + generated
serialized = json.dumps(cases, ensure_ascii=True, separators=(",", ":")).encode()
failures = []
for index, value in enumerate(cases):
    expected = canonical(value)
    actual = candidate(value)
    oracle = independent_oracle(value)
    if actual != expected or actual != oracle:
        failures.append(
            {
                "index": index,
                "repr": repr(value),
                "length": len(value),
                "canonical": expected,
                "candidate": actual,
                "oracle": oracle,
            }
        )

examples_expected = [True, True, True, False]
examples_actual = [candidate(value) for value in documented]
assert examples_actual == examples_expected
assert not failures, failures[:20]

print(f"documented examples: {len(documented)} passed")
print(f"explicit empty/branch/Unicode boundaries: {len(boundaries)} passed")
print("systematic lengths: 0..300, ASCII and non-ASCII, passed")
print("generated cases: 250, seed 820082, lengths 0..300, passed")
print(f"total comparisons: {len(cases)}")
print(f"serialized input sha256: {hashlib.sha256(serialized).hexdigest()}")
print("oracles: trusted canonical.py and independent sqrt trial division")
print("mismatches: 0")
