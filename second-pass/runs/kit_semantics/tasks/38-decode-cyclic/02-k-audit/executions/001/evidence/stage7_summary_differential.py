#!/usr/bin/env python3
"""Finite support for the K decodeCodes summary against the trusted oracle."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from itertools import product


def load_canonical():
    spec = importlib.util.spec_from_file_location("canonical", "/reference/canonical.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_summary_model(source: str) -> str:
    codes = [ord(character) for character in source]
    result: list[int] = []
    offset = 0
    while offset + 3 <= len(codes):
        first, second, third = codes[offset : offset + 3]
        result.extend((third, first, second))
        offset += 3
    result.extend(codes[offset:])
    return "".join(chr(code) for code in result)


canonical = load_canonical()
cases = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "\x00\x01\x02\x03",
    "é",
    "λ🙂",
    "日本語",
    "a\u0301bc",
    "𝄞music",
]
for length in range(9):
    cases.extend("".join(chars) for chars in product("aB0!", repeat=length))

rng = random.Random(0xDEC0DE38)
alphabet = ["a", "Z", "0", "!", "\x00", "é", "λ", "日", "🙂", "\u0301", "𝄞"]
for _ in range(10_000):
    cases.append(
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 101)))
    )

digest = hashlib.sha256()
mismatches = []
for index, source in enumerate(cases):
    expected = canonical.decode_cyclic(source)
    actual = k_summary_model(source)
    digest.update(json.dumps(source, ensure_ascii=False).encode())
    digest.update(b"\n")
    if actual != expected:
        mismatches.append((index, source, expected, actual))

print("proof_side_model=decodedResult chunks [a,b,c]->[c,a,b] plus decodedTail")
print("oracle=/reference/canonical.py decode_cyclic")
print("exhaustive_alphabet='aB0!' exhaustive_lengths=0..8")
print("random_seed=0xDEC0DE38 random_cases=10000 random_lengths=0..100")
print(f"total_cases={len(cases)}")
print(f"input_stream_sha256={digest.hexdigest()}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(repr(mismatches[:5]))
    raise SystemExit(1)
