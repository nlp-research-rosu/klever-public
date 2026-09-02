#!/usr/bin/env python3
"""Independent differential test for HumanEval/98.

Oracle: /reference/canonical.py, imported separately from the generated
candidate entry point.  The generated input space is deterministic.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_upper


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "generated_solution", Path("/tmp/audit-work/98-count-upper/solution.py")
)

documented = [
    "aBCdEf",
    "abcdefg",
    "dBBE",
]

# Empty, length boundaries, each membership branch, even/odd positions,
# non-ASCII characters, embedded NUL, and Unicode sequences.
boundaries = [
    "",
    "A",
    "E",
    "I",
    "O",
    "U",
    "B",
    "a",
    "AA",
    "BA",
    "AB",
    "A_",
    "_A",
    "AEI",
    "BAE",
    "AEIOU",
    "AaEeIiOoUu",
    "xAxExIxOxU",
    "\x00A\x00E",
    "🙂A🙂E",
    "ÁÉÍÓÚ",  # Uppercase, but not one of the five ASCII vowels in the contract.
    "A\u0301E\u0301",  # Combining marks occupy their own Python string indices.
    "𝔸A𝔼E",
]

# Exhaust every string through length 5 over symbols chosen to exercise
# membership true/false, case, ASCII/non-ASCII, and NUL.
alphabet = ("A", "E", "U", "a", "B", "🙂", "\x00")
exhaustive = (
    "".join(chars)
    for length in range(0, 6)
    for chars in itertools.product(alphabet, repeat=length)
)

# Deterministic representative longer inputs, including all five vowels and
# varied Unicode.  This is finite evidence, not a universal proof.
rng = random.Random(980026)
random_alphabet = list("AEIOUaeiouBCDFxyz012 !?") + [
    "\x00",
    "🙂",
    "Ω",
    "Á",
    "\u0301",
    "𝔸",
]
random_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 129)))
    for _ in range(5000)
]

checked = 0
mismatches: list[tuple[str, object, object]] = []
seen: set[str] = set()
for category, cases in [
    ("documented", documented),
    ("boundary", boundaries),
    ("exhaustive_short", exhaustive),
    ("deterministic_random", random_cases),
]:
    category_checked = 0
    for value in cases:
        if value in seen:
            continue
        seen.add(value)
        expected = canonical(value)
        actual = generated(value)
        checked += 1
        category_checked += 1
        if type(expected) is not int or type(actual) is not int or expected != actual:
            mismatches.append((value, expected, actual))
    print(f"{category}: checked={category_checked}")

print(f"total_unique_inputs={checked}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for value, expected, actual in mismatches[:20]:
        print(f"MISMATCH input={value!r} canonical={expected!r} generated={actual!r}")
    raise SystemExit(1)
print("RESULT: zero mismatches; both implementations returned int on every input")
