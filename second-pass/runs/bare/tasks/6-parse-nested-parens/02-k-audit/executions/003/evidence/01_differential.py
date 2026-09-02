#!/usr/bin/env python3
"""Independent differential checks: trusted canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens


canonical = load_entry(
    Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical"
)
generated = load_entry(
    Path("/tmp/audit-work/candidate/solution.py"), "submitted_solution"
)


def dyck_words(pairs: int) -> list[str]:
    result: list[str] = []

    def visit(prefix: str, opened: int, closed: int) -> None:
        if opened == pairs and closed == pairs:
            result.append(prefix)
            return
        if opened < pairs:
            visit(prefix + "(", opened + 1, closed)
        if closed < opened:
            visit(prefix + ")", opened, closed + 1)

    visit("", 0, 0)
    return result


fixed_inputs = [
    "(()()) ((())) () ((())()())",  # documented example
    "()",
    "(())",
    "()()",
    "(()())",
    "(()(())((())))",
    "() (()) ((())) (((())))",
    "",  # no groups
    " ",  # two empty split fields
    "  ",  # three empty split fields
    " ()",  # leading separator
    "() ",  # trailing separator
    "()  (())",  # repeated separator
    "  ()   (())  ",  # multiple leading/interior/trailing separators
]

print("FIXED CASES")
fixed_mismatches: list[tuple[str, list[int], list[int]]] = []
for value in fixed_inputs:
    expected = canonical(value)
    actual = generated(value)
    match = expected == actual
    print(
        f"input={value!r} canonical={expected!r} submitted={actual!r} "
        f"match={match}"
    )
    if not match:
        fixed_mismatches.append((value, expected, actual))

pool = list(itertools.chain.from_iterable(dyck_words(n) for n in range(1, 6)))
assert len(pool) == 64
rng = random.Random(0x6A11D)
generated_inputs: list[str] = []
for _ in range(300):
    group_count = rng.randint(1, 8)
    groups = [rng.choice(pool) for _ in range(group_count)]
    generated_inputs.append(" ".join(groups))

generated_mismatches = [
    (value, canonical(value), generated(value))
    for value in generated_inputs
    if canonical(value) != generated(value)
]
print("GENERATED SINGLE-SEPARATOR CASES")
print(
    "seed=0x6A11D dyck_pairs=1..5 "
    f"dyck_pool={len(pool)} cases={len(generated_inputs)} "
    f"mismatches={len(generated_mismatches)}"
)
for value, expected, actual in generated_mismatches[:20]:
    print(f"MISMATCH input={value!r} canonical={expected!r} submitted={actual!r}")

print(
    f"SUMMARY fixed_cases={len(fixed_inputs)} "
    f"fixed_mismatches={len(fixed_mismatches)} "
    f"generated_cases={len(generated_inputs)} "
    f"generated_mismatches={len(generated_mismatches)}"
)
if fixed_mismatches or generated_mismatches:
    print("DIFFERENTIAL_RESULT=MISMATCH")
    raise SystemExit(1)
print("DIFFERENTIAL_RESULT=MATCH")
