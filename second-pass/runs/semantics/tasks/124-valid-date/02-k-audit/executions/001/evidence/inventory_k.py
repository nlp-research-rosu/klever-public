#!/usr/bin/env python3
"""Enumerate every top-level K declaration/rule in fixed and proof sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/reconstruction/reference-semantics/semantics.k"),
    *sorted(
        Path("/tmp/audit-work/reconstruction/reference-semantics/semantics").glob(
            "*.k"
        )
    ),
    Path("/tmp/audit-work/reconstruction/verification.k"),
    Path("/tmp/audit-work/reconstruction/spec.k"),
]
START = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration)\b"
)
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration|module|endmodule|imports)\b"
)


def flags(text: str) -> str:
    found = []
    for name in (
        "function",
        "functional",
        "total",
        "simplification",
        "priority",
        "symbol",
        "anywhere",
        "macro",
        "alias",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(name)}\b", text):
            found.append(name)
    return ",".join(found) if found else "-"


entries: list[tuple[str, int, str, str, str]] = []
for path in ROOTS:
    lines = path.read_text().splitlines()
    starts = [idx for idx, line in enumerate(lines) if START.match(line)]
    for idx in starts:
        match = START.match(lines[idx])
        assert match is not None
        end = idx + 1
        while end < len(lines):
            if BOUNDARY.match(lines[end]):
                break
            end += 1
        statement = "\n".join(lines[idx:end]).strip()
        normalized = re.sub(r"\s+", " ", statement)
        entries.append(
            (
                str(path),
                idx + 1,
                match.group(1),
                flags(statement),
                normalized,
            )
        )

kind_counts = Counter(entry[2] for entry in entries)
file_counts = Counter(entry[0] for entry in entries)
flag_counts: Counter[str] = Counter()
for _, _, _, entry_flags, _ in entries:
    for flag in entry_flags.split(","):
        if flag != "-":
            flag_counts[flag] += 1

print(f"TOTAL_ENTRIES\t{len(entries)}")
for kind, count in sorted(kind_counts.items()):
    print(f"KIND_COUNT\t{kind}\t{count}")
for flag, count in sorted(flag_counts.items()):
    print(f"FLAG_COUNT\t{flag}\t{count}")
for path, count in sorted(file_counts.items()):
    print(f"FILE_COUNT\t{path}\t{count}")
print("BEGIN_ENTRIES")
for number, (path, line, kind, entry_flags, statement) in enumerate(entries, 1):
    print(
        f"{number:04d}\t{path}:{line}\t{kind}\t{entry_flags}\t{statement}"
    )
