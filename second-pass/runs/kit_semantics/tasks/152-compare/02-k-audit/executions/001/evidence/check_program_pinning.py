#!/usr/bin/env python3
"""Mechanical token-level comparison of translated module and entry-claim module."""

import re
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[A-Za-z][A-Za-z0-9]*|\.?[A-Za-z][A-Za-z0-9]*|-?[0-9]+|[(),]')


def balanced_argument(text: str, marker: str, start: int = 0):
    at = text.index(marker, start)
    open_at = text.index("(", at)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_at, len(text)):
        char = text[index]
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
                return text[open_at + 1 : index], index + 1
    raise ValueError(f"unbalanced occurrence of {marker}")


def normalized_tokens(text: str):
    # K's explicit empty sequence units are semantically inert syntax
    # normalization relative to the translator's omitted units.
    return [token for token in TOKEN.findall(text) if token not in {".Stmts", ".Exprs"}]


solution_text = Path("/tmp/audit-work/candidate/solution.regenerated.mpy").read_text()
spec_text = Path("/tmp/audit-work/candidate/spec.k").read_text()
solution_tokens = normalized_tokens(solution_text)

cursor = 0
entry_terms = []
while True:
    try:
        term, cursor = balanced_argument(spec_text, "#loadAll", cursor)
    except ValueError:
        break
    entry_terms.append(term)

print("translated_token_count:", len(solution_tokens))
print("entry_module_count:", len(entry_terms))
all_equal = True
for index, term in enumerate(entry_terms, 1):
    tokens = normalized_tokens(term)
    equal = tokens == solution_tokens
    all_equal = all_equal and equal
    print(f"entry_{index}_token_count:", len(tokens))
    print(f"entry_{index}_constructor_token_identity:", equal)
    if not equal:
        for position, (left, right) in enumerate(zip(solution_tokens, tokens)):
            if left != right:
                print(f"entry_{index}_first_difference:", position, left, right)
                break
        if len(solution_tokens) != len(tokens):
            print(f"entry_{index}_length_difference:", len(solution_tokens), len(tokens))

print("all_entry_modules_identical_after_empty-unit_normalization:", all_equal)
raise SystemExit(0 if all_equal and len(entry_terms) == 2 else 1)
