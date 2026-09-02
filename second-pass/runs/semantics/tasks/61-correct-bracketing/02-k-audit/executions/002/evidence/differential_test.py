#!/usr/bin/env python3
"""Independent source-level differential test for HumanEval/61."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/proof")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_function("candidate_solution", SCRATCH / "solution.py")

documented_and_boundary = [
    "(",
    "()",
    "(()())",
    ")(()",
    "",
    ")",
    "((",
    "())",
    "()()",
    "((()))",
    "(()",
    "())(",
    ")(",
    "((())())",
    "(" * 64 + ")" * 64,
    "()" * 128,
    ")" + "(" * 256,
    "(" * 256,
]

tests: list[str] = list(documented_and_boundary)
for length in range(13):
    tests.extend("".join(chars) for chars in itertools.product("()", repeat=length))

rng = random.Random(61061)
for _ in range(1000):
    length = rng.randrange(0, 513)
    tests.append("".join(rng.choice("()") for _ in range(length)))

tests.extend(["(" * 5000 + ")" * 5000, "()" * 5000, ")" * 10000])

digest = hashlib.sha256()
mismatches: list[tuple[str, bool, bool]] = []
true_count = 0
false_count = 0
prefix_negative_count = 0
positive_final_count = 0
for brackets in tests:
    assert set(brackets) <= {"(", ")"}
    expected = canonical(brackets)
    actual = candidate(brackets)
    digest.update(len(brackets).to_bytes(8, "big"))
    digest.update(brackets.encode("ascii"))
    digest.update(bytes([expected]))
    if expected:
        true_count += 1
    else:
        false_count += 1
    balance = 0
    went_negative = False
    for char in brackets:
        balance += 1 if char == "(" else -1
        went_negative |= balance < 0
    prefix_negative_count += int(went_negative)
    positive_final_count += int(not went_negative and balance > 0)
    if actual != expected:
        mismatches.append((brackets, expected, actual))

print("documented_and_boundary_results:")
for brackets in documented_and_boundary:
    print(f"  {brackets!r}: canonical={canonical(brackets)} candidate={candidate(brackets)}")
print(f"input_construction=18 explicit + all binary-parenthesis strings of lengths 0..12 + 1000 seeded random strings of lengths 0..512 + 3 length-10000 cases")
print(f"total_cases={len(tests)}")
print(f"ordered_case_result_sha256={digest.hexdigest()}")
print(f"true_results={true_count}")
print(f"false_results={false_count}")
print(f"prefix_negative_cases={prefix_negative_count}")
print(f"nonnegative_prefix_positive_final_cases={positive_final_count}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
print("SUMMARY: candidate and trusted canonical agree on all intended-domain test cases")
