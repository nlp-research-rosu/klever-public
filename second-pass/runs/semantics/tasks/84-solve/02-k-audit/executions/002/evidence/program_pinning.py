#!/usr/bin/env python3
"""Mechanical token-level comparison of solution.mpy and the spec's loaded Module."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_#][A-Za-z0-9_#-]*|-?[0-9]+|[(),.]')


def balanced_call(text: str, constructor: str, start: int = 0) -> str:
    marker = constructor + "("
    begin = text.index(marker, start)
    index = begin + len(constructor)
    depth = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[begin : index + 1]
        index += 1
    raise ValueError(f"unbalanced {constructor} call")


if len(sys.argv) != 3:
    raise SystemExit("usage: program_pinning.py SOLUTION_MPY SPEC_K")

solution_text = Path(sys.argv[1]).read_text()
spec_text = Path(sys.argv[2]).read_text()
solution_module = balanced_call(solution_text, "Module")
load_all_pos = spec_text.index("#loadAll")
spec_module = balanced_call(spec_text, "Module", load_all_pos)
solution_tokens = TOKEN.findall(solution_module)
spec_tokens = TOKEN.findall(spec_module)

print("solution_module_token_count:", len(solution_tokens))
print("spec_loaded_module_token_count:", len(spec_tokens))
print("constructor_tokens_identical:", solution_tokens == spec_tokens)
if solution_tokens != spec_tokens:
    for index, pair in enumerate(zip(solution_tokens, spec_tokens)):
        if pair[0] != pair[1]:
            print("first_difference:", index, pair)
            break
    print("lengths:", len(solution_tokens), len(spec_tokens))
    raise SystemExit(1)

call_tokens = TOKEN.findall('Call(Name("solve"), Int(N))')
k_prefix = spec_text[spec_text.index("<k>") : spec_text.index("=>", spec_text.index("<k>"))]
print("entry_call_present_after_load:", all(token in TOKEN.findall(k_prefix) for token in call_tokens))
if '~> Call(Name("solve"), Int(N))' not in " ".join(k_prefix.split()):
    raise SystemExit("spec does not execute solve(N) after loading the module")
