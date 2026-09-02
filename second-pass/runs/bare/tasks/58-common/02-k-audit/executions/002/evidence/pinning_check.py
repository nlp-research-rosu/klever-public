#!/usr/bin/env python3
"""Mechanically compare the claim's executed constructor with solution.mpy."""

from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/58-common-audit/candidate")


def balanced_module(text: str) -> str:
    start = text.index("Module(")
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
                return text[start : index + 1]
    raise ValueError("unbalanced Module constructor")


def tokens(text: str):
    return re.findall(r'"(?:\\.|[^"\\])*"|[A-Za-z_.][A-Za-z0-9_.-]*|-?[0-9]+|[(),&;]', text)


submitted = balanced_module((ROOT / "solution.mpy").read_text())
claimed = balanced_module((ROOT / "spec.k").read_text())
submitted_tokens = tokens(submitted)
claimed_tokens = tokens(claimed)

print("submitted_constructor=", "".join(submitted_tokens))
print("claim_constructor=", "".join(claimed_tokens))
print("submitted_token_count=", len(submitted_tokens))
print("claim_token_count=", len(claimed_tokens))
print("constructor_tokens_identical=", submitted_tokens == claimed_tokens)
raise SystemExit(submitted_tokens != claimed_tokens)
