#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for flip_case."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_function(path: Path):
    spec = importlib.util.spec_from_file_location(f"review_{path.stem}_{id(path)}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


canonical = load_function(Path("/reference/canonical.py"))
candidate = load_function(Path("/tmp/audit-work/27-flip-case/solution.py"))

# Includes the documented example, empty input, every ASCII alphabetic boundary
# and its immediate neighbors, punctuation/whitespace/digits, and Unicode cases
# where Python's swapcase changes code points or string length.
fixed = [
    "Hello",
    "",
    "@AZ[",
    "`az{",
    "AaZz09 !\t\n",
    "\x00\x7f",
    "éÉ",
    "ß",
    "İı",
    "Σσς",
    "Жж",
    "你好🙂",
    "\ud800\udfff",
    "\U0010ffff",
]

rng = random.Random(270027)
alphabet = [
    "\x00",
    " ",
    "@",
    "A",
    "M",
    "Z",
    "[",
    "`",
    "a",
    "m",
    "z",
    "{",
    "0",
    "9",
    "é",
    "É",
    "ß",
    "İ",
    "ı",
    "Σ",
    "ς",
    "Ж",
    "ж",
    "你",
    "🙂",
    "\ud800",
    "\U0010ffff",
]
generated = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 33)))
    for _ in range(500)
]

if "--list-inputs" in sys.argv:
    for index, value in enumerate(fixed + generated):
        print(f"case[{index}]={value!r}")

mismatches = []
for index, value in enumerate(fixed + generated):
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append((index, value, expected, actual))

print(f"fixed_cases={len(fixed)}")
print(f"generated_cases={len(generated)} seed=270027 max_length=32")
print(f"total_cases={len(fixed) + len(generated)}")
print(f"mismatches={len(mismatches)}")
for index, value, expected, actual in mismatches[:20]:
    print(
        f"mismatch[{index}] input={value!r} "
        f"canonical={expected!r} candidate={actual!r}"
    )
sys.exit(1 if mismatches else 0)
