#!/usr/bin/env python3
"""Produce a source-level inventory of every local K sentence."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    Path("/reference/reference-semantics/semantics"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
START = re.compile(
    r"^\s*(module|endmodule|imports|requires|syntax|configuration|rule|claim|"
    r"context(?:\s+alias)?|priority|alias|macro)\b"
)
ATTRIBUTES = [
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
]


def paths() -> list[Path]:
    result: list[Path] = []
    for root in ROOTS:
        if root.is_dir():
            result.extend(sorted(root.glob("*.k")))
        else:
            result.append(root)
    return result


def sentences(path: Path) -> list[tuple[int, str, str]]:
    result: list[tuple[int, str, str]] = []
    current_line = 0
    current_kind = ""
    current: list[str] = []
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        if raw.lstrip().startswith("//") or not raw.strip():
            continue
        indentation = len(raw) - len(raw.lstrip())
        match = START.match(raw) if indentation <= 2 else None
        if match:
            if current:
                result.append(
                    (current_line, current_kind, " ".join(part.strip() for part in current))
                )
            current_line = line_number
            current_kind = match.group(1).replace(" ", "-")
            current = [raw]
        elif current:
            current.append(raw)
        else:
            raise AssertionError(f"orphan source text at {path}:{line_number}: {raw}")
    if current:
        result.append(
            (current_line, current_kind, " ".join(part.strip() for part in current))
        )
    return result


records: list[tuple[str, int, str, str, str]] = []
kind_counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
file_counts: dict[str, Counter[str]] = defaultdict(Counter)

for path in paths():
    for line, kind, text in sentences(path):
        flags = [attribute for attribute in ATTRIBUTES if re.search(
            rf"(?:\[|,|\s){re.escape(attribute)}(?:\(|\]|,|\s)", text
        )]
        # priority is also significant when written as a standalone declaration.
        if kind == "priority" and "priority" not in flags:
            flags.append("priority")
        flag_text = ",".join(flags) if flags else "-"
        relative = str(path)
        records.append((relative, line, kind, flag_text, text))
        kind_counts[kind] += 1
        file_counts[relative][kind] += 1
        for flag in flags:
            attribute_counts[flag] += 1

print("id\tfile\tline\tkind\tattributes\tsource")
for index, (path, line, kind, flags, text) in enumerate(records, 1):
    print(f"K{index:04d}\t{path}\t{line}\t{kind}\t{flags}\t{text}")

print()
print("SUMMARY_KIND")
for kind, count in sorted(kind_counts.items()):
    print(f"{kind}\t{count}")
print("SUMMARY_ATTRIBUTE")
for attribute, count in sorted(attribute_counts.items()):
    print(f"{attribute}\t{count}")
print("SUMMARY_FILE")
for path in sorted(file_counts):
    details = ",".join(f"{kind}={count}" for kind, count in sorted(file_counts[path].items()))
    print(f"{path}\t{details}")
