#!/usr/bin/env python3
"""Produce a line-addressed inventory of declarations and rules in K sources."""

from __future__ import annotations

import argparse
import collections
import re
from dataclasses import dataclass
from pathlib import Path


START = re.compile(
    r"^(?:(requires|module|endmodule)\b|"
    r"\s*(imports|configuration|syntax|rule|claim|context|alias)\b)"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "no-evaluators",
    "symbol",
    "priority",
    "simplification",
    "concrete",
    "macro",
    "macro-rec",
    "owise",
    "strict",
    "seqstrict",
)


@dataclass
class Item:
    path: Path
    line: int
    kind: str
    text: str
    tags: tuple[str, ...]


def classify(first_line: str, text: str) -> tuple[str, tuple[str, ...]]:
    match = START.match(first_line)
    if match is None:
        raise ValueError(first_line)
    kind = match.group(1) or match.group(2)
    tags = []
    for attribute in ATTRIBUTES:
        if attribute == "priority":
            present = re.search(r"\bpriority\s*\(", text) is not None
        elif attribute == "symbol":
            present = re.search(r"\bsymbol\s*\(", text) is not None
        else:
            present = re.search(rf"\b{re.escape(attribute)}\b", text) is not None
        if present:
            tags.append(attribute)
    if kind == "rule":
        if "<k>" in text or re.search(r"<[A-Za-z][A-Za-z-]*>", text):
            tags.append("operational")
        else:
            tags.append("equational")
    if kind == "syntax" and "no-evaluators" in tags:
        tags.append("opaque")
    return kind, tuple(tags)


def parse_file(path: Path) -> list[Item]:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    items = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        body = lines[start:end]
        while body and (not body[-1].strip() or body[-1].lstrip().startswith("//")):
            body.pop()
        text = "\n".join(body).rstrip()
        kind, tags = classify(lines[start], text)
        items.append(Item(path, start + 1, kind, text, tags))
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--extra", type=Path, nargs="*", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted(args.root.rglob("*.k")) + list(args.extra)
    items = [item for path in paths for item in parse_file(path)]
    kind_counts = collections.Counter(item.kind for item in items)
    tag_counts = collections.Counter(tag for item in items for tag in item.tags)

    lines = [
        "# Exhaustive K source inventory",
        "",
        f"Files: {len(paths)}",
        f"Items: {len(items)}",
        "",
        "## Counts by item kind",
        "",
    ]
    lines.extend(f"- {kind}: {kind_counts[kind]}" for kind in sorted(kind_counts))
    lines.extend(["", "## Counts by classification tag", ""])
    lines.extend(f"- {tag}: {tag_counts[tag]}" for tag in sorted(tag_counts))
    lines.extend(["", "## File inventory", ""])
    for path in paths:
        file_items = [item for item in items if item.path == path]
        try:
            display = path.relative_to(args.root.parent)
        except ValueError:
            display = path
        lines.extend([f"### `{display}`", ""])
        for item in file_items:
            tag_text = ", ".join(item.tags) if item.tags else "none"
            lines.append(
                f"- Line {item.line}; kind `{item.kind}`; tags `{tag_text}`"
            )
            lines.append("")
            lines.append("  ```k")
            lines.extend(f"  {line}" for line in item.text.splitlines())
            lines.append("  ```")
            lines.append("")

    args.output.write_text("\n".join(lines).rstrip() + "\n")
    print(f"files={len(paths)}")
    print(f"items={len(items)}")
    print("kind_counts=" + repr(dict(sorted(kind_counts.items()))))
    print("tag_counts=" + repr(dict(sorted(tag_counts.items()))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
