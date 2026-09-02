#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 93."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encode


canonical = load_function("trusted_canonical_93", Path("/reference/canonical.py"))
candidate = load_function("candidate_solution_93", Path("/candidate/solution.py"))

documented = ["test", "This is a message"]
boundaries = [
    "",
    " ",
    "a",
    "b",
    "e",
    "i",
    "o",
    "u",
    "A",
    "B",
    "E",
    "I",
    "O",
    "U",
    "z",
    "Z",
    "aeiouAEIOU",
    "bcdfgBCDFG",
    "aA eE iI oO uU",
]
# Every ASCII alphabetic branch plus adjacent nonletter code-point boundaries.
boundaries.extend(chr(code) for code in range(0, 128))

alphabet = string.ascii_letters + " "
exhaustive = (
    "".join(chars)
    for length in range(3)
    for chars in itertools.product(alphabet, repeat=length)
)

rng = random.Random(930093)
random_cases = []
random_alphabet = "".join(chr(code) for code in range(128)) + "ßİıΣςé"
for length in [0, 1, 2, 3, 4, 7, 16, 31, 64, 257]:
    for _ in range(40):
        random_cases.append("".join(rng.choice(random_alphabet) for _ in range(length)))

checked = 0
seen: set[str] = set()
for group_name, cases in [
    ("documented", documented),
    ("boundary", boundaries),
    ("exhaustive_ascii_letters_space_len_0_to_2", exhaustive),
    ("deterministic_generated", random_cases),
]:
    group_checked = 0
    for message in cases:
        if message in seen:
            continue
        seen.add(message)
        expected = canonical(message)
        actual = candidate(message)
        if actual != expected:
            raise AssertionError(
                f"{group_name}: input={message!r} candidate={actual!r} canonical={expected!r}"
            )
        checked += 1
        group_checked += 1
    print(f"{group_name}: checked={group_checked} mismatches=0")

expected_examples = {
    "test": "TGST",
    "This is a message": "tHKS KS C MGSSCGG",
}
for message, expected in expected_examples.items():
    assert canonical(message) == expected
    assert candidate(message) == expected
    print(f"example {message!r} -> {expected!r}")

print(f"TOTAL checked={checked} mismatches=0")
