#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_entry("trusted_canonical", "/reference/canonical.py")
generated = load_entry(
    "scratch_generated", "/tmp/audit-work/candidate-src/solution.py"
)

documented = ["(", "()", "(()())", ")(()"]
boundaries = [
    "",
    ")",
    "((",
    "))",
    ")(",
    "()(",
    "())",
    "(()",
    "((()))",
    "()()",
    "((())())",
    "(((((((((())))))))))",
    "(" * 64,
    ")" * 64,
    "()" * 64,
    "(" * 64 + ")" * 64,
    ")" + "(" * 128 + ")" * 128,
]

exhaustive = [
    "".join(bits)
    for length in range(13)
    for bits in itertools.product("()", repeat=length)
]

rng = random.Random(610061)
generated_inputs = [
    "".join(rng.choice("()") for _ in range(rng.randrange(0, 257)))
    for _ in range(2000)
]

ordered_cases: list[tuple[str, str]] = []
seen: set[str] = set()
for category, cases in [
    ("documented", documented),
    ("boundary", boundaries),
    ("exhaustive_len_0_through_12", exhaustive),
    ("seeded_random_len_0_through_256", generated_inputs),
]:
    for case in cases:
        if case not in seen:
            seen.add(case)
            ordered_cases.append((category, case))

mismatches = []
category_counts: dict[str, int] = {}
true_count = 0
false_count = 0
for category, case in ordered_cases:
    category_counts[category] = category_counts.get(category, 0) + 1
    expected = canonical(case)
    actual = generated(case)
    if actual:
        true_count += 1
    else:
        false_count += 1
    if actual != expected:
        mismatches.append(
            {
                "category": category,
                "input": case,
                "canonical": expected,
                "generated": actual,
            }
        )

summary = {
    "domain": "strings over {'(', ')'}",
    "canonical": "/reference/canonical.py:correct_bracketing",
    "generated": "/tmp/audit-work/candidate-src/solution.py:correct_bracketing",
    "random_seed": 610061,
    "unique_cases": len(ordered_cases),
    "category_first_occurrence_counts": category_counts,
    "true_results": true_count,
    "false_results": false_count,
    "mismatch_count": len(mismatches),
    "mismatches": mismatches[:20],
    "documented_results": [
        {
            "input": case,
            "canonical": canonical(case),
            "generated": generated(case),
        }
        for case in documented
    ],
    "selected_boundary_results": [
        {
            "input": case,
            "canonical": canonical(case),
            "generated": generated(case),
        }
        for case in boundaries
    ],
}
print(json.dumps(summary, indent=2))
raise SystemExit(1 if mismatches else 0)
