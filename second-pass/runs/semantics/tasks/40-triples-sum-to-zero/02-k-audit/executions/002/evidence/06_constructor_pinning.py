#!/usr/bin/env python3
"""Mechanical token-level comparison of solution.mpy and the executed closure."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|(?:-?[0-9]+)|(?:[#.$A-Za-z_][#.$A-Za-z_0-9-]*)|[(),]'
)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def matching_close(items: list[str], open_index: int) -> int:
    depth = 0
    for index in range(open_index, len(items)):
        if items[index] == "(":
            depth += 1
        elif items[index] == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError("unbalanced constructor term")


solution = tokens((WORK / "solution.mpy").read_text())
verification = tokens((WORK / "verification.k").read_text())

assert solution[:4] == ["Module", "(", "FuncDef", "("]
func_close = matching_close(solution, 3)
assert func_close == len(solution) - 2
assert solution[-1] == ")"

# Split the FuncDef's three arguments at top-level commas. The third K-list
# argument is constructor adjacency, so it remains a token sequence.
depth = 0
commas: list[int] = []
for index in range(4, func_close):
    if solution[index] == "(":
        depth += 1
    elif solution[index] == ")":
        depth -= 1
    elif solution[index] == "," and depth == 0:
        commas.append(index)
assert len(commas) == 2, commas
name_tokens = solution[4 : commas[0]]
params_tokens = solution[commas[0] + 1 : commas[1]]
body_tokens = solution[commas[1] + 1 : func_close]

assert name_tokens == ['"triples_sum_to_zero"']
assert params_tokens == ["Params", "(", '"l"', ")"]

closure_index = verification.index("closureVal")
assert verification[closure_index + 1] == "("
closure_close = matching_close(verification, closure_index + 1)
actual_closure = verification[closure_index : closure_close + 1]

# Stmts and ParamNames are K list sorts. py2mpy uses list notation whose
# terminators are inserted by the parser; verification.k spells them
# explicitly. Remove only explicit .Stmts terminators before comparison.
actual_normalized = [item for item in actual_closure if item != ".Stmts"]
expected_normalized = [
    "closureVal",
    "(",
    '"l"',
    ",",
    ".ParamNames",
    ",",
    *body_tokens,
    ",",
    "0",
    ")",
]

print(f"solution_function_name={name_tokens[0]}")
print('solution_parameter="l"')
print("closure_definition_environment=0")
print(f"solution_body_token_count={len(body_tokens)}")
print(f"executed_closure_token_count={len(actual_normalized)}")
print(
    "solution_body_sha256="
    + hashlib.sha256("\0".join(body_tokens).encode()).hexdigest()
)
print(
    "expected_closure_sha256="
    + hashlib.sha256("\0".join(expected_normalized).encode()).hexdigest()
)
print(
    "actual_closure_sha256="
    + hashlib.sha256("\0".join(actual_normalized).encode()).hexdigest()
)
print(f"constructor_level_match={actual_normalized == expected_normalized}")
if actual_normalized != expected_normalized:
    for index, (expected, actual) in enumerate(
        zip(expected_normalized, actual_normalized)
    ):
        if expected != actual:
            print(f"first_difference={index} expected={expected} actual={actual}")
            break
    print(
        f"expected_length={len(expected_normalized)} "
        f"actual_length={len(actual_normalized)}"
    )
raise SystemExit(0 if actual_normalized == expected_normalized else 1)
