#!/usr/bin/env python3
"""Concrete satisfying substitutions for the symbolic entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


canonical = load_entry(
    "trusted_canonical_witness", Path("/tmp/audit-work/review-19/trusted/canonical.py")
)
generated = load_entry(
    "generated_solution_witness",
    Path("/tmp/audit-work/review-19/candidate/solution.py"),
)

witnesses = [
    (".NumWords", ""),
    ("nw(zeroW, .NumWords)", "zero"),
    (
        "nw(threeW, nw(oneW, nw(fiveW, .NumWords)))",
        "three one five",
    ),
    (
        "nw(nineW, nw(zeroW, nw(nineW, nw(twoW, nw(oneW, .NumWords)))))",
        "nine zero nine two one",
    ),
]

for formal_words, encoded_input in witnesses:
    canonical_result = canonical(encoded_input)
    generated_result = generated(encoded_input)
    print(f"WORDS: {formal_words}")
    print(f"encodedWords: {encoded_input!r}")
    print(f"canonical.py: {canonical_result!r}")
    print(f"solution.py: {generated_result!r}")
    assert generated_result == canonical_result
