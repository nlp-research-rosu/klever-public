#!/usr/bin/env python3
"""Emit an exhaustive, source-located inventory of K declarations and rules."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ANCHOR = re.compile(
    r'^\s*(requires(?=\s+")|module|endmodule|imports|syntax|configuration|rule|'
    r"claim|context(?:\s+alias)?|alias)\b"
)


def compact(text: str) -> str:
    return " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    )


def classes(kind: str, text: str) -> list[str]:
    found: list[str] = []
    if kind == "syntax":
        found.append("syntax")
    elif kind == "rule":
        found.append("semantic-rule")
    elif kind == "claim":
        found.append("reachability-claim")
    elif kind.startswith("context"):
        found.append("evaluation-context")
    elif kind == "configuration":
        found.append("configuration")
    else:
        found.append(kind)

    attributes = {
        "function": r"\bfunction\b",
        "functional": r"\bfunctional\b",
        "total": r"\btotal\b",
        "simplification": r"\bsimplification\b",
        "priority": r"\bpriority\s*\(",
        "owise": r"\bowise\b",
        "anywhere": r"\banywhere\b",
        "macro": r"\bmacro(?:-rec)?\b",
        "concrete-only": r"\bconcrete\b",
        "opaque/no-evaluators": r"\bno-evaluators\b",
        "symbol": r"\bsymbol\s*\(",
    }
    for label, pattern in attributes.items():
        if re.search(pattern, text):
            found.append(label)
    return found


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    anchors: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = ANCHOR.match(line)
        if match:
            anchors.append((index, match.group(1)))
    for position, (start, kind) in enumerate(anchors):
        end = anchors[position + 1][0] if position + 1 < len(anchors) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        yield start + 1, start + len(block_lines), kind, "\n".join(block_lines)


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: inventory_k.py K_FILE_OR_DIRECTORY [...]")

    paths: list[Path] = []
    for raw in sys.argv[1:]:
        path = Path(raw)
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.k")))
        elif path.suffix == ".k":
            paths.append(path)
    paths = sorted(dict.fromkeys(path.resolve() for path in paths))

    class_counts: Counter[str] = Counter()
    file_counts: Counter[str] = Counter()
    records = []
    for path in paths:
        for start, end, kind, text in declarations(path):
            labels = classes(kind, text)
            class_counts.update(labels)
            file_counts[str(path)] += 1
            records.append((path, start, end, kind, labels, compact(text)))

    print("# Exhaustive K declaration and rule inventory")
    print()
    print("Generated directly from the audited source snapshot. Each entry is one")
    print("top-level K declaration, configuration, context, rule, or claim.")
    print()
    print(f"Files: {len(paths)}")
    print(f"Inventory entries: {len(records)}")
    print()
    print("## Classification totals")
    print()
    for label, count in sorted(class_counts.items()):
        print(f"- {label}: {count}")
    print()
    print("## Per-file totals")
    print()
    for path, count in sorted(file_counts.items()):
        print(f"- `{path}`: {count}")
    print()
    print("## Entries")
    print()
    for number, (path, start, end, kind, labels, text) in enumerate(records, 1):
        location = f"{path}:{start}" if start == end else f"{path}:{start}-{end}"
        print(
            f"{number:04d}. `{location}` — kind=`{kind}`; "
            f"classes=`{','.join(labels)}` — {text}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
