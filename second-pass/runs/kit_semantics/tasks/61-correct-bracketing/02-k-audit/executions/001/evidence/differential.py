#!/usr/bin/env python3
"""Independent differential test for HumanEval/61.

Oracle 1 is the trusted canonical implementation. Oracle 2 is a direct stack
characterization written by the reviewer. The implementation under audit is
loaded from the scratch copy, never from candidate bytecode or caches.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SCRATCH = Path("/tmp/audit-work/fresh")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_entry("trusted_canonical", SCRATCH / "canonical.py")
generated = load_entry("generated_solution", SCRATCH / "solution.py")


def stack_oracle(brackets: str) -> bool:
    depth = 0
    for bracket in brackets:
        if bracket == "(":
            depth += 1
        else:
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


documented_and_boundaries = [
    "",
    "(",
    ")",
    "()",
    ")(",
    "((",
    "))",
    "(()())",
    ")(()",
    "()()",
    "((()))",
    "(()",
    "())",
    "())(",
]

cases: list[tuple[str, str]] = [
    ("documented/boundary", value) for value in documented_and_boundaries
]

# Exhaust every branch pattern through length 14 (32,767 strings total).
for length in range(15):
    for chars in itertools.product("()", repeat=length):
        cases.append(("exhaustive<=14", "".join(chars)))

# Add deterministic long shapes and generated inputs well beyond the exhaustive
# prefix. Lengths include odd/even boundaries and values around powers of two.
for length in [15, 16, 17, 31, 32, 33, 63, 64, 65, 127, 128, 129, 500, 1000]:
    cases.extend(
        [
            ("long-shape", "(" * length),
            ("long-shape", ")" * length),
            ("long-shape", "()" * length),
            ("long-shape", "(" * length + ")" * length),
            ("long-shape", ")" + "(" * length + ")" * max(length - 1, 0)),
        ]
    )

rng = random.Random(610061)
for _ in range(3000):
    length = rng.randrange(0, 1001)
    cases.append(
        ("random(seed=610061)", "".join(rng.choice("()") for _ in range(length)))
    )

mismatches: list[tuple[str, str, bool, bool, bool]] = []
counts: dict[str, int] = {}
for group, value in cases:
    expected = canonical(value)
    actual = generated(value)
    independent = stack_oracle(value)
    counts[group] = counts.get(group, 0) + 1
    if actual is not expected or actual is not independent:
        mismatches.append((group, value, actual, expected, independent))

print(f"counts={counts}")
print(f"total={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(repr(mismatch))
    raise SystemExit(1)
