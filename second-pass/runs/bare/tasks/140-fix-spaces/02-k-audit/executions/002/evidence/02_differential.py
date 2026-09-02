#!/usr/bin/env python3
"""Compare the trusted canonical and generated Python entry points."""

from __future__ import annotations

import importlib.util
import itertools
import random
import re
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/reference/canonical.py")
)
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/candidate/solution.py")
)


def literal_prompt_contract(text: str) -> str:
    """Direct run-based reading of the prose contract, independent of both programs."""
    return "".join(
        "-" if token.startswith(" ") and len(token) > 2
        else "_" * len(token) if token.startswith(" ")
        else token
        for token in re.findall(r" +|[^ ]+", text)
    )


documented = ["Example", "Example 1", " Example 2", " Example   3"]
boundaries = [
    "",
    "a",
    " ",
    "  ",
    "   ",
    "    ",
    " a",
    "  a",
    "   a",
    "    a",
    "a ",
    "a  ",
    "a   ",
    "a    ",
    "a b",
    "a  b",
    "a   b",
    "a    b",
    " ab",
    "  ab",
    "a  b  ",
    "a   b  ",
    "\t  \n",
    "é  😀",
    "é   😀",
]
exhaustive = [
    "".join(chars)
    for length in range(0, 8)
    for chars in itertools.product((" ", "a", "é"), repeat=length)
]
rng = random.Random(140_2026_07_26)
random_cases = [
    "".join(rng.choice((" ", "a", "Z", "0", "\t", "é", "😀")) for _ in range(rng.randrange(0, 65)))
    for _ in range(4_000)
]

cases = list(dict.fromkeys(documented + boundaries + exhaustive + random_cases))
canonical_mismatches = []
literal_mismatches = []
for text in cases:
    expected = canonical(text)
    got = generated(text)
    literal = literal_prompt_contract(text)
    if got != expected:
        canonical_mismatches.append((text, expected, got))
    if got != literal:
        literal_mismatches.append((text, literal, got))

print(f"documented_examples={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print("exhaustive_scope=alphabet[' ', 'a', 'é'], lengths 0..7")
print(f"exhaustive_cases={len(exhaustive)}")
print("random_seed=14020260726")
print("random_scope=4000 strings, lengths 0..64, alphabet space/a/Z/0/tab/é/😀")
print(f"unique_total_cases={len(cases)}")
print(f"canonical_mismatch_count={len(canonical_mismatches)}")
for text, expected, got in canonical_mismatches[:20]:
    print(
        "canonical_mismatch "
        f"input={text!r} canonical={expected!r} generated={got!r}"
    )
print(f"literal_prompt_contract_mismatch_count={len(literal_mismatches)}")
for text, expected, got in literal_mismatches[:20]:
    print(
        "literal_contract_mismatch "
        f"input={text!r} expected={expected!r} generated={got!r}"
    )

raise SystemExit(1 if canonical_mismatches else 0)
