#!/usr/bin/env python3
"""Mechanical constructor-token comparison for the term executed by SPEC."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


REGENERATED = Path("/tmp/audit-work/candidate-source/solution.regenerated.mpy")
SPEC = Path("/tmp/audit-work/candidate-source/spec.k")
TOKEN = re.compile(
    r"""
    "(?:\\.|[^"\\])*" |
    \#?[A-Za-z_][A-Za-z0-9_\-]* |
    -?[0-9]+ |
    =>|~>|::=|\|->|\.\.\. |
    [(),:\[\]{}]
    """,
    re.VERBOSE,
)


def strip_line_comments(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def tokens(text: str) -> list[str]:
    return TOKEN.findall(strip_line_comments(text))


def loaded_module_tokens(spec_tokens: list[str]) -> list[str]:
    try:
        start = spec_tokens.index("#loadAll")
    except ValueError as error:
        raise AssertionError("SPEC has no #loadAll term") from error
    assert spec_tokens[start + 1] == "("
    depth = 1
    inside: list[str] = []
    for token in spec_tokens[start + 2 :]:
        if token == "(":
            depth += 1
            inside.append(token)
        elif token == ")":
            depth -= 1
            if depth == 0:
                return inside
            inside.append(token)
        else:
            inside.append(token)
    raise AssertionError("unbalanced #loadAll term")


def main() -> None:
    regenerated_tokens = tokens(REGENERATED.read_text(encoding="utf-8"))
    spec_tokens = tokens(SPEC.read_text(encoding="utf-8"))
    loaded_tokens = loaded_module_tokens(spec_tokens)
    regenerated_serial = "\0".join(regenerated_tokens).encode()
    loaded_serial = "\0".join(loaded_tokens).encode()
    print(f"regenerated_constructor_tokens={len(regenerated_tokens)}")
    print(f"loaded_constructor_tokens={len(loaded_tokens)}")
    print(f"regenerated_token_sha256={hashlib.sha256(regenerated_serial).hexdigest()}")
    print(f"loaded_token_sha256={hashlib.sha256(loaded_serial).hexdigest()}")
    print(f"constructor_token_identity={regenerated_tokens == loaded_tokens}")
    print(f"claim_count={spec_tokens.count('claim')}")
    print(f"load_all_count={spec_tokens.count('#loadAll')}")
    assert regenerated_tokens == loaded_tokens
    assert spec_tokens.count("claim") == 1
    assert spec_tokens.count("#loadAll") == 1
    print("PINNING_CHECK_PASSED")


if __name__ == "__main__":
    main()
