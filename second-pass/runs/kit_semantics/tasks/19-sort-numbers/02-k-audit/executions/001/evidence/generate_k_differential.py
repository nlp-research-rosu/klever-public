#!/usr/bin/env python3
"""Generate an independent MPY assertion corpus for the concrete keyed sort."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)
RANK = {word: index for index, word in enumerate(WORDS)}
SOLUTION = Path("/tmp/audit-work/19-sort-numbers/solution.py")
PROGRAM = Path("/tmp/audit-work/19-sort-numbers/k_differential.py")
INPUTS = Path("/audit-output/evidence/05-k-differential-inputs.json")
RESULTS = Path("/audit-output/evidence/05-k-differential-generation.json")


def expected(value: str) -> str:
    tokens = value.split()
    return " ".join(sorted(tokens, key=RANK.__getitem__))


def main() -> int:
    exhaustive = [
        " ".join(items)
        for length in range(3)
        for items in itertools.product(WORDS, repeat=length)
    ]
    spacing = []
    for value in exhaustive[:20]:
        spacing.extend([f"  {value}", f"{value}  ", value.replace(" ", "   ")])
    inputs = list(dict.fromkeys(exhaustive + spacing))
    INPUTS.write_text(json.dumps(inputs, indent=2) + "\n")

    assertions = [
        f"assert sort_numbers({value!r}) == {expected(value)!r}" for value in inputs
    ]
    PROGRAM.write_text(SOLUTION.read_text().rstrip() + "\n\n" + "\n".join(assertions) + "\n")
    result = {
        "oracle": "independent rank dictionary plus Python sorted",
        "scope": "all valid word sequences of lengths 0..2 plus 20 deterministic leading/trailing/repeated-space variants",
        "assertion_count": len(assertions),
        "program": str(PROGRAM),
    }
    RESULTS.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
