#!/usr/bin/env python3
"""Emit a line-addressed inventory of every K declaration/rule under audit."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/50-decode-shift/candidate-src")
SEMANTICS = SCRATCH / "reference-semantics"
FILES = sorted(SEMANTICS.rglob("*.k")) + [
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

DECL_START = re.compile(
    r"^\s*(configuration|context|syntax|rule|claim)\b"
)
MODULE_META = re.compile(r"^\s*(module|endmodule|imports)\b")
TOP_REQUIRES = re.compile(r"^requires\b")
ATTRIBUTE = re.compile(r"\[([^\]]+)\]")
KNOWN_ATTRIBUTE = re.compile(
    r"^(?:"
    r"function|functional|total|simplification|concrete|owise|macro|macro-rec|"
    r"no-evaluators|anywhere|"
    r"priority\(\d+\)|symbol\([^)]+\)|strict(?:\([^)]+\))?|"
    r"seqstrict(?:\([^)]+\))?"
    r")$"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


totals: Counter[str] = Counter()
attribute_totals: Counter[str] = Counter()

for path in FILES:
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f"invalid source type: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if DECL_START.match(line)]
    rel = path.relative_to(SCRATCH)

    print("=" * 100)
    print(f"FILE {rel} sha256={digest(path)} lines={len(lines)}")

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if MODULE_META.match(line) or TOP_REQUIRES.match(line):
            print(f"META {rel}:{lineno}: {stripped}")

    for ordinal, start in enumerate(starts):
        end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or MODULE_META.match(block_lines[-1])
        ):
            block_lines.pop()

        first = lines[start].lstrip()
        kind = DECL_START.match(lines[start]).group(1)
        totals[kind] += 1
        joined = "\n".join(block_lines)
        attrs = []
        for group in ATTRIBUTE.findall(joined):
            attrs.extend(
                item.strip()
                for item in group.split(",")
                if KNOWN_ATTRIBUTE.match(item.strip())
            )
        for attr in attrs:
            attribute_totals[attr] += 1

        print(
            f"DECL {kind.upper()} {rel}:{start + 1}"
            + (f" ATTRS={attrs!r}" if attrs else "")
        )
        for offset, source_line in enumerate(block_lines):
            print(f"  {start + offset + 1:4d} | {source_line}")

print("=" * 100)
print("TOTALS")
for key in sorted(totals):
    print(f"{key}={totals[key]}")
print("ATTRIBUTES")
for key in sorted(attribute_totals):
    print(f"{key}={attribute_totals[key]}")
