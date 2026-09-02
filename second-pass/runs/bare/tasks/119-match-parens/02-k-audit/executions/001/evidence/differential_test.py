#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs staged candidate."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/119-match-parens-audit")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


canonical = load_entry("audit_reference_canonical", WORK / "reference_canonical.py")
candidate = load_entry("audit_candidate_solution", WORK / "solution.py")

hand_cases = [
    ("prompt-example-yes", ["()(", ")"]),
    ("prompt-example-no", [")", ")"]),
    ("both-empty/base-depth-zero", ["", ""]),
    ("first-order-only/left-paren-branch", ["(", ")"]),
    ("second-order-only/right-paren-fallthrough", [")", "("]),
    ("neither-order/open-depth-nonzero", ["(", "("]),
    ("early-negative-depth", ["))", "(("]),
    ("balanced-plus-empty", ["(())()", ""]),
    ("prefix-safe-but-unbalanced", ["((()", ")"]),
    ("long-boundary", ["(" * 40, ")" * 40]),
    (
        "cpython-recursion-boundary",
        ["(" * 600, ")" * 600],
    ),
]

mismatches = []
checked = 0


def outcome(function, value: list[str]):
    try:
        return ("return", function(value))
    except Exception as error:
        return ("exception", type(error).__name__)


def check(tag: str, value: list[str]) -> None:
    global checked
    expected = outcome(canonical, value)
    actual = outcome(candidate, value)
    checked += 1
    if expected != actual:
        mismatches.append((tag, [len(item) for item in value], expected, actual))


print("HAND_CASES:")
for case_tag, case_input in hand_cases:
    expected_value = outcome(canonical, case_input)
    actual_value = outcome(candidate, case_input)
    print(
        f"  {case_tag}: lengths={[len(item) for item in case_input]!r} "
        f"input={case_input!r} "
        f"canonical={expected_value!r} candidate={actual_value!r}"
    )
    check(case_tag, case_input)

strings = [
    "".join(chars)
    for length in range(7)
    for chars in itertools.product("()", repeat=length)
]
for first in strings:
    for second in strings:
        check("exhaustive-length-0-through-6", [first, second])

rng = random.Random(119)
for index in range(1000):
    first = "".join(rng.choice("()") for _ in range(rng.randrange(0, 81)))
    second = "".join(rng.choice("()") for _ in range(rng.randrange(0, 81)))
    check(f"seeded-random-{index}", [first, second])

print(f"EXHAUSTIVE_STRING_COUNT: {len(strings)}")
print(f"EXHAUSTIVE_PAIR_COUNT: {len(strings) ** 2}")
print(f"CPYTHON_RECURSION_LIMIT: {sys.getrecursionlimit()}")
print("RANDOM_SEED: 119")
print("RANDOM_PAIR_COUNT: 1000")
print(f"TOTAL_CHECKS: {checked}")
print(f"MISMATCH_COUNT: {len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH: {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
