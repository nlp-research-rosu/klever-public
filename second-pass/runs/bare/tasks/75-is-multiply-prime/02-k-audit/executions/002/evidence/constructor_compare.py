#!/usr/bin/env python3
"""Mechanical token-level comparison of solution.mpy with solutionProgram RHS."""

from __future__ import annotations

import re
from pathlib import Path


def constructor_tokens(text: str) -> list[str]:
    return re.findall(r'"(?:[^"\\]|\\.)*"|-?\d+|[A-Za-z][A-Za-z0-9_-]*|[(),]', text)


mpy = Path("/candidate/solution.mpy").read_text()
program_k = Path("/candidate/solution-program.k").read_text()
match = re.search(r"\brule\s+solutionProgram\s*=>\s*(Module\s*\(.*\))\s*endmodule", program_k, re.S)
if match is None:
    raise RuntimeError("could not extract solutionProgram RHS")

mpy_tokens = constructor_tokens(mpy)
rhs_tokens = constructor_tokens(match.group(1))
print("solution_mpy_token_count", len(mpy_tokens))
print("solutionProgram_rhs_token_count", len(rhs_tokens))
print("constructor_tokens_identical", mpy_tokens == rhs_tokens)
if mpy_tokens != rhs_tokens:
    for index, pair in enumerate(zip(mpy_tokens, rhs_tokens)):
        if pair[0] != pair[1]:
            print("first_difference", index, pair)
            break
    print("lengths", len(mpy_tokens), len(rhs_tokens))
raise SystemExit(0 if mpy_tokens == rhs_tokens else 1)
