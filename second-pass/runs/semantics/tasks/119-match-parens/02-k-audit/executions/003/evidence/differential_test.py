#!/usr/bin/env python3
"""Independent differential test for HumanEval 119 on its documented domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/119-match-parens/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_119")
generated = load_entry(GENERATED_PATH, "generated_solution_119")

targeted = [
    (["()(", ")"], "Yes", "documented example; first order balances"),
    ([")", ")"], "No", "documented example; neither order balances"),
    (["", ""], "Yes", "empty boundary"),
    (["(", ")"], "Yes", "first order only"),
    ([")", "("], "Yes", "second order only"),
    (["(", "("], "No", "positive final balance"),
    (["()", ""], "Yes", "balanced left with empty right"),
    (["", "()"], "Yes", "empty left with balanced right"),
    (["())", "("], "Yes", "second order repairs an early-negative first order"),
    (["(()", ")"], "Yes", "first order balances"),
    (["(()", "("], "No", "both end positive"),
    ([")))", "((("], "Yes", "second order balances at a branch boundary"),
]

mismatches: list[tuple[list[str], str, str]] = []
target_failures: list[tuple[list[str], str, str]] = []
tested = 0

print("TARGETED_CASES")
for value, expected, reason in targeted:
    can = canonical(value)
    got = generated(value)
    tested += 1
    print(f"{value!r}: canonical={can!r} generated={got!r} expected={expected!r} ({reason})")
    if can != got:
        mismatches.append((value, can, got))
    if can != expected or got != expected:
        target_failures.append((value, expected, f"canonical={can!r}, generated={got!r}"))

# Exhaust every pair whose component lengths are 0..6.  This covers all
# branch boundaries for both possible concatenation orders and all 16,129
# ordered pairs from the 127 possible component strings.
short_strings = [
    "".join(chars)
    for length in range(7)
    for chars in itertools.product("()", repeat=length)
]
for left in short_strings:
    for right in short_strings:
        value = [left, right]
        can = canonical(value)
        got = generated(value)
        tested += 1
        if can != got:
            mismatches.append((value, can, got))

# Deterministic broader coverage, including much longer strings.
rng = random.Random(119)
for _ in range(5000):
    left_len = rng.randrange(0, 257)
    right_len = rng.randrange(0, 257)
    left = "".join(rng.choice("()") for _ in range(left_len))
    right = "".join(rng.choice("()") for _ in range(right_len))
    value = [left, right]
    can = canonical(value)
    got = generated(value)
    tested += 1
    if can != got:
        mismatches.append((value, can, got))

print(
    "SCOPE: 12 targeted cases; exhaustive ordered pairs for component "
    "lengths 0..6 (16,129 pairs); 5,000 seeded pairs with each length 0..256"
)
print(f"TOTAL_INVOCATIONS={tested}")
print(f"TARGET_FAILURES={len(target_failures)}")
print(f"MISMATCHES={len(mismatches)}")
for item in target_failures[:10]:
    print(f"TARGET_FAILURE {item!r}")
for item in mismatches[:10]:
    print(f"MISMATCH {item!r}")

raise SystemExit(0 if not mismatches and not target_failures else 1)
