#!/usr/bin/env python3
"""Line-oriented exhaustive declaration/rule inventory for audited K sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path


START = re.compile(
    r"^\s*(syntax\b|rule\b|claim\b|configuration\b|context\b|alias\b)"
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:limit]).strip()
        first = lines[start].strip()
        kind = first.split(maxsplit=1)[0]
        attrs = []
        if re.search(r"\bfunction\b", block):
            attrs.append("function")
        if re.search(r"\btotal\b", block):
            attrs.append("total")
        if re.search(r"\bfunctional\b", block):
            attrs.append("functional")
        if re.search(r"\bsimplification\b", block):
            attrs.append("simplification")
        if re.search(r"\bno-evaluators\b", block):
            attrs.append("opaque/no-evaluators")
        if re.search(r"\bsymbol\s*\(", block):
            attrs.append("symbol")
        if re.search(r"\bconcrete\b", block):
            attrs.append("concrete")
        if re.search(r"\bowise\b", block):
            attrs.append("owise")
        if re.search(r"\bmacro(?:-rec)?\b", block):
            attrs.append("macro")
        if re.search(r"\bseqstrict\b", block):
            attrs.append("seqstrict")
        elif re.search(r"\bstrict\b", block):
            attrs.append("strict")
        priority = re.search(r"priority\((\d+)\)", block)
        if priority:
            attrs.append(f"priority({priority.group(1)})")
        summary = " ".join(piece.strip() for piece in block.splitlines())
        yield start + 1, kind, ",".join(attrs) or "-", summary


def main() -> None:
    print("file\tline\tkind\tattributes\ttext")
    for name in sys.argv[1:]:
        path = Path(name)
        for line, kind, attrs, summary in blocks(path):
            print(f"{path}\t{line}\t{kind}\t{attrs}\t{summary}")


if __name__ == "__main__":
    main()
