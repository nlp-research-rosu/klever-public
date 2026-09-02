#!/usr/bin/env python3
"""Enumerate every local K declaration, rule, context, config, and claim."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|alias|"
    r"module|endmodule|imports|requires)\b"
)
ATTRIBUTE_WORDS = [
    "function",
    "functional",
    "total",
    "symbol",
    "opaque",
    "priority",
    "simplification",
    "owise",
    "concrete",
    "macro",
    "strict",
    "seqstrict",
    "depends",
]


def blocks(path: Path) -> list[tuple[str, int, str]]:
    lines = path.read_text().splitlines()
    found: list[tuple[str, int, str]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        text = "\n".join(lines[start:index]).strip()
        found.append((kind, start + 1, text))
    return found


def main() -> int:
    totals: Counter[str] = Counter()
    attrs: Counter[str] = Counter()
    records: list[tuple[str, str, int, str, str]] = []

    for path in FILES:
        rel = path.relative_to(ROOT).as_posix()
        origin = (
            "FIXED_SUPPLIED_SEMANTICS"
            if rel.startswith("reference-semantics/")
            else "CANDIDATE_PROOF_ARTIFACT"
        )
        for kind, line, text in blocks(path):
            totals[kind] += 1
            code_only = "\n".join(part.split("//", 1)[0] for part in text.splitlines())
            tags = [
                word
                for word in ATTRIBUTE_WORDS
                if re.search(rf"\b{word}\b", code_only)
            ]
            attrs.update(tags)
            records.append((origin, rel, line, kind, ",".join(tags) or "-"))
            flat = " ⏎ ".join(part.strip() for part in text.splitlines())
            records[-1] += (flat,)

    print("INVENTORY SUMMARY")
    print(f"files={len(FILES)}")
    print(f"records={len(records)}")
    print("record_counts=" + repr(dict(sorted(totals.items()))))
    print("attribute_counts=" + repr(dict(sorted(attrs.items()))))
    print()
    print("origin\tfile:line\tkind\tattributes\tcomplete_source_block")
    for origin, rel, line, kind, tags, text in records:
        print(f"{origin}\t{rel}:{line}\t{kind}\t{tags}\t{text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
