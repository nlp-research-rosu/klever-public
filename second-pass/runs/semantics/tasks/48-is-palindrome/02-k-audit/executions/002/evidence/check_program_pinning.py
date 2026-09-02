#!/usr/bin/env python3
"""Mechanically compare the translated program with the SPEC #loadAll term."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


def balanced_argument(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
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
                return text[start:index]
    raise ValueError(f"unbalanced argument after {marker}")


def normalized(term: str) -> str:
    without_line_comments = re.sub(r"//[^\n]*", "", term)
    without_empty_stmts = without_line_comments.replace(".Stmts", "")
    return re.sub(r"\s+", "", without_empty_stmts)


parser = argparse.ArgumentParser()
parser.add_argument("--translated", type=pathlib.Path, required=True)
parser.add_argument("--spec", type=pathlib.Path, required=True)
parser.add_argument("--executed-out", type=pathlib.Path)
parser.add_argument("--executed-surface-out", type=pathlib.Path)
args = parser.parse_args()

translated = args.translated.read_text(encoding="utf-8")
spec = args.spec.read_text(encoding="utf-8")
executed = balanced_argument(spec, "#loadAll(")
if args.executed_out is not None:
    args.executed_out.write_text(executed.strip() + "\n", encoding="utf-8")
if args.executed_surface_out is not None:
    args.executed_surface_out.write_text(
        executed.replace(".Stmts", "").strip() + "\n", encoding="utf-8"
    )

translated_normalized = normalized(translated)
executed_normalized = normalized(executed)

print(f"translated={args.translated}")
print(f"spec={args.spec}")
print(f"executed_out={args.executed_out}")
print(f"executed_surface_out={args.executed_surface_out}")
print(f"translated_normalized={translated_normalized}")
print(f"executed_normalized={executed_normalized}")
print(f"translated_length={len(translated_normalized)}")
print(f"executed_length={len(executed_normalized)}")
print(f"constructor_level_equal={translated_normalized == executed_normalized}")
print("normalization=whitespace/comments and explicit .Stmts list identity only")
if translated_normalized != executed_normalized:
    sys.exit(1)
