#!/usr/bin/env python3
"""Create an exhaustive declaration/rule inventory for the audited K theory."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


START = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|macro|alias)\b"
)
MODULE = re.compile(r'^\s*(module|endmodule|imports\b|requires\s+")')


def blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[int, str, str]] = []
    for position, (index, kind) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_index
        for candidate in range(index + 1, next_index):
            if re.match(r"^\s*endmodule\b", lines[candidate]):
                end = candidate
                break
        text = "\n".join(lines[index:end]).rstrip()
        result.append((index + 1, kind, text))
    return result


def classify(kind: str, text: str) -> list[str]:
    code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    flags: list[str] = []
    if kind == "rule":
        flags.append("operational" if "<k>" in code else "equational")
    for flag in [
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "simplify",
        "concrete",
        "owise",
        "macro",
        "strict",
        "seqstrict",
    ]:
        if re.search(rf"\b{re.escape(flag)}\b", code):
            flags.append(flag)
    return flags


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    files: list[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.k")))
        else:
            files.append(path)
    files = sorted(dict.fromkeys(files))

    totals: collections.Counter[str] = collections.Counter()
    flag_totals: collections.Counter[str] = collections.Counter()
    inventory: list[tuple[Path, int, str, list[str], str]] = []
    for path in files:
        for line, kind, text in blocks(path):
            flags = classify(kind, text)
            totals[kind] += 1
            flag_totals.update(flags)
            inventory.append((path, line, kind, flags, one_line(text)))

    print(f"file_count={len(files)}")
    print(f"declaration_count={len(inventory)}")
    print(f"kind_counts={dict(sorted(totals.items()))}")
    print(f"flag_counts={dict(sorted(flag_totals.items()))}")
    for path in files:
        module_lines = [
            f"{number}:{line.strip()}"
            for number, line in enumerate(path.read_text().splitlines(), start=1)
            if MODULE.match(line)
        ]
        print(f"FILE {path}")
        for line in module_lines:
            print(f"  MODULE_EDGE {line}")
        for inventory_path, line, kind, flags, text in inventory:
            if inventory_path == path:
                print(
                    f"  ENTRY line={line} kind={kind} "
                    f"flags={','.join(flags) if flags else '-'} :: {text}"
                )


if __name__ == "__main__":
    main()
