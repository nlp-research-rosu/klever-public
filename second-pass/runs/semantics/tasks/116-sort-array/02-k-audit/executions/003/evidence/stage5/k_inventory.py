#!/usr/bin/env python3
"""Exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


START = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|rule|claim|context)\b"
)


def classify(kind: str, text: str) -> list[str]:
    classes: list[str] = []
    if kind == "syntax":
        classes.append("SYNTAX")
        for attribute in (
            "function",
            "total",
            "functional",
            "token",
            "strict",
            "seqstrict",
            "symbol",
        ):
            if re.search(rf"\b{attribute}\b", text):
                classes.append(attribute.upper())
    elif kind == "rule":
        classes.append("RULE")
        if "simplification" in text:
            classes.append("SIMPLIFICATION")
        else:
            classes.append("ORDINARY")
        for attribute in ("priority", "owise", "concrete", "anywhere"):
            if re.search(rf"\b{attribute}\b", text):
                classes.append(attribute.upper())
        if "<k>" in text:
            classes.append("K-CELL")
        else:
            classes.append("EQUATIONAL")
    elif kind == "claim":
        classes.append("CLAIM")
    elif kind == "configuration":
        classes.append("CONFIGURATION")
    else:
        classes.append(kind.upper())
    return classes


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for offset, (index, kind) in enumerate(starts):
        end = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        text = "\n".join(lines[index:end]).rstrip()
        yield index + 1, end, kind, text


paths = [Path(argument) for argument in sys.argv[1:]]
totals: collections.Counter[str] = collections.Counter()
file_totals: dict[str, collections.Counter[str]] = {}

records = []
for path in paths:
    counts: collections.Counter[str] = collections.Counter()
    for start, end, kind, text in declarations(path):
        classes = classify(kind, text)
        for item in classes:
            counts[item] += 1
            totals[item] += 1
        records.append((path, start, end, kind, classes, text))
    file_totals[str(path)] = counts

print("INVENTORY_SUMMARY")
for path in paths:
    counts = file_totals[str(path)]
    rendered = " ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"{path}: {rendered}")
print("TOTALS " + " ".join(f"{key}={totals[key]}" for key in sorted(totals)))

print("\nDECLARATIONS")
for number, (path, start, end, kind, classes, text) in enumerate(records, 1):
    print(
        f"\nINVENTORY_ID {number:04d} SOURCE {path}:{start}-{end} "
        f"KIND {kind} CLASS {','.join(classes)}"
    )
    print(text)
