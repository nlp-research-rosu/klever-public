#!/usr/bin/env python3
"""Create a source-faithful inventory of K declarations and rule blocks."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
START = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"configuration|syntax|rule|claim|context(?:\s+alias)?|alias"
    r")\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:configuration|syntax|rule|claim|context(?:\s+alias)?|alias|"
    r"module|endmodule|imports|requires)\b"
)
ATTRIBUTES = [
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
]


def source_files() -> list[Path]:
    files: list[Path] = []
    for root in ROOTS:
        if root.is_file():
            files.append(root)
        else:
            files.extend(sorted(root.rglob("*.k")))
    return sorted(files, key=str)


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for ordinal, start in enumerate(starts, 1):
        stop = len(lines)
        for i in range(start + 1, len(lines)):
            if BOUNDARY.match(lines[i]):
                stop = i
                break
        match = START.match(lines[start])
        assert match is not None
        text = "\n".join(lines[start:stop]).rstrip()
        yield ordinal, start + 1, match.group("kind"), text


counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
file_counts: dict[Path, Counter[str]] = {}
files = source_files()
print(f"SOURCE_FILE_COUNT: {len(files)}")
for path in files:
    print(f"SOURCE_FILE: {path}")
print()

global_ordinal = 0
for path in files:
    for file_ordinal, line, kind, text in blocks(path):
        global_ordinal += 1
        counts[kind] += 1
        file_counts.setdefault(path, Counter())[kind] += 1
        attrs = [attribute for attribute in ATTRIBUTES if attribute in text]
        for attribute in attrs:
            attribute_counts[attribute] += 1
        print(
            f"ENTRY {global_ordinal:04d} FILE={path} LINE={line} "
            f"KIND={kind} ATTRIBUTES={','.join(attrs) if attrs else '-'}"
        )
        print(text)
        print("END_ENTRY")
        print()

print(f"TOTAL_ENTRIES: {global_ordinal}")
for path in files:
    summary = ",".join(
        f"{kind}={count}" for kind, count in sorted(file_counts.get(path, {}).items())
    )
    print(f"FILE_COUNT {path}: {summary or '-'}")
for kind, count in sorted(counts.items()):
    print(f"KIND_COUNT {kind}: {count}")
for attribute, count in sorted(attribute_counts.items()):
    print(f"ATTRIBUTE_COUNT {attribute}: {count}")
