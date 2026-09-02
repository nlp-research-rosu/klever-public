#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
SOURCES = sorted((ROOT / "semantics").glob("*.k"))
SOURCES.insert(0, ROOT / "semantics.k")
SOURCES.extend([Path("/candidate/verification.k"), Path("/candidate/spec.k")])

ENTRY = re.compile(r"^\s*(configuration|context|syntax|rule|claim)\b")
STOP = re.compile(r"^\s*(?:module|endmodule)\b")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(kind: str, text: str) -> list[str]:
    classes = [kind]
    if kind == "syntax":
        for attribute in (
            "function",
            "functional",
            "total",
            "macro",
            "macro-rec",
            "symbol",
            "no-evaluators",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", text):
                classes.append(attribute)
        if "symbol" in classes or "no-evaluators" in classes:
            classes.append("opaque-symbol")
    if kind == "rule":
        if "[concrete]" in text:
            classes.append("concrete")
        if "[owise]" in text:
            classes.append("owise")
        if "simplification" in text:
            classes.append("simplification")
        match = re.search(r"priority\s*\(\s*(\d+)\s*\)", text)
        if match:
            classes.append(f"priority({match.group(1)})")
        if not any(
            item in classes
            for item in ("concrete", "owise", "simplification")
        ) and not any(item.startswith("priority(") for item in classes):
            classes.append("ordinary")
    return classes


records = []
for path in SOURCES:
    lines = path.read_text().splitlines()
    current = None
    for line_no, line in enumerate(lines, 1):
        match = ENTRY.match(line)
        if match:
            if current is not None:
                records.append(current)
            current = {
                "path": path,
                "line": line_no,
                "kind": match.group(1),
                "lines": [line.rstrip()],
            }
            continue
        if STOP.match(line):
            if current is not None:
                records.append(current)
                current = None
            continue
        if current is not None:
            # Keep the complete declaration/claim/rule through guards and attrs,
            # omitting blank/comment-only separators.
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                current["lines"].append(line.rstrip())
    if current is not None:
        records.append(current)

for record in records:
    record["text"] = "\n".join(record.pop("lines"))
    record["classes"] = classify(record["kind"], record["text"])

counts = Counter()
file_counts: dict[Path, Counter] = {}
for record in records:
    for item in record["classes"]:
        counts[item] += 1
        file_counts.setdefault(record["path"], Counter())[item] += 1

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Generated mechanically from the trusted supplied semantics and the "
    "candidate's proof-local files. Multiline entries include their guards "
    "and attributes."
)
print()
print("## Source hashes")
print()
for path in SOURCES:
    print(f"- `{path}`: `{digest(path)}`")
print()
print("## Global counts")
print()
for key in sorted(counts):
    print(f"- {key}: {counts[key]}")
print()
print("## Per-file counts")
print()
for path in SOURCES:
    summary = ", ".join(
        f"{key}={value}" for key, value in sorted(file_counts.get(path, {}).items())
    )
    print(f"- `{path}`: {summary or 'no inventoried entries'}")
print()
print("## Entries")
print()
for record in records:
    path = record["path"]
    location = f"{path}:{record['line']}"
    classes = ", ".join(record["classes"])
    print(f"### `{location}` — {classes}")
    print()
    print("```k")
    print(record["text"])
    print("```")
    print()
