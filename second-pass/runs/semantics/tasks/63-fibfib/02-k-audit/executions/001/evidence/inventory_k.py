#!/usr/bin/env python3
"""Emit a complete, line-addressed inventory of local K declarations."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


START = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|alias)\b"
)
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)\b")
END_MODULE = re.compile(r"^\s*endmodule\b")
ATTR = re.compile(r"\[([^\]]+)\]")
ATTRIBUTE_WORDS = re.compile(
    r"\b(function|functional|total|simplification|concrete|priority|owise|"
    r"macro|macro-rec|symbol|no-evaluators|strict|seqstrict|heat|cool|"
    r"assoc|comm|unit|idem|hook|format|binder|left|right|non-assoc)\b"
)


def normalize(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    return re.sub(r"\s+", " ", text).strip()


def classify(kind: str, text: str, attrs: str) -> str:
    if kind == "rule":
        if "simplification" in attrs:
            return "simplification_rule"
        if "priority(" in attrs:
            return "priority_rule"
        if "macro" in attrs:
            return "macro_rule"
        return "ordinary_rule"
    if kind == "syntax":
        if "symbol(" in attrs and "no-evaluators" in attrs:
            return "opaque_symbol_declaration"
        if "function" in attrs or "functional" in attrs:
            return "function_declaration"
        if "macro" in attrs:
            return "macro_declaration"
        return "syntax_declaration"
    return kind


def records(path: Path, display_root: Path) -> list[dict[str, str | int]]:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    module_for_line: list[str] = []
    module = ""
    for line in lines:
        match = MODULE.match(line)
        if match:
            module = match.group(1)
        module_for_line.append(module)
        if END_MODULE.match(line):
            module = ""

    output: list[dict[str, str | int]] = []
    for ordinal, index in enumerate(starts):
        next_index = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        stop = next_index
        for candidate in range(index + 1, next_index):
            if END_MODULE.match(lines[candidate]) or MODULE.match(lines[candidate]):
                stop = candidate
                break
        block = lines[index:stop]
        text = normalize(block)
        kind = START.match(lines[index]).group(1)  # type: ignore[union-attr]
        attrs = ",".join(
            match.group(1)
            for match in ATTR.finditer(text)
            if ATTRIBUTE_WORDS.search(match.group(1))
        )
        output.append(
            {
                "file": path.relative_to(display_root).as_posix(),
                "line": index + 1,
                "module": module_for_line[index],
                "kind": kind,
                "class": classify(kind, text, attrs),
                "attributes": attrs,
                "total": "yes" if re.search(r"\btotal\b", attrs) else "no",
                "functional": (
                    "yes"
                    if re.search(r"\b(function|functional)\b", attrs)
                    else "no"
                ),
                "text": text,
            }
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("extra", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    paths = sorted(args.root.rglob("*.k")) + [args.extra]
    rows: list[dict[str, str | int]] = []
    for path in paths:
        display_root = args.root.parent
        if path == args.extra:
            display_root = args.extra.parent
        rows.extend(records(path, display_root))

    fields = [
        "id",
        "file",
        "line",
        "module",
        "kind",
        "class",
        "attributes",
        "total",
        "functional",
        "text",
    ]
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, dialect="excel-tab")
        writer.writeheader()
        for row_id, row in enumerate(rows, 1):
            writer.writerow({"id": row_id, **row})

    classes: dict[str, int] = {}
    for row in rows:
        row_class = str(row["class"])
        classes[row_class] = classes.get(row_class, 0) + 1
    print(f"files={len(paths)}")
    print(f"inventory_rows={len(rows)}")
    for row_class, count in sorted(classes.items()):
        print(f"{row_class}={count}")
    print(f"output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
