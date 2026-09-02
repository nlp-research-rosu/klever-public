#!/usr/bin/env python3
"""Ground substitutions for the universal entry claim.

For each realizable Python string, this independently evaluates the recursive
postcondition denotation (comma replacement followed by the supplied model's
whitespace split) and compares it with both trusted canonical and candidate
Python executions.  Cases stay within the prompt's comma/ordinary-space
separator domain, while also covering the empty and repeated-separator edges.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


def formal_denotation(source: str) -> list[str]:
    replaced_codes = [32 if ord(character) == 44 else ord(character) for character in source]
    words: list[str] = []
    token: list[int] = []
    for code in replaced_codes:
        if code in {32, 9, 10, 13}:
            if token:
                words.append("".join(chr(item) for item in token))
                token = []
        else:
            token.append(code)
    if token:
        words.append("".join(chr(item) for item in token))
    return words


canonical = load_entry("trusted_ground", Path("/reference/canonical.py"))
candidate = load_entry("candidate_ground", Path("/candidate/solution.py"))
cases = [
    "",
    ",",
    "a",
    "a,b",
    "  alpha,, beta ",
    "Hi, my name is John",
    "One, two, three, four, five, six",
]

for source in cases:
    codes = [ord(character) for character in source]
    formal = formal_denotation(source)
    trusted = canonical(source)
    generated = candidate(source)
    print(
        f"INPUT={source!r} CS={codes!r} "
        f"FORMAL={formal!r} CANONICAL={trusted!r} CANDIDATE={generated!r}"
    )
    if not (formal == trusted == generated):
        raise SystemExit(1)

print(f"GROUND_SUBSTITUTIONS_OK cases={len(cases)}")
