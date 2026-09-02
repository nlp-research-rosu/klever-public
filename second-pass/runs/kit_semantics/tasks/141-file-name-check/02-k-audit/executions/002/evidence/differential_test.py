#!/usr/bin/env python3
"""Independent contract, canonical, and candidate differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
import re
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/proof")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
generated = load_function("generated_solution", SCRATCH / "solution.py")

# Independent source-contract oracle:
# one dot; ASCII Latin first letter; txt/exe/dll suffix; <=3 ASCII digits.
VALID_SHAPE = re.compile(r"^[A-Za-z][^.]*\.(?:txt|exe|dll)$", re.ASCII)


def contract_oracle(name: str) -> str:
    shape_ok = VALID_SHAPE.fullmatch(name) is not None
    ascii_digit_count = sum(character in "0123456789" for character in name)
    return "Yes" if shape_ok and ascii_digit_count <= 3 else "No"


curated = [
    # Prompt examples and empty/boundary cases.
    "example.txt",
    "1example.dll",
    "",
    ".",
    ".txt",
    "a",
    "a.",
    "a.txt",
    "A.exe",
    "z.dll",
    # Every branch and branch boundary.
    "abc",
    "a..txt",
    "a.b.txt",
    "1.txt",
    "_a.txt",
    "a.pdf",
    "a.TXT",
    "a123.txt",
    "a1234.txt",
    "a1b2c3.exe",
    "a1b2c3d4.dll",
    "a.txtx",
    "aexe",
    # Unicode cases that distinguish the literal source contract from
    # CPython isalpha()/isdigit() behavior in the reference implementation.
    "é.txt",
    "中.exe",
    "🙂.txt",
    "aé.txt",
    "a１２３.txt",
    "a１２３４.txt",
    "a²²².txt",
    "a²²²².txt",
]

alphabet = "aZ09.txedl?é²"
exhaustive = (
    "".join(chars)
    for length in range(0, 6)
    for chars in itertools.product(alphabet, repeat=length)
)

random_generator = random.Random(141)
random_alphabet = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "._-!? "
    "é中🙂１２３²"
)
random_cases = [
    "".join(
        random_generator.choice(random_alphabet)
        for _ in range(random_generator.randrange(0, 25))
    )
    for _ in range(20_000)
]

all_inputs = list(dict.fromkeys(itertools.chain(curated, exhaustive, random_cases)))
candidate_contract_mismatches: list[tuple[str, str, str]] = []
canonical_contract_mismatches: list[tuple[str, str, str]] = []
candidate_canonical_mismatches: list[tuple[str, str, str]] = []

for name in all_inputs:
    expected = contract_oracle(name)
    canonical_result = canonical(name)
    generated_result = generated(name)
    if generated_result != expected:
        candidate_contract_mismatches.append((name, generated_result, expected))
    if canonical_result != expected:
        canonical_contract_mismatches.append((name, canonical_result, expected))
    if generated_result != canonical_result:
        candidate_canonical_mismatches.append(
            (name, generated_result, canonical_result)
        )

print(f"curated_inputs={len(curated)}")
print(f"alphabet={alphabet!r} exhaustive_lengths=0..5")
print("random_seed=141 random_cases=20000 random_lengths=0..24")
print(f"unique_inputs={len(all_inputs)}")
print(
    "candidate_contract_mismatches="
    f"{len(candidate_contract_mismatches)}"
)
print(
    "canonical_contract_mismatches="
    f"{len(canonical_contract_mismatches)}"
)
print(
    "candidate_canonical_mismatches="
    f"{len(candidate_canonical_mismatches)}"
)

for name in curated:
    print(
        "CURATED "
        f"name={name!r} contract={contract_oracle(name)} "
        f"canonical={canonical(name)} generated={generated(name)}"
    )

for label, mismatches in [
    ("CANDIDATE_CONTRACT", candidate_contract_mismatches),
    ("CANONICAL_CONTRACT", canonical_contract_mismatches),
    ("CANDIDATE_CANONICAL", candidate_canonical_mismatches),
]:
    for name, actual, expected in mismatches[:25]:
        print(
            f"{label}_MISMATCH name={name!r} actual={actual} expected={expected}"
        )

if candidate_contract_mismatches:
    sys.exit(1)
