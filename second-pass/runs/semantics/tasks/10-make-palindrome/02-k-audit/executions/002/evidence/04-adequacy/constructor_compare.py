#!/usr/bin/env python3
"""Constructor-level comparisons between the translation, closure, and claim."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


CANDIDATE = Path("/candidate")
TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|\.Stmts|\.ParamNames|'
    r'[A-Za-z_#][A-Za-z0-9_#-]*|-?[0-9]+|[(),]'
)


def tokens(text: str) -> list[str]:
    # K sort annotations are metadata, not constructor children.
    text = re.sub(r":[A-Z][A-Za-z0-9-]*", "", text)
    return TOKEN.findall(text)


def matching_close(stream: list[str], constructor_index: int) -> int:
    assert stream[constructor_index + 1] == "("
    depth = 0
    for index in range(constructor_index + 1, len(stream)):
        if stream[index] == "(":
            depth += 1
        elif stream[index] == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError("unterminated constructor")


def arguments(stream: list[str], constructor_index: int) -> list[list[str]]:
    end = matching_close(stream, constructor_index)
    depth = 0
    commas: list[int] = []
    for index in range(constructor_index + 1, end + 1):
        if stream[index] == "(":
            depth += 1
        elif stream[index] == ")":
            depth -= 1
        elif stream[index] == "," and depth == 1:
            commas.append(index)
    boundaries = [constructor_index + 2] + [index + 1 for index in commas]
    ends = commas + [end]
    return [stream[start:stop] for start, stop in zip(boundaries, ends)]


def digest(stream: list[str]) -> str:
    return hashlib.sha256("\x00".join(stream).encode()).hexdigest()


solution_text = (CANDIDATE / "solution.mpy").read_text()
verification_text = (CANDIDATE / "verification.k").read_text()
spec_text = (CANDIDATE / "spec.k").read_text()

solution = tokens(solution_text)
verification = tokens(verification_text)

function_index = next(
    index
    for index in range(len(solution) - 2)
    if solution[index] == "FuncDef"
    and solution[index + 2] == '"make_palindrome"'
)
function_args = arguments(solution, function_index)
assert function_args[0] == ['"make_palindrome"']
assert function_args[1] == ["Params", "(", '"string"', ")"]
translated_body = function_args[2]

rule_index = next(
    index
    for index in range(len(verification) - 1)
    if verification[index : index + 2]
    == ["rule", "makePalindromeClosure"]
)
closure_index = verification.index("closureVal", rule_index)
closure_args = arguments(verification, closure_index)
assert closure_args[0] == ["(", '"string"', ",", ".ParamNames", ")"]
assert closure_args[2] == ["0"]
literal_closure_body = [
    token for token in closure_args[1] if token != ".Stmts"
]
assert translated_body == literal_closure_body

# Split translated body into Assign, For, Return.
assign_index = 0
assert translated_body[assign_index] == "Assign"
assign_end = matching_close(translated_body, assign_index)
for_index = assign_end + 1
assert translated_body[for_index] == "For"
for_end = matching_close(translated_body, for_index)
return_index = for_end + 1
assert translated_body[return_index] == "Return"
return_end = matching_close(translated_body, return_index)
assert return_end == len(translated_body) - 1
for_args = arguments(translated_body, for_index)
translated_tail_return = translated_body[return_index : return_end + 1]

# Restrict tokenization to the submitted loop claim's source computation,
# before its reachability arrow.
loop_start = spec_text.index("#loop(")
loop_arrow = spec_text.index("=> str(palindromeFrom", loop_start)
loop_source = tokens(spec_text[loop_start:loop_arrow])
loop_index = loop_source.index("#loop")
loop_end = matching_close(loop_source, loop_index)
loop_args = arguments(loop_source, loop_index)
claim_tail_return_index = loop_end + 1
assert loop_source[claim_tail_return_index] == "Return"
claim_tail_return_end = matching_close(
    loop_source, claim_tail_return_index
)
claim_tail_return = loop_source[
    claim_tail_return_index : claim_tail_return_end + 1
]

expected_range_expr = tokens(
    'Call(Name("range"), Call(Name("len"), Name("string")))'
)
expected_range_obj = tokens("rangeObj(I, isLen(S), 1)")

assert for_args[0] == loop_args[1]
assert for_args[1] == expected_range_expr
assert loop_args[0] == expected_range_obj
assert [token for token in for_args[2] if token != ".Stmts"] == [
    token for token in loop_args[2] if token != ".Stmts"
]
assert translated_tail_return == claim_tail_return

k_cells = re.findall(r"<k>(.*?)</k>", spec_text, flags=re.DOTALL)
assert len(k_cells) == 2
assert all("makePalindromeClosure" not in cell for cell in k_cells)

print("translated_make_palindrome_body_equals_literal_closure_body=true")
print(f"normalized_body_token_sha256={digest(translated_body)}")
print("loop_target_equals_translated_for_target=true")
print("loop_body_equals_translated_for_body=true")
print("loop_tail_return_equals_translated_function_tail_return=true")
print("range_expression=Call(range, Call(len, string))")
print("claim_range_value=rangeObj(I, isLen(S), 1)")
print("makePalindromeClosure_occurs_in_any_k_cell=false")
print(
    "claim_starts_at=#loop; omitted_prefix="
    "function-call/binding,Assign(i,0),len/range evaluation,For elaboration"
)
