#!/usr/bin/env python3
"""Independent differential test for the trusted and submitted entry points."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import string
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py"))
submitted = load_module(
    "submitted_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

# The prompt says English-alphabet letters; its second example also uses spaces.
alphabet = string.ascii_letters + " "
documented = ["test", "This is a message"]
boundaries = [
    "",
    "a",
    "A",
    "e",
    "E",
    "i",
    "I",
    "o",
    "O",
    "u",
    "U",
    "b",
    "B",
    "z",
    "Z",
    " ",
    "aeiouAEIOU",
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.ascii_letters,
    "a b A B z Z",
]
exhaustive_short = [
    "".join(chars)
    for length in (1, 2)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(930093)
generated = []
for _ in range(1000):
    length = rng.randrange(0, 257)
    generated.append("".join(rng.choice(alphabet) for _ in range(length)))

cases = documented + boundaries + exhaustive_short + generated
inputs_path = Path("/audit-output/evidence/differential_inputs.jsonl")
with inputs_path.open("w", encoding="utf-8") as stream:
    for index, value in enumerate(cases):
        stream.write(json.dumps({"index": index, "input": value}) + "\n")

mismatches = []
for index, value in enumerate(cases):
    expected = canonical.encode(value)
    actual = submitted.encode(value)
    if expected != actual:
        mismatches.append((index, value, expected, actual))

print(f"ORACLE: /tmp/audit-work/trusted/canonical.py::encode")
print(f"SUBMITTED: /tmp/audit-work/candidate-src/solution.py::encode")
print(f"ALPHABET_REPR: {alphabet!r}")
print(f"DOCUMENTED_CASES: {len(documented)}")
print(f"BOUNDARY_CASES: {len(boundaries)}")
print(f"EXHAUSTIVE_LENGTH_1_2_CASES: {len(exhaustive_short)}")
print(f"SEEDED_RANDOM_CASES: {len(generated)} seed=930093 max_length=256")
print(f"TOTAL_CASES: {len(cases)}")
print(f"INPUTS_FILE: {inputs_path}")
print(f"MISMATCHES: {len(mismatches)}")
for value in documented + ["", "aeiouAEIOU", "xyz XYZ"]:
    print(
        f"SAMPLE {value!r}: canonical={canonical.encode(value)!r} "
        f"submitted={submitted.encode(value)!r}"
    )
for mismatch in mismatches[:20]:
    print(f"MISMATCH: {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
