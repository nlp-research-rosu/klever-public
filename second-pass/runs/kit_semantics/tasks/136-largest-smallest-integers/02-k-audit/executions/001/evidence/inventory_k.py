#!/usr/bin/env python3
"""Emit a source-located inventory of K declarations and proof extensions."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias|module|endmodule)\b"
)
ATTRS = (
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "symbol",
    "opaque",
    "strict",
    "seqstrict",
)


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        body_lines = []
        for line in lines[start:index]:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                body_lines.append(stripped)
        text = " ".join(body_lines)
        text = re.sub(r"\s+", " ", text)
        attrs = ",".join(attribute for attribute in ATTRS if attribute in text)
        yield start + 1, kind, attrs or "-", text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    files = []
    for path in args.paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.k")))
        else:
            files.append(path)
    files = sorted(dict.fromkeys(files), key=lambda path: path.as_posix())

    counts: collections.Counter[str] = collections.Counter()
    attr_counts: collections.Counter[str] = collections.Counter()
    records = []
    for path in files:
        for line, kind, attrs, text in declarations(path):
            counts[kind] += 1
            if attrs != "-":
                attr_counts.update(attrs.split(","))
            records.append((path, line, kind, attrs, text))

    print(f"FILES: {len(files)}")
    print(f"DECLARATIONS: {len(records)}")
    print(f"COUNTS: {dict(sorted(counts.items()))}")
    print(f"ATTRIBUTE-COUNTS: {dict(sorted(attr_counts.items()))}")
    print("INVENTORY-BEGIN")
    for path, line, kind, attrs, text in records:
        print(f"{path}:{line}\t{kind}\t{attrs}\t{text}")
    print("INVENTORY-END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
