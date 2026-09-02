#!/usr/bin/env python3
"""Independent value-level differential test for HumanEval problem 5."""

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
    return module.intersperse


canonical = load_entry(
    Path("/tmp/audit-work/reconstruction/canonical.py"), "trusted_canonical"
)
generated = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "submitted_solution"
)

documented_and_boundary = [
    ([], 4),
    ([1, 2, 3], 4),
    ([7], 99),
    ([7, 8], 99),
    ([7, 8, 9], 99),
    ([0, 0], 0),
    ([-1, 2, -3, 4], -9),
    ([5, 6, 7, 8], 6),
]

checked = 0
mismatches = []
alias_differences = []
outcome_mismatches = []


def check(numbers, delimiter, label):
    global checked
    left_input = list(numbers)
    right_input = list(numbers)
    expected = canonical(left_input, delimiter)
    actual = generated(right_input, delimiter)
    checked += 1
    if expected != actual or left_input != numbers or right_input != numbers:
        mismatches.append(
            {
                "label": label,
                "numbers": numbers,
                "delimiter": delimiter,
                "canonical": expected,
                "generated": actual,
                "canonical_input_after": left_input,
                "generated_input_after": right_input,
            }
        )
    if (expected is left_input) != (actual is right_input):
        alias_differences.append(
            {
                "label": label,
                "numbers": numbers,
                "delimiter": delimiter,
                "canonical_aliases_input": expected is left_input,
                "generated_aliases_input": actual is right_input,
            }
        )


for index, (numbers, delimiter) in enumerate(documented_and_boundary):
    check(numbers, delimiter, f"explicit-{index}")

# Exhaustive small value space covers both branch boundaries and recursive depths.
for length in range(0, 7):
    for values in itertools.product((-2, 0, 3), repeat=length):
        for delimiter in (-5, 0, 3, 8):
            check(list(values), delimiter, f"exhaustive-length-{length}")

# Deterministic broader generated sample.
rng = random.Random(0x5EED)
for index in range(1000):
    length = rng.randrange(0, 41)
    numbers = [rng.randrange(-1000, 1001) for _ in range(length)]
    delimiter = rng.randrange(-1000, 1001)
    check(numbers, delimiter, f"random-{index}")


def summarized_outcome(function, numbers, delimiter):
    try:
        result = function(list(numbers), delimiter)
    except Exception as error:
        return ("exception", type(error).__name__)
    return (
        "return",
        len(result),
        result[:3],
        result[-3:],
    )


# The recursive rewrite has a CPython call-stack boundary that the iterative
# canonical implementation does not. This is an intended-domain outcome check,
# separate from normal-return value equality.
deep_outcomes = []
for length in (900, 1000, 1200):
    numbers = list(range(length))
    expected = summarized_outcome(canonical, numbers, -1)
    actual = summarized_outcome(generated, numbers, -1)
    entry = {
        "length": length,
        "canonical": expected,
        "generated": actual,
    }
    deep_outcomes.append(entry)
    if expected != actual:
        outcome_mismatches.append(entry)

print("documented_and_boundary_cases:")
for numbers, delimiter in documented_and_boundary:
    print(
        f"  numbers={numbers!r}, delimiter={delimiter!r}, "
        f"canonical={canonical(list(numbers), delimiter)!r}, "
        f"generated={generated(list(numbers), delimiter)!r}"
    )
print("exhaustive_domain: lengths=0..6, values={-2,0,3}, delimiters={-5,0,3,8}")
print("random_domain: seed=0x5EED, 1000 lists, lengths=0..40, ints=-1000..1000")
print(f"checked={checked}")
print(f"value_or_mutation_mismatches={len(mismatches)}")
print(f"return_identity_differences={len(alias_differences)}")
print(f"first_identity_differences={alias_differences[:4]!r}")
print(f"deep_recursion_outcomes={deep_outcomes!r}")
print(f"exception_or_return_outcome_mismatches={len(outcome_mismatches)}")
if mismatches:
    print(f"first_mismatches={mismatches[:10]!r}")
if mismatches or outcome_mismatches:
    raise SystemExit(1)
