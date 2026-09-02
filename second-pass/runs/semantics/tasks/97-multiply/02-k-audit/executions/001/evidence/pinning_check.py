#!/usr/bin/env python3
"""Mechanically compare the submitted MiniPython function with its proof closure."""

from __future__ import annotations

import re
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|=>|[A-Za-z_#][A-Za-z0-9_#-]*|-?[0-9]+|[(),]'
)


def tokens(path: str) -> list[str]:
    return TOKEN.findall(Path(path).read_text(encoding="utf-8"))


def close_paren(items: list[str], open_index: int) -> int:
    assert items[open_index] == "("
    depth = 0
    for index in range(open_index, len(items)):
        if items[index] == "(":
            depth += 1
        elif items[index] == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError(f"unclosed parenthesis at token {open_index}")


mpy = tokens("/tmp/audit-work/candidate-src/solution.mpy")
verification = tokens("/tmp/audit-work/candidate-src/verification.k")

# Require exactly Module(FuncDef("multiply", Params(...), BODY)).
assert mpy[:4] == ["Module", "(", "FuncDef", "("], mpy[:8]
func_close = close_paren(mpy, 3)
module_close = close_paren(mpy, 1)
assert func_close + 1 == module_close == len(mpy) - 1
assert mpy[4:6] == ['"multiply"', ","]
assert mpy[6:8] == ["Params", "("]
params_close = close_paren(mpy, 7)
assert mpy[params_close + 1] == ","
submitted_params = mpy[8:params_close]
submitted_body = mpy[params_close + 2 : func_close]

# Extract the unique closureVal(...) on multiplyClosure's RHS.
marker = ["rule", "multiplyClosure", "=>", "closureVal", "("]
starts = [
    index
    for index in range(len(verification) - len(marker) + 1)
    if verification[index : index + len(marker)] == marker
]
assert len(starts) == 1, starts
closure_open = starts[0] + len(marker) - 1
closure_close = close_paren(verification, closure_open)
closure = verification[closure_open + 1 : closure_close]

depth = 0
commas = []
for index, token in enumerate(closure):
    if token == "(":
        depth += 1
    elif token == ")":
        depth -= 1
    elif token == "," and depth == 0:
        commas.append(index)
assert len(commas) == 2, commas

closure_params = closure[: commas[0]]
closure_body = closure[commas[0] + 1 : commas[1]]
closure_env = closure[commas[1] + 1 :]
assert closure_params[0] == "(" and closure_params[-1] == ")"
assert closure_body[0] == "(" and closure_body[-1] == ")"

closure_params = closure_params[1:-1]
closure_body = closure_body[1:-1]

print(f"submitted_parameter_tokens={submitted_params}")
print(f"closure_parameter_tokens={closure_params}")
print(f"parameter_identity={submitted_params == closure_params}")
print(f"submitted_body_token_count={len(submitted_body)}")
print(f"closure_body_token_count={len(closure_body)}")
print(f"body_token_identity={submitted_body == closure_body}")
print(f"closure_environment_tokens={closure_env}")

assert submitted_params == closure_params
assert submitted_body == closure_body
assert closure_env == ["0"]
