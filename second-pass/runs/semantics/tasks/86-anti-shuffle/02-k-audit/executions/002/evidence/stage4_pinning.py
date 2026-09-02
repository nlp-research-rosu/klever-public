#!/usr/bin/env python3
"""Mechanical token-level comparison of translated and claimed program bodies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|[A-Za-z_#.$][A-Za-z0-9_#.$-]*|-?[0-9]+|=>|::=|[(),:]'
)


def matching_close(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
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
                return index
    raise ValueError(f"no matching close for index {open_index}")


def application_argument(text: str, constructor: str, arg_index: int) -> str:
    match = re.search(rf"\b{re.escape(constructor)}\s*\(", text)
    if match is None:
        raise ValueError(f"constructor {constructor} not found")
    open_index = text.index("(", match.start())
    close_index = matching_close(text, open_index)
    boundaries = [open_index + 1]
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index + 1, close_index):
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
        elif char == "," and depth == 0:
            boundaries.append(index + 1)
    boundaries.append(close_index + 1)
    if arg_index + 1 >= len(boundaries):
        raise ValueError(f"{constructor} has no argument {arg_index}")
    start = boundaries[arg_index]
    end = boundaries[arg_index + 1] - 1
    return text[start:end]


def macro_rhs(text: str, name: str) -> str:
    match = re.search(rf"\brule\s+{re.escape(name)}\s*=>", text)
    if match is None:
        raise ValueError(f"macro rule {name} not found")
    rest = text[match.end() :]
    terminator = rest.index(".Stmts")
    return rest[:terminator]


def tokens(text: str) -> list[str]:
    stripped = re.sub(r"//[^\n]*", "", text)
    return TOKEN.findall(stripped)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--solution",
        type=Path,
        default=ROOT / "regenerated-solution.mpy",
    )
    parser.add_argument(
        "--verification",
        type=Path,
        default=ROOT / "verification.k",
    )
    parser.add_argument("--spec", type=Path, default=ROOT / "spec.k")
    args = parser.parse_args()

    solution = args.solution.read_text(encoding="utf-8")
    verification = args.verification.read_text(encoding="utf-8")

    translated_body = application_argument(solution, "FuncDef", 2)
    translated_loop = application_argument(translated_body, "For", 2)
    claimed_loop = macro_rhs(verification, "antiLoopBody")
    loop_equal = tokens(translated_loop) == tokens(claimed_loop)

    claimed_body = macro_rhs(verification, "antiBody")
    claimed_body_tokens = tokens(claimed_body)
    loop_macro_positions = [
        index
        for index, token in enumerate(claimed_body_tokens)
        if token == "antiLoopBody"
    ]
    if len(loop_macro_positions) == 1:
        position = loop_macro_positions[0]
        claimed_body_tokens = (
            claimed_body_tokens[:position]
            + tokens(claimed_loop)
            + claimed_body_tokens[position + 1 :]
        )
    function_equal = tokens(translated_body) == claimed_body_tokens

    closure_literal = 'closureVal(("s", .ParamNames), antiBody, 0)'
    closure_count = args.spec.read_text(encoding="utf-8").count(
        closure_literal
    )

    print(f"TRANSLATED_FUNCTION_TOKENS={tokens(translated_body)!r}")
    print(f"CLAIMED_FUNCTION_TOKENS_AFTER_MACRO_EXPANSION={claimed_body_tokens!r}")
    print(f"LOOP_MACRO_POSITIONS={loop_macro_positions!r}")
    print(f"FUNCTION_BODY_TOKEN_EQUAL={function_equal}")
    print(f"TRANSLATED_LOOP_TOKENS={tokens(translated_loop)!r}")
    print(f"CLAIMED_LOOP_TOKENS={tokens(claimed_loop)!r}")
    print(f"LOOP_BODY_TOKEN_EQUAL={loop_equal}")
    print(f"EXACT_CLOSURE_LITERAL_COUNT={closure_count}")
    failures = int(not function_equal) + int(not loop_equal) + int(closure_count != 1)
    print(f"PINNING_FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
