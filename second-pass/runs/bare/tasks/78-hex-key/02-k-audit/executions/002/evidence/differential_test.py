#!/usr/bin/env python3
"""Independent differential test for HumanEval 78 (hex_key)."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/rebuild/solution.py")
ALPHABET = "0123456789ABCDEF"
PRIME_DIGITS = frozenset("2357BD")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


canonical = load_entry("trusted_hex_key_canonical", CANONICAL_PATH)
generated = load_entry("candidate_hex_key_generated", GENERATED_PATH)

seen: set[str] = set()
inputs: list[str] = []


def add(value: str) -> None:
    if value not in seen:
        seen.add(value)
        inputs.append(value)


# Prompt examples and explicit loop/membership boundaries.
for value in (
    "",
    "AB",
    "1077E",
    "ABED1A33",
    "123456789ABCDEF0",
    "2020",
    "0",
    "2",
    "A",
    "B",
    "F",
    "23",
    "20",
    "02",
    "FF",
    "BD",
    "DB",
):
    add(value)

# Every singleton digit and uniform repetitions stress each membership outcome.
for digit in ALPHABET:
    add(digit)
    add(digit * 2)
    add(digit * 31)

# Exhaust every valid input through length four.
for length in range(5):
    for chars in itertools.product(ALPHABET, repeat=length):
        add("".join(chars))

# Deterministic broader samples include long inputs without narrowing the domain.
rng = random.Random(0x78)
for _ in range(512):
    length = rng.randint(5, 256)
    add("".join(rng.choice(ALPHABET) for _ in range(length)))

input_digest = hashlib.sha256()
mismatches: list[tuple[str, int, int, int]] = []
for value in inputs:
    encoded = value.encode("ascii")
    input_digest.update(len(encoded).to_bytes(8, "big"))
    input_digest.update(encoded)
    expected = sum(character in PRIME_DIGITS for character in value)
    canonical_result = canonical(value)
    generated_result = generated(value)
    if canonical_result != generated_result or canonical_result != expected:
        mismatches.append(
            (value, canonical_result, generated_result, expected)
        )

print(f"canonical_path={CANONICAL_PATH}")
print(f"generated_path={GENERATED_PATH}")
print(f"alphabet={ALPHABET}")
print("exhaustive_lengths=0..4")
print("deterministic_random_seed=0x78")
print("deterministic_random_cases=512 lengths=5..256")
print(f"unique_inputs={len(inputs)}")
print(f"serialized_input_sha256={input_digest.hexdigest()}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch!r}")
    raise SystemExit(1)
print("DIFFERENTIAL_TEST_PASS")
