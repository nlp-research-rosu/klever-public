#!/usr/bin/env python3
"""Independent differential test for HumanEval/6 over the intended domain."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


WORK = Path("/tmp/audit-work/6-parse-nested-parens")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens


canonical = load_entry("trusted_canonical", WORK / "canonical.py")
generated = load_entry("generated_solution", WORK / "solution.py")


def balanced_groups(pair_count: int) -> list[str]:
    result: list[str] = []

    def visit(prefix: str, opened: int, closed: int) -> None:
        if opened == pair_count and closed == pair_count:
            result.append(prefix)
            return
        if opened < pair_count:
            visit(prefix + "(", opened + 1, closed)
        if closed < opened:
            visit(prefix + ")", opened, closed + 1)

    visit("", 0, 0)
    return result


def contract_oracle(text: str) -> list[int]:
    depths: list[int] = []
    for group in (group for group in text.split(" ") if group):
        depth = 0
        maximum = 0
        for character in group:
            if character == "(":
                depth += 1
                maximum = max(maximum, depth)
            elif character == ")":
                depth -= 1
            else:
                raise AssertionError(f"out-of-domain character: {character!r}")
            if depth < 0:
                raise AssertionError(f"negative prefix depth: {group!r}")
        if depth != 0:
            raise AssertionError(f"unbalanced group: {group!r}")
        depths.append(maximum)
    return depths


documented_and_boundaries = {
    "": [],
    " ": [],
    "   ": [],
    "()": [1],
    "(())": [2],
    "()()": [1],
    "(()())": [2],
    "((()))": [3],
    "  ()": [1],
    "()  ": [1],
    "  ()   (())  ": [1, 2],
    "(()()) ((())) () ((())()())": [2, 3, 1, 3],
}

for text, expected in documented_and_boundaries.items():
    oracle_value = contract_oracle(text)
    assert oracle_value == expected, (text, oracle_value, expected)

groups = [
    group
    for pair_count in range(1, 7)
    for group in balanced_groups(pair_count)
]
cases = set(documented_and_boundaries)

# Single-group cases cover leading/trailing/multiple delimiters and both final
# branches. Every balanced group through six pairs is included.
for group in groups:
    cases.update(
        {
            group,
            " " + group,
            group + " ",
            "  " + group + "   ",
        }
    )

# Every pair of the generated groups is tested with each separator boundary.
for left, right in itertools.product(groups, repeat=2):
    cases.add(left + " " + right)
    cases.add(left + "  " + right)
    cases.add(left + "   " + right)

# Representative three-group inputs add another delimiter transition.
sample = groups[:30]
for left, middle, right in itertools.product(sample, repeat=3):
    cases.add(left + " " + middle + "  " + right)

encoded_corpus = json.dumps(sorted(cases), ensure_ascii=True).encode()
mismatches: list[tuple[str, list[int], list[int], list[int]]] = []
for case in sorted(cases):
    expected = contract_oracle(case)
    canonical_value = canonical(case)
    generated_value = generated(case)
    if canonical_value != expected or generated_value != expected:
        mismatches.append((case, canonical_value, generated_value, expected))

print(f"documented_boundary_cases={len(documented_and_boundaries)}")
print(f"balanced_groups_pairs_1_through_6={len(groups)}")
print(f"total_unique_cases={len(cases)}")
print(f"corpus_sha256={hashlib.sha256(encoded_corpus).hexdigest()}")
print(f"mismatches={len(mismatches)}")
for text, expected in documented_and_boundaries.items():
    print(
        "boundary "
        f"input={text!r} canonical={canonical(text)!r} "
        f"generated={generated(text)!r} expected={expected!r}"
    )
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
