#!/usr/bin/env python3
"""Generate a K-executable differential harness without calling sorted()."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/reconstruction/solution.py")
HARNESS = Path("/tmp/audit-work/reconstruction/reviewer-k-differential.py")
INPUTS = Path("/audit-output/evidence/05-k-differential-inputs.json")


def insertion_sort_word(word: str) -> str:
    result: list[str] = []
    for char in word:
        index = len(result)
        while index > 0 and ord(char) < ord(result[index - 1]):
            index -= 1
        result.insert(index, char)
    return "".join(result)


def oracle(text: str) -> str:
    return " ".join(insertion_sort_word(word) for word in text.split(" "))


alphabet = " !Aa~"
exhaustive = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(alphabet, repeat=length)
]
boundaries = [
    "Hi",
    "hello",
    "Hello World!!!",
    "",
    " ",
    "  ",
    " ba",
    "ba ",
    "ba  dc",
    "~!  bA ",
]
cases = list(dict.fromkeys(boundaries + exhaustive))
INPUTS.write_text(
    json.dumps(cases, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
)

solution_text = SOLUTION.read_text(encoding="utf-8").rstrip() + "\n\n"
assertions = "".join(
    f"assert anti_shuffle({text!r}) == {oracle(text)!r}\n" for text in cases
)
HARNESS.write_text(solution_text + assertions, encoding="utf-8")

encoded = json.dumps(cases, separators=(",", ":")).encode("ascii")
print(f"alphabet={alphabet!r}")
print("exhaustive_lengths=0..3")
print(f"exhaustive_generated={len(exhaustive)}")
print(f"boundary_cases={len(boundaries)}")
print(f"unique_total={len(cases)}")
print(f"inputs_sha256={hashlib.sha256(encoded).hexdigest()}")
print(f"solution_sha256={hashlib.sha256(SOLUTION.read_bytes()).hexdigest()}")
print(f"harness_sha256={hashlib.sha256(HARNESS.read_bytes()).hexdigest()}")
