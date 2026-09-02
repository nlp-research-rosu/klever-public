#!/usr/bin/env python3
"""Independent differential test for HumanEval 86 anti_shuffle."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import string
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/86-anti-shuffle/solution.py")
)

documented = {
    "Hi": "Hi",
    "hello": "ehllo",
    "Hello World!!!": "Hello !!!Wdlor",
}

boundary_cases = [
    "",
    " ",
    "  ",
    "a",
    "ba",
    "ab",
    " a",
    "a ",
    " a ",
    "a  b",
    "  ba  dc ",
    "\tba\n",
    "321  cba",
    "!!!",
    "\x00b a",
    "éΩ a",
    "z" * 1024,
]

# Exhaust all strings through length five over an alphabet that crosses the
# separator/non-separator, upper/lower case, digit, and punctuation boundaries.
generated_cases = [
    "".join(chars)
    for length in range(6)
    for chars in itertools.product(" aB0!", repeat=length)
]

# Add deterministic broader strings, including whitespace other than ASCII 32
# and non-ASCII code points. Only literal ASCII space is a word separator.
rng = random.Random(860086)
random_alphabet = string.printable + "éΩ中🙂"
generated_cases.extend(
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 65)))
    for _ in range(500)
)

cases = list(dict.fromkeys([*documented, *boundary_cases, *generated_cases]))
Path("/audit-output/evidence/04-differential-inputs.json").write_text(
    json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8"
)

mismatches = []
for value in cases:
    expected = canonical(value)
    actual = generated(value)
    if expected != actual:
        mismatches.append({"input": value, "canonical": expected, "generated": actual})

example_failures = []
for value, expected in documented.items():
    canonical_value = canonical(value)
    generated_value = generated(value)
    if canonical_value != expected or generated_value != expected:
        example_failures.append(
            {
                "input": value,
                "stated": expected,
                "canonical": canonical_value,
                "generated": generated_value,
            }
        )

print("oracle=/reference/canonical.py:anti_shuffle")
print("generated=/tmp/audit-work/86-anti-shuffle/solution.py:anti_shuffle")
print("documented_examples=3")
print("explicit_boundary_cases=" + str(len(boundary_cases)))
print("exhaustive_alphabet=' aB0!'")
print("exhaustive_max_length=5")
print("deterministic_random_cases=500 seed=860086 max_length=64")
print("total_unique_inputs=" + str(len(cases)))
print("example_failures=" + str(len(example_failures)))
print("mismatches=" + str(len(mismatches)))

if example_failures or mismatches:
    print(
        json.dumps(
            {"example_failures": example_failures, "mismatches": mismatches[:20]},
            ensure_ascii=False,
            indent=2,
        )
    )
    sys.exit(1)
