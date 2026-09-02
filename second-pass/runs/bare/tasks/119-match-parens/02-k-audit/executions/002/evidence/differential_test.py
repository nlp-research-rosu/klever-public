#!/usr/bin/env python3
"""Independent differential check: trusted HumanEval canonical vs candidate."""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/candidate/solution.py")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


canonical = load_function(CANONICAL_PATH, "trusted_canonical_119")
candidate = load_function(CANDIDATE_PATH, "candidate_solution_119")


def outcome(function, value):
    try:
        return ("return", function(value))
    except BaseException as error:  # The observable outcome includes exceptions.
        return ("raise", type(error).__name__, str(error))


named_cases = [
    ("prompt-yes", ["()(", ")"]),
    ("prompt-no", [")", ")"]),
    ("both-empty", ["", ""]),
    ("first-order-minimal", ["(", ")"]),
    ("second-order-minimal", [")", "("]),
    ("empty-right", ["()", ""]),
    ("empty-left", ["", "()"]),
    ("unclosed-positive", ["(", "("]),
    ("early-negative", [")(", ""]),
    ("second-order-only", ["())", "("]),
    ("nested", ["(((", ")))"]),
    ("disconnected-balanced", ["()()", ""]),
]

checked = 0
mismatches: list[tuple[str, list[str], tuple, tuple]] = []


def check(label: str, value: list[str]) -> None:
    global checked
    expected = outcome(canonical, value)
    observed = outcome(candidate, value)
    checked += 1
    if expected != observed:
        mismatches.append((label, value, expected, observed))


for label, value in named_cases:
    check(label, value)

# Every pair where each component has length at most six: 16,129 pairs.
small_strings = [
    "".join(bits)
    for length in range(7)
    for bits in itertools.product("()", repeat=length)
]
for left in small_strings:
    for right in small_strings:
        check("exhaustive-components-through-length-6", [left, right])

# Recursion-depth boundary probes.  These are in the stated input domain.
for total_length in (900, 950, 975, 990, 995, 996, 997, 998, 999, 1000, 1050, 1100):
    half = total_length // 2
    nested = "(" * half + ")" * half
    check(f"nested-total-{len(nested)}", [nested, ""])

print(f"python={sys.version.split()[0]}")
print(f"recursion_limit={sys.getrecursionlimit()}")
print(f"checked={checked}")
print(f"mismatch_count={len(mismatches)}")
for index, (label, value, expected, observed) in enumerate(mismatches[:30], 1):
    lengths = [len(item) for item in value]
    previews = [item[:24] + ("..." if len(item) > 24 else "") for item in value]
    print(
        f"MISMATCH {index}: label={label} lengths={lengths} "
        f"previews={previews!r} canonical={expected!r} candidate={observed!r}"
    )

raise SystemExit(1 if mismatches else 0)
