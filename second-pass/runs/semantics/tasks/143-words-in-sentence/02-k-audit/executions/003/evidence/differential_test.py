#!/usr/bin/env python3
"""Independent differential test for HumanEval/143.

The exact input set is reproducible from this file: explicit cases, all
single-word lengths 1..100, systematic two-word partitions, and pseudorandom
single-space-separated alphabetic sentences generated with seed 143.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/143/solution.py")
SEED = 143


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_in_sentence


canonical = load_function("trusted_canonical_143", CANONICAL_PATH)
generated = load_function("generated_solution_143", GENERATED_PATH)

cases = [
    "This is a test",
    "lets go for swimming",
    "",
    "a",
    "aa",
    "aaa",
    "aaaa",
    "a bb ccc dddd eeeee ffffff ggggggg",
    "single",
    "a" * 100,
    "a" * 97 + " bb",
    "a  bb",       # robustness outside the single-space form
    " aa ",        # robustness outside the no-edge-space form
]

# Every candidate prime-test equality and every adjacent non-prime length is
# covered by evaluating all possible one-word lengths in the stated 1..100
# sentence-length domain.
cases.extend("a" * n for n in range(1, 101))

# Systematic multiword boundaries, always keeping total sentence length <=100.
for left in range(1, 50):
    for right in (1, 2, 3, 4, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        sentence = "a" * left + " " + "b" * right
        if len(sentence) <= 100:
            cases.append(sentence)

rng = random.Random(SEED)
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for _ in range(500):
    remaining = rng.randint(1, 100)
    lengths = []
    while remaining > 0:
        if lengths:
            if remaining == 1:
                break
            remaining -= 1  # separator
        length = rng.randint(1, remaining)
        lengths.append(length)
        remaining -= length
        if rng.random() < 0.35:
            break
    words = [
        "".join(rng.choice(alphabet) for _ in range(length))
        for length in lengths
    ]
    cases.append(" ".join(words))

# Stable de-duplication retains the first occurrence and therefore a stable
# exact input sequence.
cases = list(dict.fromkeys(cases))
serialized = json.dumps(cases, ensure_ascii=True, separators=(",", ":"))
mismatches = []
for sentence in cases:
    expected = canonical(sentence)
    actual = generated(sentence)
    if actual != expected:
        mismatches.append(
            {"input": sentence, "canonical": expected, "generated": actual}
        )

print(f"canonical={CANONICAL_PATH}")
print(f"generated={GENERATED_PATH}")
print(f"seed={SEED}")
print(f"case_count={len(cases)}")
print(f"inputs_json_sha256={hashlib.sha256(serialized.encode()).hexdigest()}")
print("scope=examples; empty/out-of-contract robustness; all one-word lengths "
      "1..100; systematic two-word boundaries; 500 seeded generated sentences")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], ensure_ascii=True, indent=2))
    raise SystemExit(1)
