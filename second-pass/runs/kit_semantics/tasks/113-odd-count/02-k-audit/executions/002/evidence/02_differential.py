#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval 113."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load("audit_candidate_solution", "/candidate/solution.py")
canonical = load("audit_trusted_canonical", "/reference/canonical.py")

TEMPLATE = "the number of odd elements in the string i of the input."


def doc_oracle(values: list[str]) -> list[str]:
    outputs = []
    for value in values:
        count = sum(character in "13579" for character in value)
        outputs.append(TEMPLATE.replace("i", str(count)))
    return outputs


documented = [
    (
        ["1234567"],
        ["the number of odd elements 4n the str4ng 4 of the 4nput."],
    ),
    (
        ["3", "11111111"],
        [
            "the number of odd elements 1n the str1ng 1 of the 1nput.",
            "the number of odd elements 8n the str8ng 8 of the 8nput.",
        ],
    ),
]

boundary_lists = [
    [],
    [""],
    ["0"],
    ["1"],
    ["2"],
    ["9"],
    ["02468"],
    ["13579"],
    ["111111111"],
    ["1111111111"],
    ["11111111111"],
    ["0123456789"],
    ["9", "", "0", "1357902468"],
]

all_lists: list[list[str]] = [values for values, _ in documented]
all_lists.extend(boundary_lists)

# Exhaust every ASCII digit string through length 4 as singleton inputs.
for length in range(5):
    for characters in itertools.product("0123456789", repeat=length):
        all_lists.append(["".join(characters)])

# Deterministic broader inputs exercise list length, ordering, empty strings,
# and output counts well above one decimal digit.
rng = random.Random(0x113)
for _ in range(1000):
    values = []
    for _ in range(rng.randrange(0, 13)):
        length = rng.randrange(0, 251)
        values.append("".join(rng.choice("0123456789") for _ in range(length)))
    all_lists.append(values)

mismatches = []
for index, values in enumerate(all_lists):
    expected = doc_oracle(values)
    candidate_value = candidate.odd_count(values)
    canonical_value = canonical.odd_count(values)
    if candidate_value != expected or canonical_value != expected:
        mismatches.append((index, values, expected, candidate_value, canonical_value))

for values, expected in documented:
    assert candidate.odd_count(values) == expected
    assert canonical.odd_count(values) == expected

print(f"ASCII_CASES={len(all_lists)}")
print(f"ASCII_MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(f"ASCII_MISMATCH {mismatch!r}")

# The prompt does not specify Unicode numerals. Record the canonical/candidate
# behavior as an edge observation rather than silently folding it into ASCII.
unicode_observations = ["١", "٣", "１２３", "𝟙𝟚𝟛", "²"]
for text in unicode_observations:
    try:
        canonical_value = ("RETURN", canonical.odd_count([text]))
    except Exception as error:  # noqa: BLE001 - behavior inventory
        canonical_value = ("RAISE", type(error).__name__, str(error))
    try:
        candidate_value = ("RETURN", candidate.odd_count([text]))
    except Exception as error:  # noqa: BLE001 - behavior inventory
        candidate_value = ("RAISE", type(error).__name__, str(error))
    print(
        f"UNICODE_OBSERVATION input={text!r} "
        f"candidate={candidate_value!r} canonical={canonical_value!r}"
    )

raise SystemExit(0 if not mismatches else 1)
