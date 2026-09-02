#!/usr/bin/env python3
"""Emit a complete anchored inventory of K declarations and sentences."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ANCHOR = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"requires|module|endmodule|imports|syntax|configuration|"
    r"context(?:\s+alias)?|rule|claim"
    r")\b"
)
SIMPLE = {"requires", "module", "endmodule", "imports"}


def entries(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    anchors: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = ANCHOR.match(line)
        if not match:
            continue
        indent = len(match.group("indent"))
        kind = match.group("kind")
        if kind == "requires" and indent != 0:
            continue
        if kind in {"module", "endmodule"} and indent != 0:
            continue
        if kind == "imports" and indent > 2:
            continue
        if kind not in SIMPLE and indent > 2:
            continue
        anchors.append((index, indent, kind))
    for position, (start, indent, kind) in enumerate(anchors):
        stop = start + 1
        if kind not in SIMPLE:
            stop = len(lines)
            for next_start, next_indent, _ in anchors[position + 1 :]:
                if next_indent <= indent:
                    stop = next_start
                    break
        block = lines[start:stop]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        yield start + 1, kind.replace(" ", "_"), "\n".join(block)


def flags(block: str) -> str:
    names = [
        "function",
        "total",
        "functional",
        "macro",
        "simplification",
        "priority",
        "owise",
        "anywhere",
        "concrete",
        "symbol",
        "hook",
        "strict",
        "seqstrict",
    ]
    return ", ".join(name for name in names if re.search(rf"\b{name}\b", block)) or "-"


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} FILE_OR_DIRECTORY [...]", file=sys.stderr)
        return 64
    paths: list[Path] = []
    for argument in sys.argv[1:]:
        path = Path(argument)
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.k")))
        else:
            paths.append(path)
    paths = sorted(dict.fromkeys(path.resolve() for path in paths))
    counts: Counter[str] = Counter()
    all_entries = []
    for path in paths:
        for line, kind, block in entries(path):
            counts[kind] += 1
            all_entries.append((path, line, kind, flags(block), block))

    print("# Exhaustive K source inventory")
    print()
    print(f"Files: {len(paths)}")
    print(f"Anchored entries: {len(all_entries)}")
    print("Counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print()
    for number, (path, line, kind, entry_flags, block) in enumerate(all_entries, 1):
        print(f"## {number}. {path}:{line} — {kind}; attributes: {entry_flags}")
        print()
        print("```k")
        print(block)
        print("```")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
