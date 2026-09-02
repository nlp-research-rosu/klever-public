#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential audit."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


canonical = load_function("trusted_canonical", SCRATCH / "trusted/canonical.py")
generated = load_function("submitted_solution", SCRATCH / "candidate-src/solution.py")

documented = [
    "",
    "abcdef\nghijklm",
    "abcdef",
    "aaaaa",
    "aaBAA",
    "zbcd",
]

boundaries = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "A",
    "E",
    "I",
    "O",
    "U",
    "b",
    "\n",
    "aeiouAEIOU",
    "bacedifoguh",
    "UOIEAuoiea",
    "a" * 256,
    "b" * 256,
    "\x00a\x00U\x00",
    "éAßuİ🙂",
]

# Every string of lengths 0..3 over a small alphabet that exercises each
# deletion stage, preserved characters, a digit, and a line boundary.
small_alphabet = "aeiouAEIOUbc0\n"
exhaustive_small = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(small_alphabet, repeat=length)
]

# Deterministic broader samples from the full Unicode scalar/code-point range,
# including arbitrary Python strings with NULs and surrogate code points.
rng = random.Random(510051)
generated_inputs = []
for _ in range(2000):
    length = rng.randrange(0, 65)
    generated_inputs.append(
        "".join(chr(rng.randrange(0x110000)) for _ in range(length))
    )

all_inputs = documented + boundaries + exhaustive_small + generated_inputs
mismatches = []
for index, text in enumerate(all_inputs):
    expected = canonical(text)
    actual = generated(text)
    if actual != expected:
        mismatches.append((index, text, expected, actual))
        if len(mismatches) >= 20:
            break

# Exhaust every Python code point as a singleton. This directly checks whether
# canonical `lower()` classifies any non-ASCII character as one of the five
# ASCII vowels, including surrogate code points representable in Python str.
unicode_singleton_mismatches = []
for codepoint in range(0x110000):
    text = chr(codepoint)
    expected = canonical(text)
    actual = generated(text)
    if actual != expected:
        unicode_singleton_mismatches.append((codepoint, expected, actual))
        if len(unicode_singleton_mismatches) >= 20:
            break

print(f"documented={len(documented)}")
for text in documented:
    print(
        "example",
        repr(text),
        "canonical=",
        repr(canonical(text)),
        "generated=",
        repr(generated(text)),
    )
print(f"boundaries={len(boundaries)}")
for text in boundaries:
    print(
        "boundary",
        repr(text),
        "canonical=",
        repr(canonical(text)),
        "generated=",
        repr(generated(text)),
    )
print(
    f"exhaustive_small={len(exhaustive_small)} "
    f"alphabet={small_alphabet!r} lengths=0..3"
)
print(
    "generated=2000 seed=510051 lengths=0..64 "
    "codepoints=U+0000..U+10FFFF"
)
print(
    "unicode_singletons=1114112 codepoints=U+0000..U+10FFFF "
    f"mismatches={len(unicode_singleton_mismatches)}"
)
print(f"total={len(all_inputs)} mismatches={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", repr(mismatch))
for mismatch in unicode_singleton_mismatches:
    print("UNICODE_SINGLETON_MISMATCH", repr(mismatch))

raise SystemExit(1 if mismatches or unicode_singleton_mismatches else 0)
