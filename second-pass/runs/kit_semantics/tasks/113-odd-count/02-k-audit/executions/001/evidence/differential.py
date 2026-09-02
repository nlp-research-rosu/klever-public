#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential for HumanEval/113."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


root = Path("/tmp/audit-work/rebuild")
canonical = load_function(root / "canonical.py", "trusted_canonical_113")
candidate = load_function(root / "solution.py", "candidate_solution_113")

# Documented examples, empty/outer-loop constructor boundaries, every ASCII
# digit class, zero/one/multi-digit odd counts, mixed lists, and a long input.
cases: list[list[str]] = [
    ["1234567"],
    ["3", "11111111"],
    [],
    [""],
    ["0"],
    ["1"],
    ["02468"],
    ["13579"],
    ["0123456789"],
    ["1" * 10],
    ["1" * 101 + "2" * 99],
    ["", "0", "1", "2468", "13579", "1234567890"],
]

# Exhaust all ASCII decimal strings through length four as singleton lists.
for length in range(5):
    cases.extend(
        ["".join(chars)]
        for chars in itertools.product("0123456789", repeat=length)
    )

# Deterministic broader generated ASCII lists and lengths.
rng = random.Random(11320260730)
for _ in range(500):
    list_length = rng.randrange(0, 12)
    cases.append(
        [
            "".join(
                rng.choice("0123456789")
                for _ in range(rng.randrange(0, 161))
            )
            for _ in range(list_length)
        ]
    )

# Canonical-representable CPython decimal digits outside ASCII.  These witness
# the source-domain boundary: int(character) succeeds for every character.
unicode_cases = [
    ["٣"],               # ARABIC-INDIC DIGIT THREE
    ["１２３"],           # FULLWIDTH DIGITS ONE TWO THREE
    ["०१२३४५६७८९"],      # DEVANAGARI DIGITS ZERO THROUGH NINE
    ["1٣5"],             # mixed ASCII and Arabic-Indic
]
for case in unicode_cases:
    for text in case:
        for character in text:
            int(character)
    cases.append(case)

mismatches: list[tuple[list[str], list[str], list[str]]] = []
ascii_mismatches = 0
unicode_mismatches = 0
unicode_start = len(cases) - len(unicode_cases)

for index, input_value in enumerate(cases):
    expected = canonical(input_value)
    actual = candidate(input_value)
    if actual != expected:
        mismatches.append((input_value, expected, actual))
        if index >= unicode_start:
            unicode_mismatches += 1
        else:
            ascii_mismatches += 1

print(
    "DIFFERENTIAL_SUMMARY "
    f"cases={len(cases)} ascii_cases={unicode_start} "
    f"unicode_cases={len(unicode_cases)} mismatches={len(mismatches)} "
    f"ascii_mismatches={ascii_mismatches} "
    f"unicode_mismatches={unicode_mismatches}"
)
for input_value, expected, actual in mismatches:
    print(f"MISMATCH input={input_value!r}")
    print(f"  canonical={expected!r}")
    print(f"  candidate={actual!r}")

sys.exit(1 if mismatches else 0)
