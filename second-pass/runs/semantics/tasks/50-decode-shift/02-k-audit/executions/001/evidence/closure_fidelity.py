#!/usr/bin/env python3
"""Mechanically compare the proof macro body with submitted solution.mpy."""

from __future__ import annotations

import re
from pathlib import Path

MPY = Path("/tmp/audit-work/50-decode-shift/candidate-src/solution.mpy")
VERIFICATION = Path(
    "/tmp/audit-work/50-decode-shift/candidate-src/verification.k"
)

TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|=>|[A-Za-z_#$][A-Za-z0-9_#$-]*|-?\d+|[(),.]'
)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def matching_close(stream: list[str], open_index: int) -> int:
    depth = 0
    for index in range(open_index, len(stream)):
        if stream[index] == "(":
            depth += 1
        elif stream[index] == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced token stream")


mpy_tokens = tokens(MPY.read_text(encoding="utf-8"))
needle = ["FuncDef", "(", '"decode_shift"', ","]
function_start = next(
    index
    for index in range(len(mpy_tokens) - len(needle))
    if mpy_tokens[index : index + len(needle)] == needle
)
function_end = matching_close(mpy_tokens, function_start + 1)
function = mpy_tokens[function_start : function_end + 1]

# FuncDef("decode_shift", Params("s"), BODY...)
params_start = function.index("Params")
params_open = params_start + 1
params_close = matching_close(function, params_open)
if function[params_close + 1] != ",":
    raise ValueError("unexpected FuncDef parameter separator")
body = function[params_close + 2 : -1]

verification_lines = VERIFICATION.read_text(encoding="utf-8").splitlines()


def rule_rhs(start_line: int, end_line: int) -> list[str]:
    # Human line numbers are inclusive and 1-based.
    block = "\n".join(verification_lines[start_line - 1 : end_line])
    stream = tokens(block)
    arrow = stream.index("=>")
    return stream[arrow + 1 :]


step = rule_rhs(33, 48)
macro_body = rule_rhs(51, 57)
expanded_body: list[str] = []
for token in macro_body:
    if token == "decodeStep":
        expanded_body.extend(step)
    else:
        expanded_body.append(token)

closure = rule_rhs(60, 61)
expected_closure = tokens(
    'closureVal(("s", .ParamNames), decodeBody, 0)'
)

print(f"submitted_decode_body_token_count={len(body)}")
print(f"expanded_macro_body_token_count={len(expanded_body)}")
print(f"body_token_identity={body == expanded_body}")
print(f"closure_shape_identity={closure == expected_closure}")
if body != expanded_body:
    for index, (left, right) in enumerate(zip(body, expanded_body)):
        if left != right:
            print(
                f"first_body_difference=index:{index} "
                f"submitted:{left!r} macro:{right!r}"
            )
            break
    print(f"submitted_tail={body[-20:]!r}")
    print(f"macro_tail={expanded_body[-20:]!r}")

if body != expanded_body or closure != expected_closure:
    raise SystemExit(1)
