#!/usr/bin/env python3
"""Independent differential checks of trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

from itertools import product
import importlib.util
from pathlib import Path
import random
from typing import Any, Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/160-do-algebra/solution.py")
OPS = ("+", "-", "*", "//", "**")


def load_entry(path: Path, module_name: str) -> Callable[[list[str], list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_160")
generated = load_entry(GENERATED_PATH, "generated_solution_160")


def outcome(fn: Callable[..., Any], operators: list[str], operands: list[int]) -> tuple[str, Any]:
    try:
        return ("value", fn(list(operators), list(operands)))
    except Exception as error:  # Comparing observable exception classes is intentional.
        return ("exception", type(error).__name__)


checked = 0
mismatches: list[tuple[list[str], list[int], tuple[str, Any], tuple[str, Any]]] = []


def check(operators: list[str], operands: list[int], label: str) -> None:
    global checked
    trusted = outcome(canonical, operators, operands)
    actual = outcome(generated, operators, operands)
    checked += 1
    if trusted != actual:
        mismatches.append((operators, operands, trusted, actual))
        print(
            f"MISMATCH label={label} operators={operators!r} operands={operands!r} "
            f"canonical={trusted!r} generated={actual!r}"
        )


# Documented example plus explicit precedence/associativity and branch witnesses.
named_cases = [
    (["+", "*", "-"], [2, 3, 4, 5], "documented example"),
    (["-"], [0, 0], "level-0 subtraction at zero"),
    (["-"], [20, 6], "level-0 subtraction"),
    (["-", "-"], [20, 6, 2], "left-associated subtraction"),
    (["+"], [0, 0], "level-0 addition at zero"),
    (["*"], [0, 9], "level-1 multiplication by zero"),
    (["//"], [20, 6], "level-1 floor division"),
    (["//", "//"], [20, 6, 2], "left-associated floor division"),
    (["//"], [1, 0], "floor division by zero"),
    (["**"], [0, 0], "zero to zero"),
    (["**"], [2, 0], "zero exponent"),
    (["**", "**"], [2, 3, 2], "right-associated exponentiation"),
    (["+", "*"], [2, 3, 4], "multiplication precedence"),
    (["*", "**"], [2, 3, 2], "exponentiation precedence"),
    (["//", "**"], [100, 3, 2], "floor/exponent precedence"),
    (["**", "//"], [2, 5, 3], "exponent/floor precedence"),
]
for operators, operands, label in named_cases:
    check(operators, operands, label)

# Empty/singleton and malformed boundary observations. Only the first two extend
# below the documented minimum size; mismatched lengths are explicitly out of contract.
outside_contract_cases = [
    ([], [], "empty operands"),
    ([], [7], "singleton expression"),
    (["+"], [7], "too many operators"),
    ([], [7, 8], "too many operands"),
]
for operators, operands, label in outside_contract_cases:
    check(operators, operands, f"outside-contract: {label}")

# Exhaustive intended-domain sample. For three operators use operands 0..2:
# the otherwise-included expression 3 ** (3 ** (3 ** 3)) cannot be
# materialized, while all 5^3 operator triples and every small branch remain.
exhaustive_count = 0
for operator_count in (1, 2, 3):
    operand_values = range(4) if operator_count <= 2 else range(3)
    for operators in product(OPS, repeat=operator_count):
        for operands in product(operand_values, repeat=operator_count + 1):
            check(list(operators), list(operands), f"exhaustive-{operator_count}")
            exhaustive_count += 1

# Deterministic broader sample. Cap consecutive exponentiation operators at two
# and lengths at six. This is deliberately bounded after an earlier, preserved
# stress run with a three-exponent cap was killed by the container (exit 137).
random_source = random.Random(160_20260726)
random_count = 0
for _ in range(1000):
    operator_count = random_source.randint(1, 6)
    operators: list[str] = []
    exponent_run = 0
    for _position in range(operator_count):
        choices = OPS if exponent_run < 2 else OPS[:-1]
        operator = random_source.choice(choices)
        operators.append(operator)
        exponent_run = exponent_run + 1 if operator == "**" else 0
    operands = [random_source.randint(0, 2) for _ in range(operator_count + 1)]
    check(operators, operands, "deterministic-random")
    random_count += 1

print(f"canonical={CANONICAL_PATH}")
print(f"generated={GENERATED_PATH}")
print(f"named_cases={len(named_cases)}")
print(f"outside_contract_cases={len(outside_contract_cases)}")
print(f"exhaustive_intended_cases={exhaustive_count}")
print(f"deterministic_random_cases={random_count}")
print(f"total_cases={checked}")
print(f"mismatch_count={len(mismatches)}")

# There is one expected mismatch for a deliberately malformed, out-of-contract
# length pair: canonical zip truncates, while the candidate indexes by operator length.
intended_mismatches = [
    item for item in mismatches if len(item[0]) == len(item[1]) - 1 and len(item[0]) >= 1
]
print(f"intended_domain_mismatch_count={len(intended_mismatches)}")
if intended_mismatches:
    raise SystemExit(1)
