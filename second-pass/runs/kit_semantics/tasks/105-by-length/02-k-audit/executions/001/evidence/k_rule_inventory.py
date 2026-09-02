#!/usr/bin/env python3
"""Exhaustive source-level declaration inventory for the audited K theory."""

from __future__ import annotations

from collections import Counter
import hashlib
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/reconstruction")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k"
]
START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|"
    r"syntax(?:\s+priority)?|context|rule|claim)\b"
)
INVENTORY_KINDS = {"configuration", "syntax", "syntax priority", "context", "rule", "claim"}
FLAGS = [
    "function",
    "functional",
    "total",
    "macro",
    "macro-rec",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
]


def kind_of(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("syntax priority"):
        return "syntax priority"
    return stripped.split(maxsplit=1)[0]


def normalize(lines: list[str]) -> str:
    pieces = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("//"):
            continue
        pieces.append(text)
    return " ".join(pieces)


def main() -> int:
    counts: Counter[str] = Counter()
    flag_counts: Counter[str] = Counter()
    source_bytes = 0
    print("# Exhaustive K declaration inventory")
    print()
    print(f"Root: `{ROOT}`")
    print()
    for path in SOURCES:
        raw = path.read_bytes()
        source_bytes += len(raw)
        lines = raw.decode(errors="strict").splitlines()
        starts = [index for index, line in enumerate(lines) if START.match(line)]
        relative = path.relative_to(ROOT).as_posix()
        print(f"## {relative}")
        print()
        print(f"SHA256: `{hashlib.sha256(raw).hexdigest()}`; bytes: {len(raw)}")
        print()
        for position, start in enumerate(starts):
            line = lines[start]
            kind = kind_of(line)
            if kind not in INVENTORY_KINDS:
                continue
            stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
            block = lines[start:stop]
            text = normalize(block)
            counts[kind] += 1
            present_flags = [flag for flag in FLAGS if re.search(rf"\b{re.escape(flag)}\b", text)]
            for flag in present_flags:
                flag_counts[flag] += 1
            flag_text = f" flags={','.join(present_flags)}" if present_flags else ""
            print(f"- `{relative}:{start + 1}` **{kind}**{flag_text}: `{text}`")
        print()
    print("## Counts")
    print()
    print(f"- Source files: {len(SOURCES)}")
    print(f"- Source bytes read: {source_bytes}")
    for key, count in sorted(counts.items()):
        print(f"- {key}: {count}")
    for key, count in sorted(flag_counts.items()):
        print(f"- flag `{key}`: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
