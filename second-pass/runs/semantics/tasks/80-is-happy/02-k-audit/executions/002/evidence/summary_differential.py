#!/usr/bin/env python3
"""Finite check of the proof's happyFrom/isHappySpec equations."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


def happy_from(codes: tuple[int, ...], index: int) -> bool:
    if index + 2 >= len(codes):
        return True
    if codes[index] == codes[index + 1]:
        return False
    if codes[index] == codes[index + 2]:
        return False
    if codes[index + 1] == codes[index + 2]:
        return False
    return happy_from(codes, index + 1)


def is_happy_spec(value: str) -> bool:
    codes = tuple(ord(char) for char in value)
    if len(codes) < 3:
        return False
    return happy_from(codes, 0)


root = Path("/tmp/audit-work/reconstruction")
canonical = load(root / "canonical.py", "summary_canonical")
candidate = load(root / "solution.py", "summary_candidate")
tests = [
    "".join(chars)
    for length in range(9)
    for chars in itertools.product("abc", repeat=length)
]
rng = random.Random(800081)
alphabet = string.ascii_letters + string.digits + "åβ🙂𐀀\x00"
tests += [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 101)))
    for _ in range(5000)
]
mismatches = []
for value in tests:
    summary = is_happy_spec(value)
    trusted = canonical(value)
    generated = candidate(value)
    if summary != trusted or summary != generated:
        mismatches.append((value, summary, trusted, generated))
print("SCOPE exhaustive alphabet='abc' lengths=0..8 plus seed=800081")
print("TOTAL_COMPARISONS", len(tests))
print("MISMATCHES", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))
raise SystemExit(1 if mismatches else 0)
