#!/usr/bin/env python3
"""Concrete substitutions into the target claim's reversal expression."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_palindrome


canonical = load(Path("/reference/canonical.py"), "canonical_ground_48")
generated = load(Path("/candidate/solution.py"), "generated_ground_48")

cases = ["", "a", "aba", "ab", "abca", "🙂é🙂"]
print("COMMAND: python3 /audit-output/evidence/ground_substitution.py")
print(
    "FORMAL_SUBSTITUTION: S is the tuple of Python code points; "
    "buildIS(S,isLen(S)-1,-1,-1) is S[::-1]"
)
for text in cases:
    sequence = tuple(map(ord, text))
    reverse = tuple(reversed(sequence))
    claimed_result = sequence == reverse
    trusted_result = canonical(text)
    generated_result = generated(text)
    print(
        f"text={text!r} S={sequence!r} reverse={reverse!r} "
        f"claim={claimed_result} canonical={trusted_result} "
        f"generated={generated_result}"
    )
    if len({claimed_result, trusted_result, generated_result}) != 1:
        raise SystemExit(1)
print("GROUND_SUBSTITUTION_RESULT=PASS")
