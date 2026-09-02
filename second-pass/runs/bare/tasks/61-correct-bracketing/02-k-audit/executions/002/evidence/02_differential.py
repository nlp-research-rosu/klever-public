#!/usr/bin/env python3
"""Independent differential test for HumanEval/61.

The oracle and candidate are loaded from separate, explicit paths.  The test
space is the prompt's full alphabet: strings over '(' and ')'.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/61-correct-bracketing-audit")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_entry(ROOT / "reference" / "canonical.py", "trusted_canonical")
generated = load_entry(ROOT / "candidate" / "solution.py", "generated_solution")

documented_and_boundaries = [
    "",
    "(",
    ")",
    "()",
    "((",
    "))",
    ")(",
    "()()",
    "(())",
    "(()())",
    ")(()",
    "((()))",
    "(()",
    "())",
    "((())())",
    "()(()())",
]

cases: list[tuple[str, str]] = [
    ("boundary", value) for value in documented_and_boundaries
]

# Exhaust every prompt-domain string through length 12 (8,191 cases).
for length in range(13):
    for chars in itertools.product("()", repeat=length):
        cases.append(("exhaustive-0..12", "".join(chars)))

# Seeded representative longer strings, plus explicit long/bad-prefix cases.
rng = random.Random(610061)
for _ in range(1_000):
    length = rng.randrange(13, 257)
    cases.append(("seeded-random-13..256", "".join(rng.choice("()") for _ in range(length))))
cases.extend(
    [
        ("long", "(" * 1_000 + ")" * 1_000),
        ("long", ")" + "(" * 1_000 + ")" * 999),
        ("long", "()" * 1_000),
        ("long", "(" * 2_000),
    ]
)

mismatches = []
for category, value in cases:
    expected = canonical(value)
    actual = generated(value)
    if actual != expected:
        mismatches.append(
            {
                "category": category,
                "input": value,
                "canonical": expected,
                "generated": actual,
            }
        )

summary = {
    "alphabet": ["(", ")"],
    "documented_and_boundary_count": len(documented_and_boundaries),
    "exhaustive_lengths": [0, 12],
    "seed": 610061,
    "seeded_random_count": 1_000,
    "seeded_random_lengths": [13, 256],
    "long_case_lengths": [2_000, 2_000, 2_000, 2_000],
    "total_comparisons": len(cases),
    "mismatch_count": len(mismatches),
    "boundary_results": [
        {
            "input": value,
            "canonical": canonical(value),
            "generated": generated(value),
        }
        for value in documented_and_boundaries
    ],
    "first_mismatches": mismatches[:10],
}
print(json.dumps(summary, indent=2))
raise SystemExit(1 if mismatches else 0)
