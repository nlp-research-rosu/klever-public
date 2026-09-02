#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential for HumanEval problem 91."""

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
    return module.is_bored


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("scratch_solution", Path("/tmp/audit-work/source/solution.py"))

fixed_cases = [
    ("prompt-example-0", "Hello world"),
    ("prompt-example-1", "The sky is blue. The sun is shining. I love this weather"),
    ("empty", ""),
    ("only-I", "I"),
    ("I-space", "I "),
    ("I-dot", "I."),
    ("word-It", "It is fine"),
    ("word-Island", "Island time"),
    ("embedded-I", "You and I are walking"),
    ("all-delimiters", ".?!"),
    ("adjacent-sentences", "A.I x?I y!I z"),
    ("leading-ascii-space", " I x"),
    ("leading-tab", "\tI x"),
    ("after-delimiter-tab", "A.\tI x"),
    ("after-delimiter-nbsp", "A.\u00a0I x"),
    ("leading-nbsp", "\u00a0I x"),
    ("ws-code-8", "\bI x"),
    ("ws-code-9", "\tI x"),
    ("ws-code-13", "\rI x"),
    ("ws-code-14", "\x0eI x"),
    ("char-before-bang", " I x"),
    ("bang", "!I x"),
    ("char-after-bang", '"I x'),
    ("char-before-dot", "-I x"),
    ("dot", ".I x"),
    ("char-after-dot", "/I x"),
    ("char-before-question", ">I x"),
    ("question", "?I x"),
    ("char-after-question", "@I x"),
    ("char-before-I", "HI x"),
    ("capital-I", "I x"),
    ("char-after-I", "J x"),
    ("I-tab-not-word-separator", "I\tx"),
    ("I-newline-not-space", "I\nx"),
    ("I-two-spaces", "I  x"),
    ("two-boredoms", "I x. I y"),
    ("reset-from-state-2", "A.I x"),
]

print("FIXED CASES")
fixed_mismatches = []
for label, value in fixed_cases:
    expected = canonical(value)
    actual = generated(value)
    match = expected == actual
    print(
        f"{label:28} input={value!r} canonical={expected} "
        f"generated={actual} match={match}"
    )
    if not match:
        fixed_mismatches.append((label, value, expected, actual))

alphabet = ("I", " ", "A", ".", "?", "!", "\t", "\u00a0")
exhaustive_mismatches = []
exhaustive_total = 0
for length in range(0, 6):
    for chars in itertools.product(alphabet, repeat=length):
        value = "".join(chars)
        exhaustive_total += 1
        expected = canonical(value)
        actual = generated(value)
        if expected != actual:
            exhaustive_mismatches.append((value, expected, actual))

rng = random.Random(910091)
random_alphabet = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    " .?!\t\n\r"
    "\u00a0\u2003"
)
random_mismatches = []
random_total = 2000
for _ in range(random_total):
    length = rng.randrange(0, 81)
    value = "".join(rng.choice(random_alphabet) for _ in range(length))
    expected = canonical(value)
    actual = generated(value)
    if expected != actual:
        random_mismatches.append((value, expected, actual))

print("\nSUMMARY")
print(f"fixed_total={len(fixed_cases)} fixed_mismatches={len(fixed_mismatches)}")
print(
    f"exhaustive_alphabet={alphabet!r} exhaustive_lengths=0..5 "
    f"exhaustive_total={exhaustive_total} "
    f"exhaustive_mismatches={len(exhaustive_mismatches)}"
)
print(
    f"random_seed=910091 random_lengths=0..80 random_total={random_total} "
    f"random_mismatches={len(random_mismatches)}"
)

print("\nFIRST 100 EXHAUSTIVE MISMATCHES")
for value, expected, actual in exhaustive_mismatches[:100]:
    print(f"input={value!r} canonical={expected} generated={actual}")

print("\nFIRST 100 RANDOM MISMATCHES")
for value, expected, actual in random_mismatches[:100]:
    print(f"input={value!r} canonical={expected} generated={actual}")

raise SystemExit(1 if fixed_mismatches or exhaustive_mismatches or random_mismatches else 0)
