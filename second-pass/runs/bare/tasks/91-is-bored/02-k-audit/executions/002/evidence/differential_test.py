#!/usr/bin/env python3
"""Independent differential test of candidate solution.py vs canonical.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


canonical = load_function(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
candidate = load_function(
    "submitted_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)

documented_and_boundary = [
    "Hello world",
    "The sky is blue. The sun is shining. I love this weather",
    "",
    ".",
    "?",
    "!",
    "I ",
    "I",
    "I.",
    "I?",
    "I!",
    "It starts",
    "Island",
    " I lead",
    "\tI tab-lead",
    "\nI newline-lead",
    "X.I yes",
    "X. I yes",
    "X?\tI yes",
    "X!\nI yes",
    "... ! ?  . I count!",
    "I am bored. I am still bored! Are you? I think so.",
    " I am here?You are there!  I agree",
    "It is cold. Island life! In time? I agree",
    "\tI tabbed.\nI newline?\rNot me!",
    "I first! No. I second?",
    "\u2003I unicode-leading",
    "X!\u2003I unicode-after-delimiter",
    "X.!? I after-cluster",
]

# Exhaust all short strings over characters that cross the "I " and delimiter
# branch boundaries. The separate random sample adds ordinary letters, all
# supported delimiters, Python whitespace classes, and non-ASCII characters.
exhaustive = (
    "".join(chars)
    for length in range(0, 7)
    for chars in itertools.product("I .?!", repeat=length)
)

rng = random.Random(910091)
alphabet = (
    "I iIslandxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    " .?!\t\n\r\f\v"
    "\u001c\u0085\u00a0\u2003\u2028\u202f\u3000"
    "é🙂"
)
random_cases = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 81)))
    for _ in range(20_000)
]

all_cases = itertools.chain(documented_and_boundary, exhaustive, random_cases)
mismatches: list[tuple[str, int, int]] = []
count = 0
for text in all_cases:
    count += 1
    expected = canonical(text)
    actual = candidate(text)
    if expected != actual:
        mismatches.append((text, expected, actual))

print(f"cases={count}")
print(f"mismatches={len(mismatches)}")
for text, expected, actual in mismatches[:25]:
    print(
        f"MISMATCH input={text!r} canonical={expected!r} candidate={actual!r}"
    )

focused = " I am here?You are there!  I agree"
print(
    "submitted_claim_4_witness="
    f"{focused!r} canonical={canonical(focused)} candidate={candidate(focused)}"
)

raise SystemExit(1 if mismatches else 0)
