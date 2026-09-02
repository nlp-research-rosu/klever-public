#!/usr/bin/env python3
"""Mechanical constructor-token comparison of solution.mpy and entry claims."""

from __future__ import annotations

import re
from pathlib import Path


def balanced_module_terms(text: str) -> list[str]:
    terms: list[str] = []
    start = 0
    while True:
        start = text.find("Module(", start)
        if start < 0:
            return terms
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            character = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    terms.append(text[start : index + 1])
                    start = index + 1
                    break
        else:
            raise ValueError(f"unbalanced Module term beginning at offset {start}")


token_pattern = re.compile(
    r'"(?:\\.|[^"\\])*"|'
    r"-?[0-9]+|"
    r"[A-Za-z_][A-Za-z_0-9-]*|"
    r"[(),]"
)


def tokens(term: str) -> list[str]:
    # K's concrete parser represents an empty List{Stmt, ""} as `.Stmts`.
    # The trusted translator prints that same empty list as the blank argument
    # between the surrounding comma and `)`.  Normalize only this syntax-level
    # spelling before comparing constructor tokens.
    normalized = term.replace(".Stmts", "")
    parsed = token_pattern.findall(normalized)
    residue = token_pattern.sub("", normalized)
    if residue.strip():
        raise ValueError(f"unexpected constructor-term text: {residue!r}")
    return parsed


mpy_text = Path("/tmp/audit-work/rebuild/solution.mpy").read_text()
spec_text = Path("/tmp/audit-work/rebuild/spec.k").read_text()

mpy_terms = balanced_module_terms(mpy_text)
spec_terms = balanced_module_terms(spec_text)
print(f"solution_module_term_count={len(mpy_terms)}")
print(f"spec_entry_module_term_count={len(spec_terms)}")
assert len(mpy_terms) == 1
assert len(spec_terms) == 3

mpy_tokens = tokens(mpy_terms[0])
print(f"solution_constructor_token_count={len(mpy_tokens)}")
for index, term in enumerate(spec_terms, 1):
    claim_tokens = tokens(term)
    match = claim_tokens == mpy_tokens
    print(
        f"entry_claim_{index}_token_count={len(claim_tokens)}:"
        f"constructor_exact_match={match}"
    )
    if not match:
        for offset, pair in enumerate(zip(mpy_tokens, claim_tokens)):
            if pair[0] != pair[1]:
                print(
                    f"first_difference[{index}]={offset}:"
                    f"solution={pair[0]!r}:claim={pair[1]!r}"
                )
                break
    assert match
