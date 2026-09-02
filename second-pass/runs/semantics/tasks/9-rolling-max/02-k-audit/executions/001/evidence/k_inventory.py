#!/usr/bin/env python3
"""Create a source-located inventory of top-level K declarations and rules."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|alias)\b"
)
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "macro",
    "macro-rec",
    "priority",
    "owise",
    "symbol",
    "strict",
    "seqstrict",
    "token",
    "bracket",
    "assoc",
    "comm",
    "idem",
    "unit",
)


def sources(paths: list[Path]) -> list[Path]:
    result: list[Path] = []
    for path in paths:
        if path.is_dir():
            result.extend(sorted(path.rglob("*.k")))
        else:
            result.append(path)
    return sorted(set(result))


def entries(path: Path) -> list[tuple[int, str, str, list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))

    result: list[tuple[int, str, str, list[str]]] = []
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw = "\n".join(lines[start:stop])
        # Stop snippets at the module boundary if this is the final entry.
        raw = raw.split("\nendmodule", 1)[0]
        normalized = " ".join(
            line.strip()
            for line in raw.splitlines()
            if line.strip() and not line.lstrip().startswith("//")
        )
        attrs = [name for name in ATTRIBUTES if re.search(rf"\b{re.escape(name)}\b", raw)]
        result.append((start + 1, kind, normalized, attrs))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--base", type=Path, required=True)
    args = parser.parse_args()

    kind_counts: collections.Counter[str] = collections.Counter()
    attr_counts: collections.Counter[str] = collections.Counter()
    file_counts: collections.Counter[str] = collections.Counter()
    rows: list[tuple[str, int, str, str, str]] = []

    for path in sources(args.paths):
        relative = str(path.resolve().relative_to(args.base.resolve()))
        for line, kind, statement, attrs in entries(path):
            kind_counts[kind] += 1
            file_counts[relative] += 1
            attr_counts.update(attrs)
            rows.append((relative, line, kind, ",".join(attrs) or "-", statement))

    print("# K source inventory")
    print()
    print(f"Files: {len(file_counts)}")
    print(f"Entries: {len(rows)}")
    print("Kinds: " + ", ".join(f"{key}={kind_counts[key]}" for key in sorted(kind_counts)))
    print("Attributes: " + ", ".join(f"{key}={attr_counts[key]}" for key in sorted(attr_counts)))
    print()
    print("## Counts by file")
    print()
    for path in sorted(file_counts):
        print(f"- `{path}`: {file_counts[path]}")
    print()
    print("## Source-located entries")
    print()
    print("| File | Line | Kind | Attributes | Normalized statement |")
    print("|---|---:|---|---|---|")
    for path, line, kind, attrs, statement in rows:
        escaped = statement.replace("|", r"\|")
        print(f"| `{path}` | {line} | {kind} | {attrs} | `{escaped}` |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
