#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/160."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path, module_name: str) -> Callable[[list[str], list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


def outcome(function: Callable[..., Any], operators: list[str], operands: list[int]) -> tuple[str, Any]:
    try:
        return ("value", function(list(operators), list(operands)))
    except BaseException as error:  # Compare observable exceptional outcomes too.
        return ("exception", type(error).__name__)


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical_160")
candidate = load_function(
    Path("/tmp/audit-work/160-do-algebra/solution.py"), "candidate_solution_160"
)

print("COMMAND: python3 /audit-output/evidence/02_differential.py")
documented_and_boundary = [
    ("documented-example", ["+", "*", "-"], [2, 3, 4, 5]),
    ("minimum-plus", ["+"], [0, 0]),
    ("minimum-minus", ["-"], [0, 7]),
    ("minimum-multiply", ["*"], [0, 999]),
    ("minimum-floor", ["//"], [7, 3]),
    ("minimum-power", ["**"], [2, 0]),
    ("precedence-mul", ["+", "*"], [2, 3, 4]),
    ("precedence-floor", ["-", "//"], [20, 7, 3]),
    ("right-assoc-power", ["**", "**"], [2, 3, 2]),
    ("zero-divisor", ["//"], [5, 0]),
    ("nested-zero-divisor", ["//", "-"], [5, 0, 0]),
    ("large-nonnegative", ["+", "*"], [10**30, 2, 10**20]),
]

valid_mismatches: list[tuple[Any, ...]] = []
valid_checked = 0
for label, operators, operands in documented_and_boundary:
    expected = outcome(canonical, operators, operands)
    actual = outcome(candidate, operators, operands)
    print(label, operators, operands, "canonical=", expected, "candidate=", actual)
    valid_checked += 1
    if actual != expected:
        valid_mismatches.append((label, operators, operands, expected, actual))

# Exhaust every one-operator branch over small operands.
for operator, left, right in itertools.product(
    ["+", "-", "*", "//", "**"], range(5), range(5)
):
    operators = [operator]
    operands = [left, right]
    expected = outcome(canonical, operators, operands)
    actual = outcome(candidate, operators, operands)
    valid_checked += 1
    if actual != expected:
        valid_mismatches.append(("exhaustive-one-op", operators, operands, expected, actual))

# Seeded representative inputs over the unbounded-shape contract (sampled lengths 1..3).
rng = random.Random(0x160A11)
operator_alphabet = ["+", "-", "*", "//", "**"]
generated = 0
while generated < 1200:
    operator_count = rng.randint(1, 4)
    operators = [rng.choice(operator_alphabet) for _ in range(operator_count)]
    # Avoid resource-unbounded right-associated exponent towers in the test
    # harness. A dedicated finite right-associativity boundary appears above.
    if any(left == right == "**" for left, right in zip(operators, operators[1:])):
        continue
    operands = [rng.randint(0, 5) for _ in range(operator_count + 1)]
    expected = outcome(canonical, operators, operands)
    actual = outcome(candidate, operators, operands)
    valid_checked += 1
    if actual != expected:
        valid_mismatches.append(
            (f"generated-{generated}", operators, operands, expected, actual)
        )
    generated += 1

# Empty/malformed cases are explicitly inspected but are outside the stated domain.
invalid_cases = [
    ("both-empty", [], []),
    ("no-operator-single-operand", [], [7]),
    ("operator-with-too-few-operands", ["+"], [2]),
    ("too-many-operands", ["+"], [2, 3, 4]),
]
for label, operators, operands in invalid_cases:
    print(
        "outside-domain",
        label,
        "canonical=",
        outcome(canonical, operators, operands),
        "candidate=",
        outcome(candidate, operators, operands),
    )

print(f"valid_checked={valid_checked} valid_mismatches={len(valid_mismatches)}")
if valid_mismatches:
    for mismatch in valid_mismatches[:20]:
        print("MISMATCH", mismatch)
    raise SystemExit(1)
print("RESULT: PASS")
