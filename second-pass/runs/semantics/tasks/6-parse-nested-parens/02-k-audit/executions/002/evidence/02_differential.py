#!/usr/bin/env python3
"""Independent differential test for HumanEval/6.

The intended-valid bucket consists of one or more nonempty balanced parenthesis
groups separated by exactly one ASCII space. Boundary/ambiguous inputs are
reported separately and never hidden.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated", Path("/tmp/audit-work/reconstruction/solution.py")
)


def balanced_groups(pairs: int) -> list[str]:
    result: list[str] = []

    def visit(prefix: str, opens: int, closes: int) -> None:
        if opens == pairs and closes == pairs:
            result.append(prefix)
            return
        if opens < pairs:
            visit(prefix + "(", opens + 1, closes)
        if closes < opens:
            visit(prefix + ")", opens, closes + 1)

    visit("", 0, 0)
    return result


documented = ["(()()) ((())) () ((())()())"]
branch_boundaries = [
    "()",
    "(())",
    "()()",
    "(()())",
    "((()))",
    "() ()",
    "(()) () (()())",
]

all_groups = [g for pairs in range(1, 7) for g in balanced_groups(pairs)]
intended_valid = list(dict.fromkeys(documented + branch_boundaries + all_groups))

# Exhaustive pairs drawn from all groups through 4 pairs.
small_groups = [g for pairs in range(1, 5) for g in balanced_groups(pairs)]
intended_valid.extend(f"{left} {right}" for left in small_groups for right in small_groups)

# Deterministic representative multi-group inputs at larger sizes.
rng = random.Random(6006)
for _ in range(500):
    group_count = rng.randint(1, 8)
    groups = [rng.choice(all_groups) for _ in range(group_count)]
    intended_valid.append(" ".join(groups))
intended_valid = list(dict.fromkeys(intended_valid))

boundary_or_ambiguous = [
    "",
    " ",
    "  ",
    "() ",
    " ()",
    "()  ()",
    "()   (())",
    "(",
    ")",
    "(()",
    "())",
    ")(",
    "( )",
]


def run_bucket(name: str, cases: list[str]) -> list[dict[str, object]]:
    mismatches: list[dict[str, object]] = []
    digest = hashlib.sha256()
    for text in cases:
        expected = canonical(text)
        actual = generated(text)
        digest.update(
            json.dumps(
                [text, expected, actual],
                ensure_ascii=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
        digest.update(b"\n")
        if actual != expected:
            mismatches.append(
                {"input": text, "canonical": expected, "generated": actual}
            )
    print(
        f"{name}: cases={len(cases)} mismatches={len(mismatches)} "
        f"result_sha256={digest.hexdigest()}"
    )
    for mismatch in mismatches:
        print(f"{name}_MISMATCH={json.dumps(mismatch, sort_keys=True)}")
    return mismatches


doc_mismatches = run_bucket("documented", documented)
valid_mismatches = run_bucket("intended_valid", intended_valid)
boundary_mismatches = run_bucket("boundary_or_ambiguous", boundary_or_ambiguous)

print("boundary_inputs=" + json.dumps(boundary_or_ambiguous))
print(f"boundary_mismatch_count={len(boundary_mismatches)}")
assert not doc_mismatches
assert not valid_mismatches
print("DIFFERENTIAL_VALID_DOMAIN=PASS")
