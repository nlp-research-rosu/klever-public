#!/usr/bin/env python3
"""Create a complete declaration/rule/claim inventory for the audited K sources."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re


DECL = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"requires|module|endmodule|imports|configuration|syntax|rule|claim|"
    r"context(?:\s+alias)?|alias"
    r")\b"
)
INTERESTING_ATTRIBUTE = re.compile(
    r"\b("
    r"function|total|functional|simplification|concrete|priority|owise|"
    r"symbol|no-evaluators|strict|seqstrict|macro-rec|macro"
    r")\b"
)


def source_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(root.rglob("*.k"))


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = DECL.match(line)
        if match:
            indent = len(match.group("indent").expandtabs(8))
            kind = match.group("kind")
            if kind in {"requires", "module", "endmodule"} and indent != 0:
                continue
            if kind not in {"requires", "module", "endmodule"} and indent > 2:
                continue
            starts.append((index, indent, kind))
    for position, (start, indent, kind) in enumerate(starts):
        if kind in {"requires", "module", "endmodule", "imports"}:
            end = start + 1
        else:
            end = len(lines)
            for next_start, next_indent, _ in starts[position + 1 :]:
                if next_indent <= indent:
                    end = next_start
                    break
        text_lines = lines[start:end]
        while text_lines and (
            not text_lines[-1].strip() or text_lines[-1].lstrip().startswith("//")
        ):
            text_lines.pop()
        yield start + 1, start + len(text_lines), kind, "\n".join(text_lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    files: list[Path] = []
    for root in args.paths:
        files.extend(source_files(root))
    files = sorted(dict.fromkeys(files))

    counts: Counter[str] = Counter()
    attribute_counts: Counter[str] = Counter()
    file_counts: dict[Path, Counter[str]] = {}
    inventory = []
    for path in files:
        file_counts[path] = Counter()
        for start, end, kind, text in blocks(path):
            counts[kind] += 1
            file_counts[path][kind] += 1
            attrs = INTERESTING_ATTRIBUTE.findall(text)
            for attr in attrs:
                attribute_counts[attr.split("(")[0]] += 1
            inventory.append((path, start, end, kind, attrs, text))

    print("K DECLARATION AND RULE INVENTORY")
    print(f"FILES: {len(files)}")
    print(f"ENTRIES: {len(inventory)}")
    print("KIND_COUNTS:", dict(sorted(counts.items())))
    print("ATTRIBUTE_COUNTS:", dict(sorted(attribute_counts.items())))
    print("PER_FILE_COUNTS:")
    for path in files:
        print(f"  {path}: {dict(sorted(file_counts[path].items()))}")
    print()
    for number, (path, start, end, kind, attrs, text) in enumerate(inventory, 1):
        print(
            f"ENTRY {number:04d} | {path}:{start}-{end} | KIND={kind} | "
            f"ATTRS={attrs}"
        )
        print(text)
        print("END_ENTRY")


if __name__ == "__main__":
    main()
