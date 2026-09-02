#!/usr/bin/env python3
"""Enumerate all K modules, configurations, syntax, contexts, rules, and claims."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


START_RE = re.compile(
    r"^(?P<indent> {0,2})(?P<kind>"
    r"requires|module|endmodule|imports|configuration|syntax|context|rule|claim"
    r")\b"
)


def attributes(block: str, kind: str) -> str:
    flags: list[str] = []
    tests = [
        ("function", r"\bfunction\b"),
        ("functional", r"\bfunctional\b"),
        ("total", r"\btotal\b"),
        ("macro", r"\bmacro\b"),
        ("strict", r"\bstrict(?:ness)?\b"),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification\b"),
        ("concrete", r"\bconcrete\b"),
        ("symbol", r"\bsymbol\s*\("),
        ("no-evaluators", r"\bno-evaluators\b"),
        ("anywhere", r"\banywhere\b"),
    ]
    for label, pattern in tests:
        if re.search(pattern, block):
            flags.append(label)
    if kind == "rule":
        flags.append("operational" if "<k>" in block or "<generatedTop>" in block else "equational")
    return ",".join(flags) if flags else "-"


def inventory(path: Path) -> list[tuple[int, str, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START_RE.match(line)
        if match:
            starts.append((index, match.group("kind")))

    records: list[tuple[int, str, str, str]] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        records.append((start + 1, kind, attributes(block, kind), block))
    return records


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} FILE_OR_DIRECTORY [...]", file=sys.stderr)
        return 64

    files: set[Path] = set()
    for raw_path in sys.argv[1:]:
        path = Path(raw_path)
        if path.is_dir():
            files.update(path.rglob("*.k"))
        elif path.suffix == ".k":
            files.add(path)

    totals: Counter[str] = Counter()
    attr_totals: Counter[str] = Counter()
    all_records: list[tuple[Path, int, str, str, str]] = []
    for path in sorted(files):
        for line, kind, attrs, block in inventory(path):
            totals[kind] += 1
            for flag in attrs.split(","):
                if flag != "-":
                    attr_totals[flag] += 1
            all_records.append((path, line, kind, attrs, block))

    print("INVENTORY_COUNTS")
    for kind in sorted(totals):
        print(f"{kind}\t{totals[kind]}")
    print("ATTRIBUTE_COUNTS")
    for flag in sorted(attr_totals):
        print(f"{flag}\t{attr_totals[flag]}")
    print(f"TOTAL_RECORDS\t{len(all_records)}")

    for number, (path, line, kind, attrs, block) in enumerate(all_records, 1):
        print()
        print(
            f"RECORD {number:04d}\t{path}:{line}\t"
            f"KIND={kind}\tATTRS={attrs}"
        )
        print(block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
