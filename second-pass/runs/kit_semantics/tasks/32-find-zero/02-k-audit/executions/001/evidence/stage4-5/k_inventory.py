#!/usr/bin/env python3
"""Produce a line-addressed inventory of K declarations and rules."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


START = re.compile(
    r"^(requires|module|endmodule|imports|configuration|syntax|rule|claim|context|alias)\b"
)
FLAGS = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "anywhere",
    "macro",
    "alias",
    "hook",
    "no-evaluators",
    "symbol",
)


def records(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    result: list[dict[str, object]] = []
    current_kind: str | None = None
    current_start = 0
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_kind, current_start, current_lines
        if current_kind is None:
            return
        text = " ".join(part.strip() for part in current_lines if part.strip())
        present_flags = [flag for flag in FLAGS if re.search(rf"\b{re.escape(flag)}\b", text)]
        result.append(
            {
                "file": str(path),
                "line": current_start,
                "kind": current_kind,
                "flags": present_flags,
                "text": text,
            }
        )
        current_kind = None
        current_lines = []

    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        match = START.match(stripped)
        is_top_require = match and match.group(1) == "requires" and line == line.lstrip()
        starts_record = bool(match and (match.group(1) != "requires" or is_top_require))
        if starts_record:
            flush()
            current_kind = match.group(1)
            current_start = number
            current_lines = [line]
        elif current_kind is not None:
            current_lines.append(line)
    flush()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    print("file\tline\tkind\tflags\ttext")
    counts: dict[str, int] = {}
    total = 0
    for path_argument in args.paths:
        files = (
            sorted(path_argument.rglob("*.k"))
            if path_argument.is_dir()
            else [path_argument]
        )
        for path in files:
            for record in records(path):
                total += 1
                key = f"{path}:{record['kind']}"
                counts[key] = counts.get(key, 0) + 1
                fields = (
                    record["file"],
                    record["line"],
                    record["kind"],
                    ",".join(record["flags"]),
                    record["text"],
                )
                print("\t".join(json.dumps(field, ensure_ascii=False) for field in fields))
    print("# SUMMARY " + json.dumps({"records": total, "counts": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
