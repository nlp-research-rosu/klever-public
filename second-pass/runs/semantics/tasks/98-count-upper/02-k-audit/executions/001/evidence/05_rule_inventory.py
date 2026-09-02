#!/usr/bin/env python3
"""Exhaustive declaration inventory for the supplied K sources and candidate proof."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(r"^\s*(syntax|configuration|context|rule|claim)\b")


def uncomment(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def classify(kind: str, text: str) -> str:
    code = uncomment(text)
    tags: list[str] = [kind]
    if kind == "syntax":
        if re.search(r"\bfunction\b", code):
            tags.append("function")
        if re.search(r"\btotal\b", code):
            tags.append("total")
        if re.search(r"\bfunctional\b", code):
            tags.append("functional")
        if re.search(r"\bno-evaluators\b", code):
            tags.append("opaque/no-evaluators")
        if re.search(r"\bconcrete\b", code):
            tags.append("concrete")
        if re.search(r"\bmacro-rec\b", code):
            tags.append("macro-rec")
        elif re.search(r"\bmacro\b", code):
            tags.append("macro")
        if re.search(r"\bsymbol\s*\(", code):
            tags.append("symbol")
        if re.search(r"\bstrict\b|\bseqstrict\b", code):
            tags.append("strictness")
    elif kind == "rule":
        if re.search(r"\bpriority\s*\(", code):
            tags.append("priority")
        if re.search(r"\bsimplification\b", code):
            tags.append("simplification")
        if re.search(r"\bconcrete\b", code):
            tags.append("concrete")
        if re.search(r"\bowise\b", code):
            tags.append("owise")
        if len(tags) == 1:
            tags.append("ordinary")
    return ",".join(tags)


def flatten(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        code = raw.split("//", 1)[0].strip()
        if code:
            lines.append(code)
    return " ".join(lines)


def main() -> int:
    counts: collections.Counter[str] = collections.Counter()
    records: list[tuple[str, int, str, str]] = []
    for path in SOURCES:
        lines = path.read_text().splitlines()
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = START.match(line)
            if match:
                starts.append((index, match.group(1)))
        for position, (start, kind) in enumerate(starts):
            stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            stanza = "\n".join(lines[start:stop])
            category = classify(kind, stanza)
            relative = path.relative_to(ROOT).as_posix()
            records.append((relative, start + 1, category, flatten(stanza)))
            counts[kind] += 1
            for tag in category.split(",")[1:]:
                counts[f"{kind}:{tag}"] += 1

    print("# Exhaustive K declaration inventory")
    print(f"SOURCE_COUNT={len(SOURCES)}")
    print(f"DECLARATION_COUNT={len(records)}")
    for required_key in (
        "syntax:function",
        "syntax:total",
        "syntax:functional",
        "syntax:opaque/no-evaluators",
        "syntax:symbol",
        "syntax:macro",
        "syntax:macro-rec",
        "rule:ordinary",
        "rule:priority",
        "rule:simplification",
        "rule:concrete",
        "rule:owise",
    ):
        counts.setdefault(required_key, 0)
    for key in sorted(counts):
        print(f"COUNT[{key}]={counts[key]}")
    print()
    for number, (path, line, category, text) in enumerate(records, 1):
        print(f"{number:04d}|{path}:{line}|{category}|{text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
