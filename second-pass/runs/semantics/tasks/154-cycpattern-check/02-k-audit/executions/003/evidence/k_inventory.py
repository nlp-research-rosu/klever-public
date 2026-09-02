#!/usr/bin/env python3
"""Lexical inventory of every local K declaration and rule in audit scope."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
FILES = [ROOT / "reference-semantics" / "semantics.k"]
FILES += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
FILES += [ROOT / "verification.k", ROOT / "spec.k"]

START = re.compile(
    r"^\s*(module|endmodule|imports|requires|configuration|syntax|context|rule|claim)\b"
)
DECLARATION = {"configuration", "syntax", "context", "rule", "claim"}


def strip_line_comment(line: str) -> str:
    return line.split("//", 1)[0].rstrip()


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(strip_line_comment(line))
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        if kind not in DECLARATION:
            continue
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw = lines[start:next_start]
        while raw and not strip_line_comment(raw[-1]).strip():
            raw.pop()
        text = " ".join(
            fragment.strip()
            for fragment in map(strip_line_comment, raw)
            if fragment.strip()
        )
        yield start + 1, kind, text


def tags(text: str) -> str:
    found = []
    for tag in [
        "function",
        "total",
        "functional",
        "symbol(",
        "simplification",
        "priority(",
        "owise",
        "strict",
        "seqstrict",
    ]:
        if tag in text:
            found.append(tag.rstrip("("))
    return ",".join(found) or "-"


def main() -> int:
    totals: collections.Counter[str] = collections.Counter()
    print(f"FILE_COUNT={len(FILES)}")
    for path in FILES:
        relative = path.relative_to(ROOT)
        items = list(blocks(path))
        counts = collections.Counter(kind for _, kind, _ in items)
        totals.update(counts)
        print(
            f"\n===== FILE {relative} "
            + " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
        )
        for line, kind, text in items:
            print(f"{relative}:{line}: {kind.upper()} tags={tags(text)} :: {text}")
    print("\n===== TOTALS")
    for kind in sorted(totals):
        print(f"{kind}={totals[kind]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
