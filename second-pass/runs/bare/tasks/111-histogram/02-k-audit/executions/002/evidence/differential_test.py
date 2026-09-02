#!/usr/bin/env python3
"""Independent differential test: trusted canonical versus submitted Python."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import re
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function("submitted_solution", Path("/tmp/audit-work/fresh/solution.py"))

cases: list[str] = [
    "a b c",
    "a b b a",
    "a b c a b",
    "b b b b a",
    "",
    "a",
    "a a",
    "a b",
    "a a b",
    "a b b",
    "a a b b c",
    "z z y x x",
    " a",
    "a ",
    "  a",
    "a  b",
    "   ",
]

# Exhaust all token sequences through length six over three lowercase letters,
# rendered with canonical single-space separators.
for length in range(7):
    for words in itertools.product(("a", "b", "c"), repeat=length):
        cases.append(" ".join(words))

# Exercise repeated/leading/trailing ASCII spaces, still within the documented
# "space separated lowercase letters" representation.
base_words = ["a", "b", "c", "a"]
for separators in itertools.product((" ", "  ", "   "), repeat=3):
    cases.append(base_words[0] + "".join(s + w for s, w in zip(separators, base_words[1:])))
    cases.append(" " + cases[-1] + " ")

rng = random.Random(111)
for _ in range(500):
    words = [rng.choice("abcde") for _ in range(rng.randrange(0, 25))]
    if not words:
        cases.append(rng.choice(("", " ", "  ")))
        continue
    leading = " " * rng.randrange(0, 4)
    trailing = " " * rng.randrange(0, 4)
    separators = [" " * rng.randrange(1, 5) for _ in range(len(words) - 1)]
    cases.append(leading + words[0] + "".join(s + w for s, w in zip(separators, words[1:])) + trailing)

unique_cases = list(dict.fromkeys(cases))
mismatches = []
contract_mismatches = []
representation_boundary_mismatches = []
results = []
for value in unique_cases:
    expected = canonical(value)
    actual = generated(value)
    in_contract = re.fullmatch(r"(?:[a-z](?: [a-z])*)?", value) is not None
    results.append(
        {
            "input": value,
            "canonical": expected,
            "generated": actual,
            "single_space_letter_grammar": in_contract,
        }
    )
    if expected != actual:
        mismatches.append(results[-1])
        if in_contract:
            contract_mismatches.append(results[-1])
        else:
            representation_boundary_mismatches.append(results[-1])

print(f"documented_and_boundary_cases=17")
print(f"total_unique_cases={len(unique_cases)}")
print(f"mismatch_count={len(mismatches)}")
print(f"single_space_letter_grammar_mismatch_count={len(contract_mismatches)}")
print(f"representation_boundary_mismatch_count={len(representation_boundary_mismatches)}")
print("documented_results=" + json.dumps(results[:17], sort_keys=True))
if mismatches:
    print("first_mismatches=" + json.dumps(mismatches[:20], sort_keys=True))
if contract_mismatches:
    raise SystemExit(1)
