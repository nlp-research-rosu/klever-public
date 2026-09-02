#!/usr/bin/env python3
"""Emit a complete source-level K declaration inventory with stable IDs."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/hex-key-audit")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(?P<indent> {0,2})(?P<kind>requires|module|imports|syntax|configuration|context|rule|claim|endmodule)\b"
)
INVENTORY_KINDS = {"syntax", "configuration", "context", "rule", "claim"}


def tags(kind: str, block: str, path: Path) -> list[str]:
    code = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
    found: list[str] = []
    for attribute in (
        "function",
        "total",
        "functional",
        "symbol",
        "no-evaluators",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
        "priority",
        "owise",
        "simplification",
        "concrete",
    ):
        if re.search(rf"\b{re.escape(attribute)}\b", code):
            found.append(attribute)
    if kind == "rule":
        if "<k>" in code:
            found.append("operational")
        elif path.name == "verification.k" and "hexKey" in code:
            found.append("source-macro-equation")
        else:
            found.append("equational")
    return found


def main() -> int:
    counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    entries: list[tuple[Path, int, str, str, list[str]]] = []

    for path in SOURCES:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = START.match(line)
            if match and match.group("kind") in INVENTORY_KINDS:
                starts.append((index, match.group("kind")))
        for offset, (start, kind) in enumerate(starts):
            stop = len(lines)
            for line_index in range(start + 1, len(lines)):
                match = START.match(lines[line_index])
                if match:
                    stop = line_index
                    break
            block = "\n".join(lines[start:stop]).rstrip()
            entry_tags = tags(kind, block, path)
            counts[kind] += 1
            tag_counts.update(entry_tags)
            entries.append((path, start + 1, kind, block, entry_tags))

    print("inventory_scope:")
    for path in SOURCES:
        rel = path.relative_to(ROOT)
        print(
            f"  {rel}: bytes={path.stat().st_size} "
            f"sha256={hashlib.sha256(path.read_bytes()).hexdigest()}"
        )
    print(f"source_file_count: {len(SOURCES)}")
    print(f"inventory_entry_count: {len(entries)}")
    print("kind_counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print("tag_counts: " + ", ".join(f"{key}={tag_counts[key]}" for key in sorted(tag_counts)))

    for number, (path, line, kind, block, entry_tags) in enumerate(entries, 1):
        rel = path.relative_to(ROOT)
        stable_id = f"K{number:04d}"
        print()
        print(f"--- {stable_id} {rel}:{line} kind={kind} tags={','.join(entry_tags) or 'none'}")
        print(block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
