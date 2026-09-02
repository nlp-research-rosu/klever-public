#!/usr/bin/env python3
"""Mechanical constructor- and AST-level real-program pinning checks."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path


ROOT = Path("/tmp/audit-work/cycpattern-audit/candidate-src")


def normalize_k(text: str) -> str:
    """Drop whitespace and comments outside K string literals."""
    output: list[str] = []
    index = 0
    quoted = False
    escaped = False
    while index < len(text):
        char = text[index]
        if quoted:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
            continue
        if char == '"':
            quoted = True
            output.append(char)
            index += 1
            continue
        if text.startswith("//", index):
            newline = text.find("\n", index)
            index = len(text) if newline < 0 else newline + 1
            continue
        if char.isspace():
            index += 1
            continue
        output.append(char)
        index += 1
    if quoted:
        raise ValueError("unterminated K string literal")
    return "".join(output)


def extract_balanced_argument(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
    quoted = False
    escaped = False
    index = start
    while index < len(text):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        else:
            if char == '"':
                quoted = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return text[start:index]
        index += 1
    raise ValueError(f"unbalanced term after {marker!r}")


def function_ast(path: Path) -> str:
    module = ast.parse(path.read_text(), filename=str(path))
    functions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1:
        raise AssertionError(f"{path} has {len(functions)} functions")
    return ast.dump(functions[0], include_attributes=False)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    submitted = normalize_k((ROOT / "solution.mpy").read_text().strip())
    spec_text = (ROOT / "spec.k").read_text()
    claimed_module = normalize_k(extract_balanced_argument(spec_text, "#loadAll("))

    candidate_ast = function_ast(ROOT / "solution.py")
    smoke_ast = function_ast(ROOT / "concrete_smoke.py")

    print(f"solution_mpy_normalized_sha256={digest(submitted)}")
    print(f"entry_claim_module_normalized_sha256={digest(claimed_module)}")
    print(f"constructor_term_identity={submitted == claimed_module}")
    print(f"solution_function_ast_sha256={digest(candidate_ast)}")
    print(f"concrete_smoke_function_ast_sha256={digest(smoke_ast)}")
    print(f"concrete_smoke_function_ast_identity={candidate_ast == smoke_ast}")
    return 0 if submitted == claimed_module and candidate_ast == smoke_ast else 1


if __name__ == "__main__":
    raise SystemExit(main())
