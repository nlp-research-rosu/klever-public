#!/usr/bin/env python3
"""Create a line-addressed inventory of every local K declaration and rule."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/candidate")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s{2}(configuration|syntax(?:\s+(?:priority|associativity))?|"
    r"rule|claim|context(?:\s+alias)?)\b"
)
ATTR_TOKEN = re.compile(
    r"(?:\bfunction\b|\btotal\b|\bfunctional\b|\bmacro-rec\b|\bmacro\b|\bconcrete\b|\bowise\b|"
    r"simplification|anywhere|no-evaluators|"
    r"priority\(\d+\)|seqstrict\([^)]*\)|strict(?:\([^)]*\))?|"
    r"symbol\([^)]*\))"
)
BRACKET = re.compile(r"\[([^\]]+)\]")


def one_line(lines: list[str]) -> str:
    return " ".join(" ".join(lines).split())


counts: dict[str, int] = {}
attribute_counts: dict[str, int] = {}
records: list[tuple[str, int, str, str, str]] = []

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        while end > start and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        block = one_line(lines[start:end])
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1)
        attrs = sorted(
            {
                token
                for bracket in BRACKET.findall(block)
                for token in ATTR_TOKEN.findall(bracket)
            }
        )
        counts[kind] = counts.get(kind, 0) + 1
        for attr in attrs:
            attribute_counts[attr] = attribute_counts.get(attr, 0) + 1
        records.append(
            (
                path.relative_to(ROOT).as_posix(),
                start + 1,
                kind,
                ",".join(attrs) or "-",
                block,
            )
        )

print("SUMMARY")
for key in sorted(counts):
    print(f"{key}\t{counts[key]}")
print("ATTRIBUTES")
for key in sorted(attribute_counts):
    print(f"{key}\t{attribute_counts[key]}")
print("RECORDS")
print("file\tline\tkind\tattributes\tdeclaration")
for record in records:
    print("\t".join(map(str, record)))
