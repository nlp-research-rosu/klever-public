#!/usr/bin/env python3
"""Emit a line-addressable exhaustive inventory of K declarations and rules."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
START = re.compile(
    r"^\s*(configuration|syntax(?:\s+priority|\s+associativity)?|"
    r"context(?:\s+alias)?|rule|claim)\b"
)
ATTRS = [
    "function",
    "functional",
    "total",
    "no-evaluators",
    "symbol",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]


def source_paths():
    paths = []
    for root in ROOTS:
        if root.is_dir():
            paths.extend(sorted(root.rglob("*.k")))
        else:
            paths.append(root)
    return paths


def compact(block: list[str]) -> str:
    kept = []
    for line in block:
        if line.lstrip().startswith("//"):
            continue
        code = line.strip()
        if code:
            kept.append(code)
    return " ".join(kept)


entries = []
files = source_paths()
for path in files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        while end > start and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        text = compact(lines[start:end])
        category = kind.split()[0]
        flags = [flag for flag in ATTRS if re.search(rf"\b{re.escape(flag)}\b", text)]
        if category == "rule" and "simplification" in flags:
            category = "simplification-rule"
        elif category == "rule":
            category = "ordinary-rule"
        elif category == "syntax" and (
            "no-evaluators" in flags or "symbol" in flags
        ):
            category = "opaque-or-symbolic-syntax"
        entries.append(
            {
                "path": path,
                "start": start + 1,
                "end": end,
                "category": category,
                "flags": flags,
                "text": text,
            }
        )

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Generated from the trusted supplied semantics and the candidate's proof/spec "
    "sources. Each entry records its complete source span compacted to one line."
)
print()
print("## Source manifest")
print()
for path in files:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"- `{path}` — sha256 `{digest}`")

print()
print("## Aggregate counts")
print()
category_counts = Counter(entry["category"] for entry in entries)
attribute_counts = Counter(
    flag for entry in entries for flag in set(entry["flags"])
)
print(f"- Files: {len(files)}")
print(f"- Total inventoried declarations/rules/claims/contexts: {len(entries)}")
for name, count in sorted(category_counts.items()):
    print(f"- Category `{name}`: {count}")
for name, count in sorted(attribute_counts.items()):
    print(f"- Attribute marker `{name}`: {count}")

for path in files:
    selected = [entry for entry in entries if entry["path"] == path]
    print()
    print(f"## {path}")
    print()
    if not selected:
        print("- No local syntax, configuration, context, rule, or claim declarations.")
        continue
    for entry in selected:
        span = (
            str(entry["start"])
            if entry["start"] == entry["end"]
            else f"{entry['start']}-{entry['end']}"
        )
        flags = ",".join(entry["flags"]) if entry["flags"] else "-"
        if str(path).startswith("/reference/reference-semantics/"):
            disposition = (
                "selected trusted supplied semantics; candidate copy is byte-identical"
            )
        elif path == Path("/candidate/verification.k"):
            disposition = "candidate proof extension; individually assessed in REVIEW.md"
        else:
            disposition = "candidate target claim; adequacy assessed in REVIEW.md"
        print(
            f"- `{span}` | `{entry['category']}` | attrs `{flags}` | "
            f"disposition `{disposition}` | "
            f"`{entry['text'].replace('`', chr(39))}`"
        )
