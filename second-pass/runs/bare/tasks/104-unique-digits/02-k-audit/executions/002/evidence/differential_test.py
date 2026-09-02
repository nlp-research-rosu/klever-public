#!/usr/bin/env python3
"""Independent differential checks for HumanEval/104."""

from __future__ import annotations

import hashlib
import importlib.util
import random
from pathlib import Path
import sys
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/104-unique-digits-audit-002/source/solution.py")


def load_function(module_name: str, path: Path) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


canonical = load_function("trusted_canonical_104", CANONICAL_PATH)
candidate = load_function("candidate_solution_104", CANDIDATE_PATH)


def invoke(function: Callable[[list[int]], list[int]], values: list[int]) -> tuple[str, object]:
    try:
        return ("value", function(values))
    except BaseException as error:  # An exception is observable disagreement.
        return ("exception", (type(error).__name__, str(error)))


def describe(values: list[int]) -> str:
    digit_lengths = [len(str(value)) for value in values]
    sample = values if max(digit_lengths, default=0) <= 50 else []
    digest = hashlib.sha256(",".join(map(str, values)).encode()).hexdigest()[:16]
    return f"len={len(values)} digit_lengths={digit_lengths} sample={sample} sha256[:16]={digest}"


def describe_result(result: tuple[str, object]) -> str:
    kind, payload = result
    if kind == "value":
        assert isinstance(payload, list)
        return f"value:({describe(payload)})"
    return f"exception:{payload}"


named_cases: list[tuple[str, list[int]]] = [
    ("prompt-example-1", [15, 33, 1422, 1]),
    ("prompt-example-2", [152, 323, 1422, 10]),
    ("empty-list", []),
    ("smallest-positive-odd", [1]),
    ("smallest-positive-even", [2]),
    ("one-digit-boundaries", [1, 2, 7, 8, 9]),
    ("decimal-carry-boundary", [9, 10, 11, 12, 19, 20, 21]),
    ("entry-precondition-witness", [15, 2]),
    ("even-digit-positions", [2111, 1211, 1121, 1112, 1111]),
    ("duplicates-and-order", [97531, 7, 111, 97531, 3, 7]),
    ("mixed-digit-lengths", [1, 31, 531, 7531, 97531, 2468, 22221]),
]

# These remain within CPython's default 4,300-digit int-to-string limit.
# The all-odd inputs force every recursive helper call.
for digits in [900, 950, 975, 990, 995, 999, 1000, 1001, 1100]:
    named_cases.append((f"all-odd-{digits}-digits", [int("1" * digits)]))

rng = random.Random(104)
generated_cases: list[list[int]] = []
for _ in range(300):
    length = rng.randrange(0, 21)
    generated_cases.append([rng.randrange(1, 10**18) for _ in range(length)])
for value in range(1, 2001):
    generated_cases.append([value])

mismatches: list[tuple[str, list[int], tuple[str, object], tuple[str, object]]] = []
for name, values in named_cases:
    trusted = invoke(canonical, values)
    generated = invoke(candidate, values)
    status = "MATCH" if trusted == generated else "MISMATCH"
    print(f"{status} named={name} input=({describe(values)})")
    if name == "entry-precondition-witness":
        print(f"  canonical={describe_result(trusted)}")
        print(f"  candidate={describe_result(generated)}")
    if trusted != generated:
        print(f"  canonical={describe_result(trusted)}")
        print(f"  candidate={describe_result(generated)}")
        mismatches.append((name, values, trusted, generated))

generated_mismatches = 0
for index, values in enumerate(generated_cases):
    trusted = invoke(canonical, values)
    generated = invoke(candidate, values)
    if trusted != generated:
        generated_mismatches += 1
        if generated_mismatches <= 10:
            print(f"MISMATCH generated={index} input=({describe(values)})")
            print(f"  canonical={describe_result(trusted)}")
            print(f"  candidate={describe_result(generated)}")

print(f"named_cases={len(named_cases)} named_mismatches={len(mismatches)}")
print(f"generated_cases={len(generated_cases)} generated_mismatches={generated_mismatches}")
print(f"python_recursion_limit={sys.getrecursionlimit()}")
print(f"TOTAL_MISMATCHES={len(mismatches) + generated_mismatches}")
sys.exit(1 if mismatches or generated_mismatches else 0)
