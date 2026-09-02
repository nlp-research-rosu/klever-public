#!/usr/bin/env python3
"""Independent canonical-vs-submitted-Python differential test.

The oracle and generated entry point are imported from distinct source files.
No K equations or candidate test vectors are reused as an oracle.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "submitted_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

curated = [
    "",
    "x",
    "xx",
    "xX",
    "xyzXYZ",
    "Jerry",
    "AaBb!",
    "@A[Z{a",
    "0123456789",
    " !\t\n",
    "Åå",
    "Éé",
    "İi\u0307",
    "Σσς",
    "ẞß",
    "StraßeSTRASSE",
    "𐐀𐐨",
    "😀😀A😀a",
    "e\u0301Éé",
    "\x00A\x00a",
]

# Exhaustive small strings straddle the ASCII lower-case rule boundaries and
# include non-ASCII case pairs. The source itself has no explicit branches.
alphabet = ["@", "A", "Z", "[", "a", "z", "Å", "å", "Σ", "σ", "ς", "ẞ", "ß"]
exhaustive = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(160016)
pool = alphabet + ["0", "9", "!", " ", "İ", "\u0307", "é", "É", "𐐀", "𐐨", "😀"]
random_cases = [
    "".join(rng.choice(pool) for _ in range(rng.randrange(0, 26)))
    for _ in range(2000)
]

cases = curated + exhaustive + random_cases
mismatches = []
for value in cases:
    expected = canonical(value)
    actual = generated(value)
    if actual != expected:
        mismatches.append((value, expected, actual))

print("oracle=/reference/canonical.py:count_distinct_characters")
print("subject=/tmp/audit-work/candidate-src/solution.py:count_distinct_characters")
print("curated_inputs=" + json.dumps(curated, ensure_ascii=True))
print(
    "generated_scope="
    + json.dumps(
        {
            "exhaustive_alphabet": alphabet,
            "exhaustive_lengths": [0, 1, 2, 3],
            "random_seed": 160016,
            "random_count": len(random_cases),
            "random_length_range": [0, 25],
        },
        ensure_ascii=True,
        sort_keys=True,
    )
)
print(f"case_count={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH " + repr(mismatch))

raise SystemExit(1 if mismatches else 0)
