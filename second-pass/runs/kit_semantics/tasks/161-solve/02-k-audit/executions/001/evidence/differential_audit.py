#!/usr/bin/env python3
"""Independent docstring-first differential for HumanEval/161."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


CANDIDATE_PATH = Path("/tmp/audit-work/161-solve/scratch/solution.py")
CANONICAL_PATH = Path("/tmp/audit-work/161-solve/scratch/canonical.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


candidate_solve = load_function("audit_candidate_solution", CANDIDATE_PATH)
canonical_solve = load_function("audit_trusted_canonical", CANONICAL_PATH)


def contract_oracle(s: str) -> str:
    """Direct transcription of the docstring, independent of both programs."""
    if any(character.isalpha() for character in s):
        return "".join(
            character.swapcase() if character.isalpha() else character
            for character in s
        )
    return s[::-1]


def supplied_ascii_model_oracle(s: str) -> str:
    """Mirror only the audited isAlphaC/swapC supplied-model boundary."""
    def is_ascii_alpha(character: str) -> bool:
        return "A" <= character <= "Z" or "a" <= character <= "z"

    if any(is_ascii_alpha(character) for character in s):
        return "".join(
            character.swapcase() if is_ascii_alpha(character) else character
            for character in s
        )
    return s[::-1]


documented = {
    "1234": "4321",
    "ab": "AB",
    "#a@C": "#A@c",
}

boundary_cases = [
    "",
    "a",
    "A",
    "z",
    "Z",
    "0",
    "9",
    "#",
    " ",
    "\n",
    "a1",
    "1a",
    "A#",
    "#Z",
    "0123456789",
    "!@#$%^&*()",
    "aA",
    "zZ",
    "a#Z",
    "Z#a",
    "abcXYZ",
    "123# abc XYZ!",
    "é",
    "é1",
    "éa",
    "ß",
    "ß1",
    "İ",
    "Σσς",
    "Жя",
    "中文",
    "א",
    "ا",
    "e\u0301",
    "\u0301",
    "😀",
    "😀1",
    "𐐀𐐨",
    "\x00",
    "\x00a\x00",
]

small_alphabet = ["a", "Z", "0", "#", " ", "\n", "é", "ß", "Σ", "\u0301", "😀"]
exhaustive_cases = (
    "".join(chars)
    for length in range(0, 5)
    for chars in itertools.product(small_alphabet, repeat=length)
)

rng = random.Random(161)
random_pool = (
    "abcXYZ019# @\n\t"
    "éÉßİıΣσςЖя中文אا"
    "\u0301😀𐐀𐐨"
)
random_cases = [
    "".join(rng.choice(random_pool) for _ in range(rng.randrange(0, 33)))
    for _ in range(20_000)
]

tested = 0
candidate_oracle_mismatches = []
canonical_oracle_mismatches = []
candidate_canonical_mismatches = []
seen = set()


def check_case(s: str) -> None:
    global tested
    if s in seen:
        return
    seen.add(s)
    tested += 1
    expected = contract_oracle(s)
    candidate = candidate_solve(s)
    canonical = canonical_solve(s)
    if candidate != expected:
        candidate_oracle_mismatches.append((s, expected, candidate))
    if canonical != expected:
        canonical_oracle_mismatches.append((s, expected, canonical))
    if candidate != canonical:
        candidate_canonical_mismatches.append((s, candidate, canonical))


for input_string, expected in documented.items():
    actual = candidate_solve(input_string)
    if actual != expected:
        raise AssertionError(
            f"documented example failed: {input_string!r}: {actual!r} != {expected!r}"
        )
    check_case(input_string)

for input_string in boundary_cases:
    check_case(input_string)
for input_string in exhaustive_cases:
    check_case(input_string)
for input_string in random_cases:
    check_case(input_string)

assert not candidate_oracle_mismatches, candidate_oracle_mismatches[:10]
assert not canonical_oracle_mismatches, canonical_oracle_mismatches[:10]
assert not candidate_canonical_mismatches, candidate_canonical_mismatches[:10]

model_witness = "é1"
python_result = candidate_solve(model_witness)
model_result = supplied_ascii_model_oracle(model_witness)
assert python_result == "É1"
assert model_result == "1é"
assert python_result != model_result

print("DOCSTRING_EXAMPLES_PASS", len(documented))
print("BOUNDARY_CASES_DECLARED", len(boundary_cases))
print("SMALL_ALPHABET", repr(small_alphabet))
print("EXHAUSTIVE_LENGTHS", "0..4")
print("RANDOM_SEED", 161)
print("RANDOM_CASES_GENERATED", len(random_cases))
print("DISTINCT_CASES_TESTED", tested)
print("CANDIDATE_VS_CONTRACT_MISMATCHES", len(candidate_oracle_mismatches))
print("CANONICAL_VS_CONTRACT_MISMATCHES", len(canonical_oracle_mismatches))
print("CANDIDATE_VS_CANONICAL_MISMATCHES", len(candidate_canonical_mismatches))
print(
    "SUPPLIED_MODEL_DIVERGENCE_WITNESS",
    repr(model_witness),
    "CPYTHON=",
    repr(python_result),
    "ASCII_MODEL=",
    repr(model_result),
)
print("DIFFERENTIAL_PASS")
