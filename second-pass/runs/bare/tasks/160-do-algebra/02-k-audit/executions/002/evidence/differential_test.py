#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/160-do-algebra")
OPS = ("+", "-", "*", "//", "**")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


canonical = load_entry(ROOT / "reference/canonical.py", "trusted_canonical")
candidate = load_entry(ROOT / "candidate/solution.py", "candidate_solution")


def outcome(function, operators, operands):
    try:
        value = function(list(operators), list(operands))
        return ("return", type(value).__name__, value)
    except Exception as error:  # exception behavior is part of the comparison
        return ("raise", type(error).__name__)


explicit_cases = [
    (("+", "*", "-"), (2, 3, 4, 5)),  # documented example
    (("+",), (0, 0)),                  # minimum shape and zero boundary
    (("-",), (0, 1)),                  # negative result from nonnegative inputs
    (("*",), (0, 99)),
    (("//",), (7, 3)),
    (("//",), (1, 0)),                 # expected ZeroDivisionError
    (("**",), (0, 0)),                 # Python's 0 ** 0 boundary
    (("**",), (2, 0)),
    (("**", "**"), (2, 3, 2)),         # right associativity
    (("//", "//"), (20, 3, 2)),        # left associativity
    (("+", "*"), (2, 3, 4)),           # precedence boundary
    (("*", "+"), (2, 3, 4)),
    (("-", "+", "*"), (8, 1, 2, 3)),
    (tuple("+" for _ in range(32)), tuple(range(33))),  # longer loop
]

cases = list(explicit_cases)

# Exhaust all operator/operand tuples at useful small bounds without creating
# infeasible exponent towers.
for operator_count, operand_values in ((1, range(5)), (2, range(5)), (3, range(3))):
    for operators in itertools.product(OPS, repeat=operator_count):
        for operands in itertools.product(operand_values, repeat=operator_count + 1):
            cases.append((operators, operands))

# Seeded longer generated cases avoid exponent towers while covering many loop
# iterations, intermediate negatives, zeros, and division exceptions.
rng = random.Random(160)
for _ in range(500):
    operator_count = rng.randint(3, 10)
    operators = tuple(rng.choice(OPS[:-1]) for _ in range(operator_count))
    operands = tuple(rng.randint(0, 20) for _ in range(operator_count + 1))
    cases.append((operators, operands))

mismatches = []
return_count = 0
raise_count = 0
for operators, operands in cases:
    expected = outcome(canonical, operators, operands)
    actual = outcome(candidate, operators, operands)
    if expected[0] == "return":
        return_count += 1
    else:
        raise_count += 1
    if actual != expected:
        mismatches.append((operators, operands, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"explicit_cases={len(explicit_cases)}")
print("exhaustive_scope=operator lengths 1,2 over operands 0..4; length 3 over operands 0..2")
print("generated_scope=500 seeded cases, lengths 3..10, operators +,-,*,//, operands 0..20")
print(f"total_cases={len(cases)}")
print(f"returns={return_count}")
print(f"raises={raise_count}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", mismatch)

if mismatches:
    raise SystemExit(1)
