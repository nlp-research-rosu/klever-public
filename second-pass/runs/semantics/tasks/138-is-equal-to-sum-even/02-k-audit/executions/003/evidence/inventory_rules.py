#!/usr/bin/env python3
"""Emit a source-located inventory of all K declarations, contexts, rules, and claims."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(r"^  (configuration|syntax|rule|context|claim)\b")
ATTRIBUTES = [
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "symbol",
    "no-evaluators",
]


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [(index, START.match(line).group(1)) for index, line in enumerate(lines) if START.match(line)]
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:stop]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        meaningful = [
            line.strip()
            for line in block_lines
            if line.strip() and not line.lstrip().startswith("//")
        ]
        yield start + 1, kind.upper(), " ".join(meaningful)


def main() -> int:
    records = []
    for path in ROOTS:
        if not path.is_file() or path.is_symlink():
            print(f"invalid inventory input: {path}", file=sys.stderr)
            return 1
        for line, kind, text in blocks(path):
            attrs = [attribute for attribute in ATTRIBUTES if re.search(rf"\b{re.escape(attribute)}\b", text)]
            records.append(
                (
                    str(path),
                    line,
                    kind,
                    ",".join(attrs) if attrs else "-",
                    text.replace("\t", " "),
                )
            )

    counts = Counter(record[2] for record in records)
    attr_counts = Counter(
        attribute
        for record in records
        for attribute in ([] if record[3] == "-" else record[3].split(","))
    )
    print("# Exhaustive K source inventory")
    print("# Inputs:")
    for path in ROOTS:
        print(f"#   {path}")
    print(f"# TOTAL_RECORDS={len(records)}")
    print("# KIND_COUNTS=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)))
    print("# ATTRIBUTE_COUNTS=" + ",".join(f"{key}:{attr_counts[key]}" for key in sorted(attr_counts)))
    print("id\tfile\tline\tkind\tattributes\tdeclaration_or_rule")
    for index, record in enumerate(records, 1):
        print(index, *record, sep="\t")
    return 0


if __name__ == "__main__":
    sys.exit(main())
