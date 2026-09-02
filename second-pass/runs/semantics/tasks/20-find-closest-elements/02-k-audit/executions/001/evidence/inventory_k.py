#!/usr/bin/env python3
"""Produce a line-addressable inventory of K declarations and rules."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(
    r"^\s*(syntax(?:\s+priority|\s+associativity)?|"
    r"configuration|rule|claim|context(?:\s+alias)?)\b"
)
STOP = re.compile(r"^\s*(module|endmodule|imports)\b")


def classify(head: str, text: str) -> str:
    tags: list[str] = []
    if head.startswith("syntax"):
        tags.append("syntax")
        for attr in (
            "function",
            "functional",
            "total",
            "symbol(",
            "no-evaluators",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if attr in text:
                tags.append(attr.rstrip("("))
    elif head == "rule":
        tags.append("rule")
        for attr in ("simplification", "priority(", "concrete", "owise", "macro", "anywhere"):
            if attr in text:
                tags.append(attr.rstrip("("))
        if not any(tag in tags for tag in ("simplification", "priority", "concrete", "owise", "macro", "anywhere")):
            tags.append("ordinary")
    else:
        tags.append(head.replace(" ", "-"))
    return ",".join(tags)


def statements(path: Path) -> list[tuple[int, int, str, str]]:
    lines = path.read_text().splitlines()
    found: list[tuple[int, int, str, str]] = []
    current_start: int | None = None
    current_head = ""
    current_lines: list[str] = []

    def flush(end_line: int) -> None:
        nonlocal current_start, current_head, current_lines
        if current_start is None:
            return
        text = " ".join(
            part.strip() for part in current_lines if part.strip() and not part.lstrip().startswith("//")
        )
        text = re.sub(r"\s+", " ", text)
        found.append((current_start, end_line, classify(current_head, text), text))
        current_start = None
        current_head = ""
        current_lines = []

    for number, line in enumerate(lines, start=1):
        match = START.match(line)
        if match:
            flush(number - 1)
            current_start = number
            current_head = match.group(1)
            current_lines = [line]
        elif STOP.match(line):
            flush(number - 1)
        elif current_start is not None:
            current_lines.append(line)
    flush(len(lines))
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    rows: list[tuple[str, int, int, str, str]] = []
    for path in sorted(args.paths):
        for start, end, kind, text in statements(path):
            rows.append((str(path.relative_to(args.root)), start, end, kind, text))

    with args.output.open("w") as out:
        out.write("file\tstart_line\tend_line\tclassification\tstatement\n")
        for row in rows:
            escaped = [str(value).replace("\t", "\\t").replace("\n", "\\n") for value in row]
            out.write("\t".join(escaped) + "\n")

    print(f"inventory_rows={len(rows)}")
    counts: dict[str, int] = {}
    for _, _, _, classification, _ in rows:
        for tag in classification.split(","):
            counts[tag] = counts.get(tag, 0) + 1
    for tag in sorted(counts):
        print(f"{tag}={counts[tag]}")
    print(f"output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
