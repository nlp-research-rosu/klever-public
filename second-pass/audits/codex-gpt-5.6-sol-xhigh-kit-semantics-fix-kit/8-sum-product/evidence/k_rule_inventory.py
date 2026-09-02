#!/usr/bin/env python3
"""Emit a source-located exhaustive declaration/rule inventory for K files."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias)\b")
BOUNDARY = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias|module|endmodule|requires)\b")
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "anywhere",
    "strict",
    "seqstrict",
    "macro",
    "hook",
    "symbol",
)


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for offset, index in enumerate(starts):
        next_index = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        # Do not attach following module delimiters/comments to the declaration.
        for probe in range(index + 1, next_index):
            if BOUNDARY.match(lines[probe]) and not START.match(lines[probe]):
                next_index = probe
                break
        block = "\n".join(lines[index:next_index]).strip()
        normalized = " ".join(block.split())
        kind = START.match(lines[index]).group(1)  # type: ignore[union-attr]
        bracket_text = " ".join(re.findall(r"\[([^\]]*)\]", block, flags=re.DOTALL))
        attrs = [
            attribute
            for attribute in ATTRIBUTES
            if re.search(rf"\b{re.escape(attribute)}\b", bracket_text)
        ]
        yield index + 1, kind, ",".join(attrs) if attrs else "-", normalized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    paths: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.k")))
        else:
            paths.append(path)
    counts: Counter[str] = Counter()
    total = 0
    print("file\tline\tkind\tattributes\tdeclaration")
    for path in sorted(dict.fromkeys(paths)):
        for line, kind, attrs, first in declarations(path):
            total += 1
            counts[kind] += 1
            print(f"{path}\t{line}\t{kind}\t{attrs}\t{first}")
    print(f"TOTAL\t{total}")
    for kind in sorted(counts):
        print(f"COUNT_{kind.upper()}\t{counts[kind]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
