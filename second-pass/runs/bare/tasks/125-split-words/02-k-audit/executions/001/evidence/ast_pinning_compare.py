#!/usr/bin/env python3
"""Token-compare regenerated solution.mpy with verification.k's solutionAST.

Inside a K source rule, empty generated lists are spelled `.Exprs`/`.Stmts`;
the standalone .mpy concrete syntax spells those positions as empty text.
Those two explicit empty-list tokens are removed before exact token comparison.
"""

from __future__ import annotations

import re
from pathlib import Path


PROGRAM = Path("/tmp/audit-work/fresh/generated/solution.regenerated.mpy")
VERIFICATION = Path("/tmp/audit-work/fresh/candidate/verification.k")
TOKEN_RE = re.compile(
    r'\.Exprs|\.Stmts|"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z_0-9]*|-?[0-9]+|[(),]'
)


def extract_solution_ast_rhs(source: str) -> str:
    marker = "rule solutionAST =>"
    marker_index = source.index(marker)
    module_index = source.index("Module(", marker_index + len(marker))
    in_string = False
    escaped = False
    depth = 0
    for index in range(module_index, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[module_index : index + 1]
    raise ValueError("unterminated solutionAST RHS")


def main() -> int:
    program_tokens = TOKEN_RE.findall(PROGRAM.read_text(encoding="utf-8"))
    rhs = extract_solution_ast_rhs(VERIFICATION.read_text(encoding="utf-8"))
    verification_tokens_raw = TOKEN_RE.findall(rhs)
    verification_tokens = [
        token
        for token in verification_tokens_raw
        if token not in {".Exprs", ".Stmts"}
    ]
    equal = program_tokens == verification_tokens
    print("REGENERATED_PROGRAM:", PROGRAM)
    print("VERIFICATION:", VERIFICATION)
    print("PROGRAM_TOKEN_COUNT:", len(program_tokens))
    print("VERIFICATION_RAW_TOKEN_COUNT:", len(verification_tokens_raw))
    print("REMOVED_EXPLICIT_EMPTY_LIST_TOKENS:", len(verification_tokens_raw) - len(verification_tokens))
    print("VERIFICATION_NORMALIZED_TOKEN_COUNT:", len(verification_tokens))
    print("TOKEN_IDENTICAL:", equal)
    if not equal:
        for index, pair in enumerate(zip(program_tokens, verification_tokens)):
            if pair[0] != pair[1]:
                print("FIRST_DIFFERENCE_INDEX:", index)
                print("PROGRAM_TOKEN:", repr(pair[0]))
                print("VERIFICATION_TOKEN:", repr(pair[1]))
                break
        if len(program_tokens) != len(verification_tokens):
            print("TOKEN_COUNT_DIFFERENCE:", len(program_tokens) - len(verification_tokens))
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
