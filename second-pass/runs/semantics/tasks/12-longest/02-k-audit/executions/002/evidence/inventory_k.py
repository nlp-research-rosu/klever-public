#!/usr/bin/env python3
"""Produce a line-addressable inventory of K declarations and rules."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys


START = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"configuration|syntax|rule|claim|context alias|context"
    r")\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:configuration|syntax|rule|claim|context alias|context|"
    r"module|endmodule|imports|requires)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "macro",
    "macro-rec",
    "simplification",
    "priority",
    "owise",
    "anywhere",
    "no-evaluators",
    "symbol",
    "hook",
)


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for start_number, start in enumerate(starts):
        end = starts[start_number + 1] if start_number + 1 < len(starts) else len(lines)
        # Do not absorb an intervening module/import boundary at file end.
        for candidate in range(start + 1, end):
            if BOUNDARY.match(lines[candidate]):
                end = candidate
                break
        text = "\n".join(lines[start:end]).strip()
        match = START.match(lines[start])
        assert match is not None
        yield start + 1, match.group("kind"), text


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: inventory_k.py K-FILE-OR-DIRECTORY ...", file=sys.stderr)
        return 2
    files: set[Path] = set()
    for raw_path in sys.argv[1:]:
        path = Path(raw_path)
        if path.is_dir():
            files.update(path.rglob("*.k"))
        elif path.suffix == ".k":
            files.add(path)
        else:
            raise ValueError(f"not a K source: {path}")

    kind_counts: Counter[str] = Counter()
    file_counts: Counter[str] = Counter()
    attr_counts: Counter[str] = Counter()
    rows: list[tuple[str, int, str, str, str]] = []
    for path in sorted(files):
        display_path = str(path)
        for line, kind, text in blocks(path):
            normalized = " ".join(text.split())
            present = [
                attribute
                for attribute in ATTRIBUTES
                if re.search(rf"\b{re.escape(attribute)}\b", text)
            ]
            rows.append(
                (display_path, line, kind, ",".join(present) or "-", normalized)
            )
            kind_counts[kind] += 1
            file_counts[display_path] += 1
            attr_counts.update(present)

    print(
        "# SUMMARY total="
        + str(len(rows))
        + " kinds="
        + ",".join(f"{key}:{kind_counts[key]}" for key in sorted(kind_counts))
    )
    print(
        "# ATTRIBUTES "
        + ",".join(f"{key}:{attr_counts[key]}" for key in sorted(attr_counts))
    )
    for path in sorted(file_counts):
        print(f"# FILE {path} entries={file_counts[path]}")
    print("id\tfile\tline\tkind\tattributes\tdeclaration_or_rule")
    for identifier, (path, line, kind, attributes, text) in enumerate(rows, start=1):
        print(f"{identifier}\t{path}\t{line}\t{kind}\t{attributes}\t{text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
