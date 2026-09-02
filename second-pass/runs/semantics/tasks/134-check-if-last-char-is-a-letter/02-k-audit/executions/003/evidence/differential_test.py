#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval 134."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/candidate/solution.py"), "generated_candidate"
)

documented = ["apple pie", "apple pi e", "apple pi e ", ""]
branch_boundaries = [
    "a",
    "A",
    "7",
    "!",
    "ab",
    "a ",
    "a b",
    "a B",
    "a  b",
    "a !",
    " é",
    "é",
    " β",
    "β",
]

# Exhaust all strings through length four over a branch-focused alphabet.
alphabet = " aA0!?éβ"
exhaustive = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(134)
generated = [
    "".join(rng.choice(alphabet + "bzZ9") for _ in range(rng.randrange(0, 25)))
    for _ in range(1000)
]

inputs = list(dict.fromkeys(documented + branch_boundaries + exhaustive + generated))
mismatches = []
for text in inputs:
    expected = canonical(text)
    actual = candidate(text)
    if expected != actual:
        mismatches.append((text, expected, actual))

print(f"documented={len(documented)}")
print(f"branch_boundaries={len(branch_boundaries)}")
print(f"exhaustive_alphabet={alphabet!r}")
print(f"exhaustive_max_length=4")
print(f"seeded_generated=1000 seed=134 max_length=24")
print(f"unique_inputs={len(inputs)}")
print(f"mismatches={len(mismatches)}")
for text, expected, actual in mismatches[:40]:
    print(
        f"mismatch input={text!r} canonical={expected!r} candidate={actual!r}"
    )

raise SystemExit(1 if mismatches else 0)
