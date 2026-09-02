#!/usr/bin/env python3
"""Emit a line-addressed inventory of K declarations, rules, and attributes."""

from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^(?:requires\b|\s*(?:module|endmodule|imports|configuration|"
    r"context(?:\s+alias)?|syntax|rule|claim)\b)"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "anywhere",
    "preserves-definedness",
)


def files_from(args: list[str]) -> list[Path]:
    result: list[Path] = []
    for raw in args:
        path = Path(raw)
        if path.is_dir():
            result.extend(sorted(path.rglob("*.k")))
        else:
            result.append(path)
    return sorted(dict.fromkeys(result), key=lambda item: str(item))


def main() -> int:
    paths = files_from(sys.argv[1:])
    if not paths:
        print("usage: inventory_k.py K_FILE_OR_DIRECTORY ...", file=sys.stderr)
        return 64

    totals: Counter[str] = Counter()
    print("K SOURCE MANIFEST")
    for path in paths:
        data = path.read_bytes()
        lines = data.decode().splitlines()
        print(
            f"{path} lines={len(lines)} bytes={len(data)} "
            f"sha256={hashlib.sha256(data).hexdigest()}"
        )

    print("\nDECLARATION AND RULE INVENTORY")
    for path in paths:
        lines = path.read_text().splitlines()
        print(f"\nFILE {path}")
        starts = [
            (index, match)
            for index, line in enumerate(lines)
            if (match := START.match(line)) is not None
        ]
        for position, (index, match) in enumerate(starts):
            line_number = index + 1
            stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            block_lines = lines[index:stop]
            block_text = "\n".join(block_lines)
            kind_match = re.match(
                r"^\s*(requires|module|endmodule|imports|configuration|"
                r"context(?:\s+alias)?|syntax|rule|claim)\b",
                lines[index],
            )
            assert kind_match is not None
            kind = kind_match.group(1).replace(" ", "_")
            totals[kind] += 1
            attribute_text = "\n".join(
                re.sub(r"//.*$", "", block_line) for block_line in block_lines
            )
            found_attrs = [
                attr
                for attr in ATTRS
                if re.search(
                    rf"(?<![A-Za-z0-9_-]){re.escape(attr)}(?![A-Za-z0-9_-])",
                    attribute_text,
                )
            ]
            for attr in found_attrs:
                totals[f"attribute:{attr}"] += 1
            suffix = f" attrs={','.join(found_attrs)}" if found_attrs else ""
            print(f"BEGIN {line_number:04d} {kind}{suffix}")
            for block_index, block_line in enumerate(block_lines, line_number):
                print(f"{block_index:04d} | {block_line}")
            print(f"END {line_number:04d} {kind}")

    print("\nCOUNTS")
    for key in sorted(totals):
        print(f"{key}={totals[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
