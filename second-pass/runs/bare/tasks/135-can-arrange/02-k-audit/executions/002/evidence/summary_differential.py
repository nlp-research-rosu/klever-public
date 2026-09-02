#!/usr/bin/env python3
"""Finite evidence that verification.k's answer equations match the oracle."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location("summary_oracle_135", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


canonical = load(Path("/reference/canonical.py"))


def proof_answer(array, offset, length):
    """Direct executable rendition of answer/answerStep in verification.k."""
    if length <= 1:
        return -1
    recursive = proof_answer(array, offset + 1, length - 1)
    if recursive != -1:
        return recursive + 1
    if array[offset + 1] < array[offset]:
        return 1
    return -1


checked = 0
mismatches = []


def check(array, offset=0, length=None):
    global checked
    length = len(array) - offset if length is None else length
    checked += 1
    model = proof_answer(array, offset, length)
    oracle = canonical(array[offset : offset + length])
    if model != oracle:
        mismatches.append((array, offset, length, model, oracle))


for length in range(0, 9):
    for permutation in itertools.permutations(range(length)):
        check(list(permutation))

rng = random.Random(135_135)
for _ in range(5000):
    size = rng.randrange(0, 61)
    array = rng.sample(range(-10000, 10001), size)
    offset = rng.randrange(0, size + 1)
    length = rng.randrange(0, size - offset + 1)
    check(array, offset, length)

print(
    "SCOPE exhaustive_distinct_permutations_n0_through_n8=46234 "
    f"seeded_random_valid_views=5000 total={checked}"
)
print(f"MISMATCH_COUNT {len(mismatches)}")
for mismatch in mismatches[:10]:
    array, offset, length, model, oracle = mismatch
    print(
        f"MISMATCH array={array!r} offset={offset} length={length} "
        f"proof_answer={model} canonical={oracle}"
    )

raise SystemExit(1 if mismatches else 0)
