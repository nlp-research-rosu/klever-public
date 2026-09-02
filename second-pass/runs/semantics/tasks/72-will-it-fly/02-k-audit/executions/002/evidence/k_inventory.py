#!/usr/bin/env python3
"""Exhaustive lexical inventory of supplied and proof-local K sentences.

This deliberately inventories source sentences, not generated kompile rules.
Each rule/configuration/context/syntax declaration is emitted with its complete
collapsed source text and relevant attributes.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(
    r"^[ \t]*(module|imports|syntax|configuration|context|rule|claim|alias|endmodule)\b"
)
ATTR_NAMES = (
    "function",
    "functional",
    "total",
    "no-evaluators",
    "symbol",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)


def mask_comments(text: str) -> str:
    out = list(text)
    i = 0
    state = "code"
    block_depth = 0
    while i < len(text):
        char = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if state == "line":
            if char == "\n":
                state = "code"
            else:
                out[i] = " "
            i += 1
        elif state == "string":
            if char == "\\" and nxt:
                out[i] = out[i + 1] = " "
                i += 2
            else:
                if char == '"':
                    state = "code"
                elif char != "\n":
                    out[i] = " "
                i += 1
        elif state == "block":
            if char == "/" and nxt == "*":
                out[i] = out[i + 1] = " "
                block_depth += 1
                i += 2
            elif char == "*" and nxt == "/":
                out[i] = out[i + 1] = " "
                block_depth -= 1
                i += 2
                if block_depth == 0:
                    state = "code"
            else:
                if char != "\n":
                    out[i] = " "
                i += 1
        elif char == "/" and nxt == "/":
            out[i] = out[i + 1] = " "
            state = "line"
            i += 2
        elif char == "/" and nxt == "*":
            out[i] = out[i + 1] = " "
            state = "block"
            block_depth = 1
            i += 2
        else:
            if char == '"':
                state = "string"
            i += 1
    return "".join(out)


def sentences(path: Path):
    text = path.read_text()
    masked_lines = mask_comments(text).splitlines()
    raw_lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(masked_lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(raw_lines)
        if kind in {"module", "imports", "endmodule"}:
            end = start + 1
        segment = "\n".join(raw_lines[start:end]).strip()
        if segment:
            yield start + 1, end, kind, segment


def classify(kind: str, text: str) -> str:
    code = mask_comments(text)
    found = []
    for name in ATTR_NAMES:
        if name in {"priority", "symbol"}:
            hit = re.search(rf"\b{name}\s*\(", code)
        else:
            hit = re.search(rf"\b{re.escape(name)}\b", code)
        if hit:
            found.append(name)
    if kind == "rule" and not found:
        found.append("ordinary")
    return ",".join(found) if found else "-"


parser = argparse.ArgumentParser()
parser.add_argument("paths", nargs="+", type=Path)
args = parser.parse_args()

files: list[Path] = []
for supplied in args.paths:
    if supplied.is_dir():
        files.extend(sorted(supplied.rglob("*.k")))
    else:
        files.append(supplied)

counts: dict[str, int] = {}
print("source\tlines\tkind\tattributes\ttext")
for path in files:
    for start, end, kind, text in sentences(path):
        if kind not in {"syntax", "configuration", "context", "rule", "claim", "alias"}:
            continue
        counts[kind] = counts.get(kind, 0) + 1
        collapsed = " ".join(text.split())
        print(
            f"{path}:{start}\t{start}-{end}\t{kind}\t"
            f"{classify(kind, text)}\t{collapsed}"
        )

print("# counts " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
