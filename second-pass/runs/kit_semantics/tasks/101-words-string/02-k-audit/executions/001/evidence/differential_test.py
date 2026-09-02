#!/usr/bin/env python3
"""Independent differential test for HumanEval/101.

The oracle is the trusted mounted canonical implementation, imported directly
from its fixed path.  The implementation under audit is imported independently
from /candidate.  Inputs include all documented examples, explicit edge and
Unicode boundaries, exhaustive short strings, and a deterministic larger
generated sample.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


canonical = load_entry("trusted_humaneval_101_canonical", Path("/reference/canonical.py"))
generated = load_entry("candidate_humaneval_101_solution", Path("/candidate/solution.py"))

explicit = [
    # Prompt examples.
    "Hi, my name is John",
    "One, two, three, four, five, six",
    # Empty and one-character boundaries.
    "",
    "a",
    ",",
    " ",
    "\t",
    "\n",
    "\r",
    "\v",
    "\f",
    "\u00a0",
    "\u2003",
    # Canonical empty branch; comma and non-comma loop branches; split edges.
    ",,",
    "  ",
    "a,b",
    "a b",
    "a,,b",
    "a  b",
    ",a,",
    " a ",
    " , ",
    "a,\tb\nc\rd",
    # Unicode text and whitespace handled by real CPython strings.
    "naïve,café",
    "猫 狗,鳥",
    "😀, 🚀",
    "left\u00a0right",
    "left\u2003right",
    "left\u2028right",
    "left\u3000right",
    "\x00,\x00",
]

cases: list[str] = []
seen: set[str] = set()


def add(value: str) -> None:
    if value not in seen:
        seen.add(value)
        cases.append(value)


for value in explicit:
    add(value)

# Exhaust every short arrangement of ordinary word characters and both stated
# separators.  This crosses each branch at every short position.
short_alphabet = ("a", "B", "0", ",", " ")
for length in range(0, 7):
    for chars in itertools.product(short_alphabet, repeat=length):
        add("".join(chars))

# Deterministic broader strings include all CPython whitespace classes used in
# the explicit set plus non-ASCII text and NUL.
rng = random.Random(101)
wide_alphabet = list("aB09, \t\n\r\v\f") + [
    "\u00a0",
    "\u2003",
    "\u2028",
    "\u3000",
    "é",
    "猫",
    "😀",
    "\x00",
]
for _ in range(5000):
    length = rng.randrange(0, 81)
    add("".join(rng.choice(wide_alphabet) for _ in range(length)))

mismatches = []
for source in cases:
    expected = canonical(source)
    actual = generated(source)
    if actual != expected:
        mismatches.append(
            {
                "input_repr": repr(source),
                "canonical": repr(expected),
                "generated": repr(actual),
            }
        )

print("ORACLE=/reference/canonical.py:words_string")
print("SUBJECT=/candidate/solution.py:words_string")
print(f"EXPLICIT_CASES={len(explicit)}")
print(f"UNIQUE_TOTAL_CASES={len(cases)}")
print("EXHAUSTIVE_SHORT_ALPHABET=('a','B','0',',',' ') LENGTHS=0..6")
print("DETERMINISTIC_RANDOM_SEED=101 RANDOM_CASES=5000 LENGTHS=0..80")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(mismatch)
    raise SystemExit(1)
print("DIFFERENTIAL_OK")
