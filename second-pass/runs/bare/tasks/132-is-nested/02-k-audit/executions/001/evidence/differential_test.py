#!/usr/bin/env python3
"""Independent differential test for HumanEval 132 on bracket-only strings."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


def contains_nested_subsequence(text: str) -> bool:
    """Independent contract oracle: does `[[]]` occur as a subsequence?"""
    target_index = 0
    target = "[[]]"
    for character in text:
        if character == target[target_index]:
            target_index += 1
            if target_index == len(target):
                return True
    return False


candidate = load_entry(
    Path("/tmp/audit-work/source/solution.py"), "audit_candidate_solution"
)
canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "audit_trusted_canonical"
)

documented_examples = {
    "[[]]": True,
    "[]]]]]]][[[[[]": False,
    "[][]": False,
    "[]": False,
    "[[][]]": True,
    "[[]][[": True,
}

# These cases exercise the empty input; every single-character boundary; the
# state-0/1/2/3 transitions; ignored characters in each state; an almost-match;
# exact first acceptance; and acceptance with leading/trailing noise.
branch_and_boundary_cases = [
    "",
    "[",
    "]",
    "[[",
    "[]",
    "][",
    "]]",
    "][[",
    "[[[",
    "[[]",
    "[][]",
    "[[]]",
    "][[]]",
    "[[[]]",
    "[[]][",
    "[[]]]",
    "]]][[[",
    "]]][[[]]]][[",
]

inputs: list[tuple[str, str]] = []
inputs.extend(("documented", text) for text in documented_examples)
inputs.extend(("branch-boundary", text) for text in branch_and_boundary_cases)
for length in range(15):
    inputs.extend(
        ("exhaustive-0-to-14", "".join(chars))
        for chars in itertools.product("[]", repeat=length)
    )

rng = random.Random(132)
for length in (15, 16, 31, 32, 63, 64, 127, 128, 255):
    for _ in range(250):
        inputs.append(
            ("seeded-long", "".join(rng.choice("[]") for _ in range(length)))
        )

mismatches = []
for category, text in inputs:
    expected = contains_nested_subsequence(text)
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    documented = documented_examples.get(text, expected)
    if not (
        documented == expected == canonical_result == candidate_result
    ):
        mismatches.append(
            {
                "category": category,
                "input": text,
                "documented": documented,
                "oracle": expected,
                "canonical": canonical_result,
                "candidate": candidate_result,
            }
        )

print("ORACLE: explicit linear subsequence scan for target '[[]]'")
print(f"DOCUMENTED_EXAMPLES: {len(documented_examples)}")
print(f"BRANCH_BOUNDARY_CASES: {len(branch_and_boundary_cases)}")
print("EXHAUSTIVE_SCOPE: every bracket string of lengths 0 through 14")
print("SEEDED_LONG_SCOPE: 250 strings at each of 9 listed lengths; seed=132")
print(f"TOTAL_COMPARISONS: {len(inputs)}")
print(f"MISMATCHES: {len(mismatches)}")
for mismatch in mismatches[:20]:
    print(mismatch)

raise SystemExit(1 if mismatches else 0)
