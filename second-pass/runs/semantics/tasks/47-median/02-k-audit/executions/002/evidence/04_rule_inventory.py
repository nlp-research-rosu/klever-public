#!/usr/bin/env python3
"""Produce a complete line-addressed inventory of local K declarations."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
FILES = [
    SCRATCH / "reference-semantics" / "semantics.k",
    *sorted((SCRATCH / "reference-semantics" / "semantics").glob("*.k")),
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|macro|alias)\b"
)
STOP = re.compile(
    r"^\s*(?:configuration|syntax|context|rule|claim|macro|alias|"
    r"module|endmodule|imports)\b"
)


def classify(kind: str, text: str) -> str:
    tags: list[str] = []
    if kind == "syntax":
        tags.append("syntax")
        for attr in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "strict",
            "seqstrict",
            "macro",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", text):
                tags.append(attr)
        if "symbol" in tags or "no-evaluators" in tags:
            tags.append("opaque")
    elif kind == "rule":
        tags.append("operational-rule" if "<k>" in text else "equational-rule")
        for attr in (
            "simplification",
            "priority",
            "owise",
            "concrete",
            "anywhere",
            "preserves-definedness",
        ):
            if re.search(rf"\b{re.escape(attr)}(?:\(|\b)", text):
                tags.append(attr)
    else:
        tags.append(kind)
    return ",".join(tags)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if match is None:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not STOP.match(lines[index]):
            index += 1
        text = " ".join(
            piece.strip()
            for piece in lines[start:index]
            if piece.strip() and not piece.lstrip().startswith("//")
        )
        text = re.sub(r"\s+", " ", text)
        yield start + 1, kind, classify(kind, text), text


def main() -> int:
    overall = Counter()
    per_file: dict[str, Counter] = defaultdict(Counter)
    records: list[tuple[str, int, str, str, str]] = []
    for path in FILES:
        rel = path.relative_to(SCRATCH).as_posix()
        for line, kind, classification, text in blocks(path):
            records.append((rel, line, kind, classification, text))
            overall["records"] += 1
            overall[kind] += 1
            per_file[rel]["records"] += 1
            per_file[rel][kind] += 1
            for tag in classification.split(","):
                overall[f"tag:{tag}"] += 1
                per_file[rel][f"tag:{tag}"] += 1

    print("K RULE/DECLARATION INVENTORY")
    print(f"FILES\t{len(FILES)}")
    for key in sorted(overall):
        print(f"TOTAL\t{key}\t{overall[key]}")
    print("PER_FILE_BEGIN")
    for rel in sorted(per_file):
        counts = " ".join(f"{key}={per_file[rel][key]}" for key in sorted(per_file[rel]))
        print(f"FILE_SUMMARY\t{rel}\t{counts}")
    print("PER_FILE_END")
    print("RECORDS_BEGIN")
    print("path\tline\tkind\tclassification\tstatement")
    for rel, line, kind, classification, text in records:
        print(f"{rel}\t{line}\t{kind}\t{classification}\t{text}")
    print("RECORDS_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
