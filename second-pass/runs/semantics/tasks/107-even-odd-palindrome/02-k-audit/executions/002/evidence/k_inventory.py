#!/usr/bin/env python3
"""Exhaustive source inventory of K declarations and rule-like sentences."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


START = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\b|context\s+alias\b)"
)
BOUNDARY = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\b|"
    r"module\b|endmodule\b|imports\b|requires\b)"
)
ATTR = re.compile(r"\[([^\]]+)\]")


def blocks(path: Path) -> list[tuple[int, str, list[str]]]:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    output: list[tuple[int, str, list[str]]] = []
    for position, index in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        while end > index + 1:
            candidate = lines[end - 1].strip()
            if (
                not candidate
                or candidate.startswith("//")
                or BOUNDARY.match(lines[end - 1])
            ):
                end -= 1
            else:
                break
        first_word = START.match(lines[index]).group(1).split()[0]  # type: ignore[union-attr]
        output.append((index + 1, first_word, lines[index:end]))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    totals: collections.Counter[str] = collections.Counter()
    attribute_totals: collections.Counter[str] = collections.Counter()

    for supplied in args.paths:
        paths = sorted(supplied.rglob("*.k")) if supplied.is_dir() else [supplied]
        for path in paths:
            file_counts: collections.Counter[str] = collections.Counter()
            print(f"===== FILE {path}")
            for line_number, kind, content_lines in blocks(path):
                text = "\n".join(content_lines)
                file_counts[kind] += 1
                totals[kind] += 1
                for attrs in ATTR.findall(text):
                    for attribute in attrs.split(","):
                        key = attribute.strip().split("(", 1)[0]
                        attribute_totals[key] += 1
                indented = "\n".join(f"    {line}" for line in content_lines)
                print(f"--- {kind.upper()} line={line_number}\n{indented}")
            print(f"FILE_COUNTS {dict(sorted(file_counts.items()))}")

    print(f"TOTAL_COUNTS {dict(sorted(totals.items()))}")
    print(f"ATTRIBUTE_COUNTS {dict(sorted(attribute_totals.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
