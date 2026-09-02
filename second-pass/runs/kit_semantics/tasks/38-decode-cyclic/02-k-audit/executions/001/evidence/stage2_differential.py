#!/usr/bin/env python3
"""Independent differential oracle for candidate versus trusted canonical code."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from itertools import product
from pathlib import Path


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", "/reference/canonical.py")
candidate = load_module("generated_solution", "/candidate/solution.py")

boundary_cases = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "abcdefg",
    "abcdefgh",
    "abcdefghi",
    "abcdefghijklmn",
    "\x00",
    "\x00\x01",
    "\x00\x01\x02",
    "é",
    "λ🙂",
    "日本語",
    "a\u0301bc",
    "🙂🙃😉😊x",
    "𝄞music",
]

cases: list[str] = list(boundary_cases)
for length in range(9):
    cases.extend("".join(chars) for chars in product("aB0!", repeat=length))

rng = random.Random(0x38DEC0DE)
alphabet = ["a", "Z", "0", "!", "\x00", "é", "λ", "日", "🙂", "\u0301", "𝄞"]
for _ in range(10_000):
    length = rng.randrange(0, 101)
    cases.append("".join(rng.choice(alphabet) for _ in range(length)))

digest = hashlib.sha256()
mismatches = []
roundtrip_mismatches = []
for index, source in enumerate(cases):
    encoded = canonical.encode_cyclic(source)
    expected_direct = canonical.decode_cyclic(source)
    actual_direct = candidate.decode_cyclic(source)
    actual_roundtrip = candidate.decode_cyclic(encoded)
    digest.update(json.dumps(source, ensure_ascii=False).encode("utf-8"))
    digest.update(b"\n")
    if actual_direct != expected_direct:
        mismatches.append((index, source, expected_direct, actual_direct))
    if actual_roundtrip != source:
        roundtrip_mismatches.append((index, source, encoded, actual_roundtrip))

print(f"boundary_cases={len(boundary_cases)}")
print("exhaustive_alphabet='aB0!' exhaustive_lengths=0..8")
print("random_seed=0x38DEC0DE random_cases=10000 random_lengths=0..100")
print(f"total_cases={len(cases)}")
print(f"input_stream_sha256={digest.hexdigest()}")
print(f"canonical_candidate_mismatches={len(mismatches)}")
print(f"encode_decode_roundtrip_mismatches={len(roundtrip_mismatches)}")
if mismatches:
    print("first_direct_mismatches=", repr(mismatches[:5]))
if roundtrip_mismatches:
    print("first_roundtrip_mismatches=", repr(roundtrip_mismatches[:5]))
if mismatches or roundtrip_mismatches:
    raise SystemExit(1)
