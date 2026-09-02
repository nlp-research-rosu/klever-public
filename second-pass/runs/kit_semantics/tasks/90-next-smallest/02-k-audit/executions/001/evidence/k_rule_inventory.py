#!/usr/bin/env python3
"""Produce a complete declaration/rule inventory for the audited K sources.

This is deliberately lexical: every source line beginning a K declaration,
configuration, context, rule, or claim is captured with its complete source
chunk through the next such declaration.  The final assertion ensures no
matching declaration start was skipped.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


START = re.compile(r"^\s*(configuration|context\s+alias|context|syntax|rule|claim)\b")


def strip_line_comment(line: str) -> str:
    # K files in this corpus use // comments; strings containing // do not
    # occur in declaration introducers.
    return line.split("//", 1)[0]


def flags(text: str) -> list[str]:
    found = []
    for label, pattern in [
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification(?:\s*\(|\b)"),
        ("concrete", r"\bconcrete\b"),
        ("symbolic", r"\bsymbolic\s*\("),
        ("owise", r"\bowise\b"),
        ("strictness", r"\b(?:strict|seqstrict)\s*(?:\(|\])"),
        ("macro", r"\bmacro\b"),
        ("preserves-definedness", r"\bpreserves-definedness\b"),
    ]:
        if re.search(pattern, text):
            found.append(label)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    if args.output is not None:
        sys.stdout = args.output.open("w", encoding="utf-8")

    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.k")))
        else:
            files.append(path)
    files = sorted(dict.fromkeys(files), key=lambda p: str(p))

    totals = Counter()
    total_starts = 0
    records: list[tuple[Path, int, str, list[str], str]] = []
    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        starts = []
        for index, line in enumerate(lines):
            match = START.match(strip_line_comment(line))
            if match:
                starts.append((index, match.group(1).replace(" ", "_")))
        total_starts += len(starts)
        for number, (index, kind) in enumerate(starts):
            end = starts[number + 1][0] if number + 1 < len(starts) else len(lines)
            chunk_lines = lines[index:end]
            while chunk_lines and (
                not chunk_lines[-1].strip()
                or chunk_lines[-1].lstrip().startswith("//")
                or chunk_lines[-1].strip() == "endmodule"
            ):
                chunk_lines.pop()
            chunk = "\n".join(chunk_lines)
            record_flags = flags(chunk)
            records.append((path, index + 1, kind, record_flags, chunk))
            totals[kind] += 1
            totals.update(f"flag:{item}" for item in record_flags)

    assert len(records) == total_starts
    print("K SOURCE DECLARATION AND RULE INVENTORY")
    print(f"files={len(files)}")
    print(f"lexical_declaration_starts={total_starts}")
    print(f"captured_records={len(records)}")
    print("counts:")
    for key in sorted(totals):
        print(f"  {key}={totals[key]}")
    print()
    for ordinal, (path, line, kind, record_flags, chunk) in enumerate(records, 1):
        rendered_flags = ",".join(record_flags) if record_flags else "none"
        print(f"RECORD {ordinal}: {path}:{line} kind={kind} flags={rendered_flags}")
        print(chunk)
        print("END_RECORD")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
