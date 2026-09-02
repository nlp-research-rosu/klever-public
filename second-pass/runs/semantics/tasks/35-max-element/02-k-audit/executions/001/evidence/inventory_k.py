#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed inventory of local K declarations."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

START = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"configuration|syntax|context|rule|claim|alias|priority"
    r")\b"
)
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "opaque",
    "symbol",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "cell",
)


def declarations(path: Path) -> list[tuple[int, str, str, tuple[str, ...]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str, int]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind"), len(match.group("indent"))))

    result: list[tuple[int, str, str, tuple[str, ...]]] = []
    for offset, (index, kind, indent) in enumerate(starts):
        end = len(lines)
        for next_index, _, next_indent in starts[offset + 1 :]:
            if next_indent <= indent:
                end = next_index
                break
        for terminator in range(index + 1, end):
            if lines[terminator].strip() == "endmodule":
                end = terminator
                break
        block_lines = lines[index:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        normalized = " ".join(line.strip() for line in block_lines)
        attrs = tuple(
            attribute
            for attribute in ATTRIBUTES
            if re.search(rf"\b{re.escape(attribute)}\b", normalized)
        )
        result.append((index + 1, kind, normalized, attrs))
    return result


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} FILE_OR_DIRECTORY ...", file=sys.stderr)
        return 2

    files: list[Path] = []
    for name in sys.argv[1:]:
        path = Path(name)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.k")))
        elif path.suffix == ".k":
            files.append(path)

    files = sorted(dict.fromkeys(files))
    total_counts: collections.Counter[str] = collections.Counter()
    attribute_counts: collections.Counter[str] = collections.Counter()
    file_counts: dict[str, collections.Counter[str]] = {}
    all_rows: list[tuple[str, int, str, str, tuple[str, ...]]] = []

    for path in files:
        counter: collections.Counter[str] = collections.Counter()
        for line, kind, block, attrs in declarations(path):
            counter[kind] += 1
            total_counts[kind] += 1
            attribute_counts.update(attrs)
            all_rows.append((str(path), line, kind, block, attrs))
        file_counts[str(path)] = counter

    print("# Summary by file")
    print("file\tconfiguration\tsyntax\tcontext\trule\tclaim\talias\tpriority\ttotal")
    for path, counter in file_counts.items():
        total = sum(counter.values())
        print(
            f"{path}\t{counter['configuration']}\t{counter['syntax']}\t"
            f"{counter['context']}\t{counter['rule']}\t{counter['claim']}\t"
            f"{counter['alias']}\t{counter['priority']}\t{total}"
        )
    print("# Overall declaration counts")
    print(" ".join(f"{name}={total_counts[name]}" for name in sorted(total_counts)))
    print("# Attribute-bearing declaration counts")
    print(" ".join(f"{name}={attribute_counts[name]}" for name in ATTRIBUTES))
    print("# Exhaustive declaration inventory")
    print("file\tline\tkind\tattributes\tdeclaration")
    for path, line, kind, block, attrs in all_rows:
        print(f"{path}\t{line}\t{kind}\t{','.join(attrs) or '-'}\t{block}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
