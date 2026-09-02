#!/usr/bin/env python3
"""Enumerate K declarations and rules for the independent proof audit."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
STOP = re.compile(r"^\s*(module|endmodule|imports)\b")


def source_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(path.rglob("*.k"))
        else:
            files.append(path)
    return sorted(set(files), key=str)


def blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[tuple[int, str, str]] = []
    current: list[str] = []
    current_line = 0
    current_kind = ""

    def finish() -> None:
        nonlocal current, current_line, current_kind
        if current:
            text = " ".join(part.strip() for part in current if part.strip())
            out.append((current_line, current_kind, re.sub(r"\s+", " ", text)))
        current = []
        current_line = 0
        current_kind = ""

    for number, line in enumerate(lines, 1):
        start = START.match(line)
        if start:
            finish()
            current = [line]
            current_line = number
            current_kind = start.group(1)
            continue
        if current:
            if STOP.match(line):
                finish()
            elif line.lstrip().startswith("//"):
                continue
            else:
                current.append(line)
    finish()
    return out


def flags(kind: str, text: str) -> list[str]:
    found: list[str] = []
    candidates = [
        "function",
        "functional",
        "total",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
        "concrete",
        "owise",
        "simplification",
        "no-evaluators",
    ]
    for candidate in candidates:
        if candidate in text:
            found.append(candidate)
    if "priority(" in text:
        match = re.search(r"priority\(([^)]+)\)", text)
        found.append(f"priority({match.group(1) if match else '?'})")
    if "symbol(" in text:
        match = re.search(r"symbol\(([^)]+)\)", text)
        found.append(f"symbol({match.group(1) if match else '?'})")
    if kind == "rule":
        found.append("operational" if "<k>" in text else "equational")
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    total = Counter()
    flag_counts = Counter()
    inventory: list[tuple[Path, int, str, list[str], str]] = []
    for path in source_files(args.paths):
        for line, kind, text in blocks(path):
            item_flags = flags(kind, text)
            total[kind] += 1
            flag_counts.update(item_flags)
            inventory.append((path, line, kind, item_flags, text))

    print(f"files={len(source_files(args.paths))}")
    print(f"declaration_counts={dict(sorted(total.items()))}")
    print(f"attribute_and_class_counts={dict(sorted(flag_counts.items()))}")
    print("inventory:")
    for path, line, kind, item_flags, text in inventory:
        rendered_flags = ",".join(item_flags) if item_flags else "-"
        print(f"{path}:{line}: {kind} [{rendered_flags}] {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
