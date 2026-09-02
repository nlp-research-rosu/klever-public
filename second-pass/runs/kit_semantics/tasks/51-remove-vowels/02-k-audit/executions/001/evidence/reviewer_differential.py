#!/usr/bin/env python3
"""Independent differential test for HumanEval 51-remove-vowels."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(
    Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_generated"
)

documented = [
    "",
    "abcdef\nghijklm",
    "abcdef",
    "aaaaa",
    "aaBAA",
    "zbcd",
]

# Empty, singleton outcomes for every branch, and code points around each ASCII
# vowel boundary. Unicode cases exercise Python's character iteration/lowercase
# behavior, including a lowercase mapping that expands to two code points.
boundaries = [
    "",
    *list("aeiouAEIOU"),
    *list("`abdehijnoptuvz@ABDEHIJNOP TUVZ".replace(" ", "")),
    "a",
    "b",
    "A",
    "B",
    "\x00",
    "\n",
    "\U0010ffff",
    "éΩ中🙂",
    "İıſKÅ",
    "bAeiOUz",
    "A\nB\tE",
]

alphabet = "aAeEiIoOuUbZ0 \nİéΩ中🙂"
exhaustive = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(5100729)
random_alphabet = (
    "\x00\x7f"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789 \n\t"
    "éΩ中🙂İıſKÅ"
)
generated_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 129)))
    for _ in range(2000)
]

cases = documented + boundaries + exhaustive + generated_cases
mismatches = []
for text in cases:
    expected = canonical(text)
    actual = generated(text)
    if expected != actual:
        mismatches.append(
            {"input": text, "canonical": expected, "generated": actual}
        )

# Python strings are sequences of Unicode code points. Exhaust every singleton
# value, including the surrogate code points Python permits in an in-memory str.
unicode_singleton_mismatches = []
for codepoint in range(sys.maxunicode + 1):
    text = chr(codepoint)
    expected = canonical(text)
    actual = generated(text)
    if expected != actual:
        unicode_singleton_mismatches.append(
            {
                "codepoint": codepoint,
                "input": text,
                "canonical": expected,
                "generated": actual,
            }
        )

result = {
    "documented": len(documented),
    "boundaries": len(boundaries),
    "exhaustive": len(exhaustive),
    "generated": len(generated_cases),
    "total": len(cases),
    "mismatches": len(mismatches),
    "first_mismatches": mismatches[:10],
    "unicode_singletons": sys.maxunicode + 1,
    "unicode_singleton_mismatches": len(unicode_singleton_mismatches),
    "first_unicode_singleton_mismatches": unicode_singleton_mismatches[:10],
}
print(json.dumps(result, ensure_ascii=True, sort_keys=True))
if mismatches or unicode_singleton_mismatches:
    raise SystemExit(1)
