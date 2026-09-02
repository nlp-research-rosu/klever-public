#!/usr/bin/env python3
"""Compare the exact lowered AST term in semantic.k and the end claim."""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys


def extract_balanced_module(text: str) -> str:
    start = text.index("Module(")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
                return text[start : index + 1]
    raise ValueError("unbalanced Module term")


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} semantic.k spec.k")
        return 64
    semantic_path = pathlib.Path(sys.argv[1])
    spec_path = pathlib.Path(sys.argv[2])
    semantic_term = normalize(
        extract_balanced_module(semantic_path.read_text(encoding="utf-8"))
    )
    spec_term = normalize(extract_balanced_module(spec_path.read_text(encoding="utf-8")))
    print(f"semantic_path={semantic_path.resolve()}")
    print(f"spec_path={spec_path.resolve()}")
    print(f"semantic_term_sha256={hashlib.sha256(semantic_term.encode()).hexdigest()}")
    print(f"spec_term_sha256={hashlib.sha256(spec_term.encode()).hexdigest()}")
    print(f"normalized_terms_equal={semantic_term == spec_term}")
    if semantic_term != spec_term:
        print(f"semantic_term={semantic_term}")
        print(f"spec_term={spec_term}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
