#!/usr/bin/env python3
"""Ground instances of the formal postcondition compared with both Python functions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encode


def map_swap(codes: list[int]) -> list[int]:
    result = []
    for code in codes:
        if 65 <= code <= 90:
            result.append(code + 32)
        elif 97 <= code <= 122:
            result.append(code - 32)
        else:
            result.append(code)
    return result


def replace_code(codes: list[int], old: int, new: int) -> list[int]:
    return [new if code == old else code for code in codes]


def formal_postcondition(message: str) -> str:
    codes = map_swap([ord(character) for character in message])
    for old, new in [
        (97, 99),
        (101, 103),
        (105, 107),
        (111, 113),
        (117, 119),
        (65, 67),
        (69, 71),
        (73, 75),
        (79, 81),
        (85, 87),
    ]:
        codes = replace_code(codes, old, new)
    return "".join(chr(code) for code in codes)


candidate = load_function("ground_candidate", Path("/candidate/solution.py"))
canonical = load_function("ground_canonical", Path("/reference/canonical.py"))

for message in ["", "a", "u", "U", "b", "test", "This is a message", "aeiouAEIOU"]:
    formal = formal_postcondition(message)
    candidate_result = candidate(message)
    canonical_result = canonical(message)
    assert formal == candidate_result == canonical_result
    print(
        f"input={message!r} CS={[ord(character) for character in message]} "
        f"formal={formal!r} candidate={candidate_result!r} canonical={canonical_result!r}"
    )

u_codes = map_swap([ord("u")])
for old, new in [
    (97, 99),
    (101, 103),
    (105, 107),
    (111, 113),
    (117, 119),
    (65, 67),
    (69, 71),
    (73, 75),
    (79, 81),
    (85, 88),  # independent false mutation
]:
    u_codes = replace_code(u_codes, old, new)
mutated_u = "".join(chr(code) for code in u_codes)
assert mutated_u == "X"
assert mutated_u != candidate("u")
print(f"false_mutation_witness input='u' correct={candidate('u')!r} mutated={mutated_u!r}")

print("GROUND_WITNESSES=PASS")
