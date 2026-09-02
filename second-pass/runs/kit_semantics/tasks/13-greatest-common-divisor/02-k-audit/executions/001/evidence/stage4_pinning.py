#!/usr/bin/env python3
"""Mechanical constructor/body and compositional-control comparison."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def normalize_k(text: str) -> str:
    """Remove comments and non-string whitespace while preserving strings."""
    output: list[str] = []
    index = 0
    state = "code"
    block_depth = 0
    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if char == "\n":
                state = "code"
            index += 1
            continue
        if state == "block-comment":
            if char == "/" and following == "*":
                block_depth += 1
                index += 2
                continue
            if char == "*" and following == "/":
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
                continue
            index += 1
            continue
        if state == "string":
            output.append(char)
            if char == "\\" and following:
                output.append(following)
                index += 2
                continue
            if char == '"':
                state = "code"
            index += 1
            continue
        if char == "/" and following == "/":
            state = "line-comment"
            index += 2
            continue
        if char == "/" and following == "*":
            state = "block-comment"
            block_depth = 1
            index += 2
            continue
        if char == '"':
            state = "string"
            output.append(char)
        elif not char.isspace():
            output.append(char)
        index += 1
    return "".join(output)


def matching_close(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    index = open_index
    while index < len(text):
        char = text[index]
        if in_string:
            if char == "\\":
                index += 2
                continue
            if char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    raise ValueError("unbalanced term")


def closure_bodies(text: str) -> list[str]:
    prefix = 'closureVal(("a","b"),'
    bodies: list[str] = []
    position = 0
    while True:
        found = text.find(prefix, position)
        if found < 0:
            return bodies
        body_start = found + len(prefix)
        closure_open = found + len("closureVal")
        closure_close = matching_close(text, closure_open)
        depth = 1
        in_string = False
        separator = None
        index = body_start
        while index < closure_close:
            char = text[index]
            if in_string:
                if char == "\\":
                    index += 2
                    continue
                if char == '"':
                    in_string = False
            elif char == '"':
                in_string = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "," and depth == 1:
                separator = index
                break
            index += 1
        if separator is None or text[separator:closure_close + 1] != ",0)":
            raise ValueError("unexpected closure environment argument")
        bodies.append(text[body_start:separator])
        position = closure_close + 1


def k_cell(spec_source: str, label: str) -> tuple[str, str]:
    claim = re.search(
        rf"claim\s+\[{re.escape(label)}\]:(.*?)(?=\n\s*claim\s+\[|\nendmodule)",
        spec_source,
        re.S,
    )
    if claim is None:
        raise ValueError(f"missing claim {label}")
    cell = re.search(r"<k>(.*?)</k>", claim.group(1), re.S)
    if cell is None:
        raise ValueError(f"missing k cell in {label}")
    normalized = normalize_k(cell.group(1))
    if normalized.count("=>") != 1:
        raise ValueError(f"unexpected rewrite count in {label} k cell")
    return tuple(normalized.split("=>", 1))  # type: ignore[return-value]


solution_text = normalize_k(
    Path("/tmp/audit-work/candidate/solution.regenerated.mpy").read_text()
)
function_prefix = 'FuncDef("greatest_common_divisor",Params("a","b"),'
function_start = solution_text.find(function_prefix)
if function_start < 0:
    raise SystemExit("translated function binding/signature not found")
function_open = function_start + len('FuncDef')
function_close = matching_close(solution_text, function_open)
translated_body = solution_text[
    function_start + len(function_prefix):function_close
]

spec_path = Path("/tmp/audit-work/candidate/spec.k")
spec_source = spec_path.read_text()
spec_text = normalize_k(spec_source)
bodies = closure_bodies(spec_text)
body_matches = [body == translated_body for body in bodies]

loop_left, _loop_right = k_cell(spec_source, "gcd-loop")
_entry_left, entry_right = k_cell(spec_source, "gcd-entry")

print(f"translated_function_body_sha256={hashlib.sha256(translated_body.encode()).hexdigest()}")
print(f"closure_occurrences={len(bodies)}")
print(f"closure_body_matches={body_matches}")
print(
    "entry_target_loop_source_control_exact_match="
    f"{entry_right == loop_left}"
)
print("composition_cell_unifier=GLOBALS:<entry global map>,_R:0,CONT:.K")
print(
    "program_constructor_counts="
    + repr(
        {
            name: translated_body.count(name)
            for name in (
                "Expr(",
                "Str(",
                "Assign(",
                "While(",
                "Compare(",
                "BinOp(",
                "Return(",
                "Call(",
                "Name(",
                "Int(",
            )
        }
    )
)

if len(bodies) != 2 or not all(body_matches) or entry_right != loop_left:
    raise SystemExit(1)
