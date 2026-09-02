#!/usr/bin/env python3
"""Produce a complete, line-addressable inventory of K source declarations."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/audit-38-20260729")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^  (configuration|syntax|context|rule|claim|alias)\b|^  syntax priority\b"
)
BOUNDARY = re.compile(
    r"^  (configuration|syntax|context|rule|claim|alias|module|endmodule|imports|requires)\b"
)


def classify(kind: str, text: str) -> tuple[str, str]:
    flags = []
    for flag in (
        "function",
        "functional",
        "total",
        "simplification",
        "concrete",
        "macro",
        "macro-rec",
        "owise",
        "priority",
        "symbol",
        "hook",
        "no-evaluators",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", text):
            flags.append(flag)
    if kind == "rule":
        if "macro" in flags or "macro-rec" in flags:
            category = "macro-rule"
        elif "<" in text and ">" in text:
            category = "operational-rule"
        else:
            category = "equational-rule"
    elif kind == "syntax" and ("function" in flags or "functional" in flags):
        category = "function-declaration"
    elif kind == "syntax":
        category = "syntax-declaration"
    elif kind == "claim":
        category = "reachability-claim"
    else:
        category = kind
    return category, ",".join(flags) if flags else "-"


records = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for index in starts:
        end = index + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        raw = "\n".join(lines[index:end]).strip()
        kind_match = re.match(r"(configuration|syntax|context|rule|claim|alias)", raw)
        assert kind_match is not None, (path, index + 1, raw)
        kind = kind_match.group(1)
        category, flags = classify(kind, raw)
        compact = " ".join(
            part.strip()
            for part in raw.splitlines()
            if part.strip() and not part.lstrip().startswith("//")
        )
        records.append(
            (
                path.relative_to(ROOT).as_posix(),
                index + 1,
                end,
                category,
                flags,
                compact,
            )
        )

counts = Counter(record[3] for record in records)
print("# Exhaustive K declaration and rule inventory")
print()
print(f"Files: {len(FILES)}")
print(f"Records: {len(records)}")
for category, count in sorted(counts.items()):
    print(f"- {category}: {count}")
print()
print("| ID | File:lines | Category | Attributes | Exact declaration/rule (condensed) |")
print("|---:|---|---|---|---|")
for number, (path, start, end, category, flags, compact) in enumerate(records, 1):
    escaped = compact.replace("|", "\\|")
    print(f"| K{number:04d} | `{path}:{start}-{end}` | {category} | {flags} | `{escaped}` |")
