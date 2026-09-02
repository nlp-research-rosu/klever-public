#!/usr/bin/env python3
"""Mechanical constructor-level claim/program and ground-obligation checks."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def extract_balanced(text: str, marker: str) -> list[str]:
    results: list[str] = []
    search_from = 0
    while True:
        start = text.find(marker, search_from)
        if start < 0:
            return results
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
            else:
                if char == '"':
                    in_string = True
                elif char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth == 0:
                        results.append(text[start : index + 1])
                        search_from = index + 1
                        break
        else:
            raise ValueError(f"unbalanced occurrence of {marker!r}")


def normalize_constructor(term: str) -> str:
    # `.Stmts` is the explicit spelling of the associative Stmts unit. The
    # trusted translator renders the same empty sequence as an omitted slot.
    without_space = re.sub(r"\s+", "", term)
    return without_space.replace(".Stmts", "")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


def rounded_int(n: int, m: int) -> int:
    return round(Fraction(n + m, 2))


def bit_value(digits: str) -> int:
    result = 0
    weight = 1
    for character in reversed(digits):
        result += (ord(character) - 48) * weight
        weight *= 2
    return result


failures: list[str] = []
solution_text = (ROOT / "solution.mpy").read_text()
spec_text = (ROOT / "spec.k").read_text()
verification_text = (ROOT / "verification.k").read_text()
connection_text = (ROOT / "connection-spec.k").read_text()

solution_functions = extract_balanced(solution_text, "FuncDef(")
spec_functions = extract_balanced(spec_text, "FuncDef(")
print(f"solution_funcdef_count={len(solution_functions)}")
print(f"spec_funcdef_count={len(spec_functions)}")
if len(solution_functions) != 1 or len(spec_functions) != 2:
    failures.append("unexpected number of FuncDef terms")
else:
    solution_norm = normalize_constructor(solution_functions[0])
    solution_digest = hashlib.sha256(solution_norm.encode()).hexdigest()
    print(f"normalized_solution_funcdef_sha256={solution_digest}")
    for index, function in enumerate(spec_functions, 1):
        function_norm = normalize_constructor(function)
        function_digest = hashlib.sha256(function_norm.encode()).hexdigest()
        same = function_norm == solution_norm
        print(
            f"spec_funcdef_{index}_sha256={function_digest} "
            f"constructor_equal={same}"
        )
        if not same:
            failures.append(f"spec FuncDef {index} differs from solution.mpy")

solution_whiles = extract_balanced(solution_text, "While(")
bridge_whiles = extract_balanced(verification_text, "#while(")
connection_whiles = extract_balanced(connection_text, "#while(")
print(
    f"while_counts solution={len(solution_whiles)} bridge={len(bridge_whiles)} "
    f"connection={len(connection_whiles)}"
)
if not (len(solution_whiles) == len(bridge_whiles) == len(connection_whiles) == 1):
    failures.append("unexpected number of loop terms")
else:
    lowered_solution = "#while(" + solution_whiles[0][len("While(") :]
    lowered_norm = normalize_constructor(lowered_solution)
    bridge_norm = normalize_constructor(bridge_whiles[0])
    connection_norm = normalize_constructor(connection_whiles[0])
    print(f"solution_lowered_bridge_equal={lowered_norm == bridge_norm}")
    print(f"bridge_connection_loop_equal={bridge_norm == connection_norm}")
    if lowered_norm != bridge_norm:
        failures.append("operational bridge loop differs from lowered real-program loop")
    if bridge_norm != connection_norm:
        failures.append("connection theorem loop differs from operational bridge loop")

generated = load_function(ROOT / "solution.py", "pinning_generated")
canonical = load_function(Path("/reference/canonical.py"), "pinning_canonical")
ground_cases = [
    ("invalid witness", 2, 1),
    ("valid zero-loop witness", 1, 1),
    ("valid tie-down witness", 2, 3),
    ("valid tie-up witness", 3, 4),
    ("valid prompt witness", 20, 33),
]
for label, n, m in ground_cases:
    generated_value = generated(n, m)
    canonical_value = canonical(n, m)
    if n > m:
        post_holds = generated_value == -1
        claim_detail = "post=-1"
    else:
        expected_integer = rounded_int(n, m)
        expected_string = bin(expected_integer)
        digits = expected_string[2:]
        predicate = (
            bit_value(digits) == expected_integer
            and all(character in "01" for character in digits)
            and digits.startswith("1")
        )
        post_holds = generated_value == expected_string and predicate
        claim_detail = (
            f"roundedInt={expected_integer} digits={digits} "
            f"bitValue={bit_value(digits)} allBits/startsOne={predicate}"
        )
    print(
        f"{label}: N={n} M={m} generated={generated_value!r} "
        f"canonical={canonical_value!r} {claim_detail} post_holds={post_holds}"
    )
    if not post_holds:
        failures.append(f"ground claimed postcondition failed: {label}")

print("invalid_precondition_witness=N=2,M=1 satisfies N>0,M>0,N>M")
print("valid_precondition_witness=N=1,M=1 satisfies N>0,M>0,N<=M")
print(f"FAILURE_COUNT={len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
sys.exit(1 if failures else 0)
