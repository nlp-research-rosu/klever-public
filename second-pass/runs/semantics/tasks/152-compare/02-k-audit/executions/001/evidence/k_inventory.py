#!/usr/bin/env python3
"""Produce a complete source-indexed inventory of K declarations and rules."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


SOURCE = Path("/tmp/audit-work/compare152/source")
FILES = sorted((SOURCE / "reference-semantics").rglob("*.k")) + [
    SOURCE / "verification.k",
    SOURCE / "spec.k",
    SOURCE / "operational-spec.k",
]

START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
STOP = re.compile(r"^\s*(?:module|endmodule|imports|requires)\b")


def category(kind: str, text: str) -> str:
    if kind == "syntax":
        tags = []
        for tag in (
            "function",
            "total",
            "functional",
            "macro-rec",
            "macro",
            "symbol",
            "no-evaluators",
            "token",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(tag)}\b", text):
                tags.append(tag)
        return "syntax" + ("/" + ",".join(tags) if tags else "")
    if kind == "rule":
        tags = []
        for tag in ("simplification", "priority", "concrete", "owise"):
            if re.search(rf"\b{tag}\b", text):
                tags.append(tag)
        return "rule/" + (",".join(tags) if tags else "ordinary")
    return kind


counts: collections.Counter[str] = collections.Counter()
records = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    file_records = []
    for index, start in enumerate(starts):
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1)
        next_start = starts[index + 1] if index + 1 < len(starts) else len(lines)
        end = start + 1
        while end < next_start:
            line = lines[end]
            if STOP.match(line) or (not line.strip()) or line.lstrip().startswith("//"):
                break
            end += 1
        text = "\n".join(lines[start:end]).rstrip()
        class_name = category(kind, text)
        counts[class_name] += 1
        file_records.append((start + 1, end, kind, class_name, text))
    records.append((path, file_records))

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Scope: the byte-verified supplied `reference-semantics/**/*.k`, "
    "`verification.k`, `spec.k`, and `operational-spec.k` in the clean scratch copy."
)
print()
for path, file_records in records:
    relative = path.relative_to(SOURCE)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"## `{relative}`")
    print()
    print(f"SHA-256: `{digest}`. Inventoried items: {len(file_records)}.")
    print()
    for ordinal, (start, end, kind, class_name, text) in enumerate(file_records, 1):
        line_label = str(start) if start == end else f"{start}-{end}"
        print(
            f"### {relative}:{line_label} — item {ordinal} "
            f"(`{kind}`, `{class_name}`)"
        )
        print()
        print("```k")
        print(text)
        print("```")
        print()

print("## Inventory totals")
print()
print(f"Files: {len(records)}")
print()
for class_name in sorted(counts):
    print(f"- `{class_name}`: {counts[class_name]}")
