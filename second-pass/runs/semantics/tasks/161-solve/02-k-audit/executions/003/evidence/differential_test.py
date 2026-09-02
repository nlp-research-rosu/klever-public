#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/161."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


canonical = load_entry("/reference/canonical.py", "trusted_canonical_161")
candidate = load_entry("/candidate/solution.py", "candidate_solution_161")

hand_cases = [
    ("documented-no-letter", "1234"),
    ("documented-lower", "ab"),
    ("documented-mixed", "#a@C"),
    ("empty", ""),
    ("one-nonletter", "#"),
    ("one-lower", "a"),
    ("one-upper", "Z"),
    ("mixed-ascii", "a1B!"),
    ("ascii-boundaries-before-after", "@AZ[\\`az{"),
    ("uncased-unicode-letter", "中"),
    ("uncased-unicode-plus-digit", "1中"),
    ("unicode-cased", "éΣςİıß"),
    ("uncased-unicode-two", "中文"),
]

seen = set()
cases: list[tuple[str, str]] = []
for label, value in hand_cases:
    if value not in seen:
        seen.add(value)
        cases.append((label, value))

# Deterministically cover both branches, ASCII case boundaries, and Unicode
# letters that either do or do not change under swapcase.
alphabet = ("a", "Z", "0", "#", "é", "ß", "中", "文", "Σ", "ς", "İ")
for length in range(5):
    for chars in itertools.product(alphabet, repeat=length):
        value = "".join(chars)
        if value not in seen:
            seen.add(value)
            cases.append((f"generated-len-{length}", value))

mismatches = []
canonical_letter_branch = 0
canonical_no_letter_branch = 0
for label, value in cases:
    expected = canonical(value)
    actual = candidate(value)
    if any(ch.isalpha() for ch in value):
        canonical_letter_branch += 1
    else:
        canonical_no_letter_branch += 1
    if expected != actual:
        mismatches.append((label, value, expected, actual))

print(f"total_cases={len(cases)}")
print(f"canonical_letter_branch={canonical_letter_branch}")
print(f"canonical_no_letter_branch={canonical_no_letter_branch}")
print(f"mismatch_count={len(mismatches)}")
for label, value, expected, actual in mismatches[:20]:
    print(
        "MISMATCH",
        f"label={label}",
        f"input={value!r}",
        f"canonical={expected!r}",
        f"candidate={actual!r}",
    )

# A differential is expected to expose any deviation; do not convert a
# mismatch into a script failure because the log itself is audit evidence.
raise SystemExit(0)
