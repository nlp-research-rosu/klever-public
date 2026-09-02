#!/usr/bin/env python3
"""Ground Python witnesses for candidate semantic equations and solution fidelity."""

from __future__ import annotations

import importlib.util


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_witness", "/tmp/audit-work/trusted/canonical.py")
generated = load("generated_witness", "/tmp/audit-work/candidate-src/solution.py")

letter = "é"
print(
    "isalpha witness:",
    repr(letter),
    "codepoint=",
    ord(letter),
    "python_isalpha=",
    letter.isalpha(),
    "candidate_isAlpha_ASCII=",
    (65 <= ord(letter) <= 90) or (97 <= ord(letter) <= 122),
)
print(
    "swapcase witness:",
    repr(letter),
    "python_swapcase=",
    repr(letter.swapcase()),
    "python_swapcase_codepoints=",
    [ord(c) for c in letter.swapcase()],
    "candidate_toggle=",
    ord(letter),
)

value = "aⅠ"
print(
    "solution witness:",
    repr(value),
    "canonical=",
    repr(canonical.solve(value)),
    "generated=",
    repr(generated.solve(value)),
    "roman_isalpha=",
    "Ⅰ".isalpha(),
    "roman_swapcase=",
    repr("Ⅰ".swapcase()),
)

if not letter.isalpha() or letter.swapcase() != "É":
    raise SystemExit(1)
if canonical.solve(value) == generated.solve(value):
    raise SystemExit(1)
