#!/usr/bin/env python3
"""Inventory every declaration in the supplied MPY sources and local proof."""

from __future__ import annotations

import re
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|"
    r"syntax|context(?:\s+alias)?|rule|claim|alias|macro)\b"
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        first = START.match(lines[start])
        assert first is not None
        kind = first.group(1)
        # Comments and blank lines immediately before the next declaration are
        # not part of this declaration.
        content = lines[start:end]
        while content and (not content[-1].strip() or content[-1].lstrip().startswith("//")):
            content.pop()
        normalized = " ".join(line.strip() for line in content)
        attrs = [
            attr
            for attr in (
                "function",
                "functional",
                "total",
                "symbol(",
                "no-evaluators",
                "priority(",
                "simplification",
                "concrete",
                "symbolic(",
                "owise",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
                "heat",
                "cool",
                "preserves-definedness",
            )
            if attr in normalized
        ]
        yield start + 1, kind, ",".join(attrs) or "-", normalized


count = 0
by_file: dict[str, dict[str, int]] = {}
print("file\tline\tkind\tattributes\tdeclaration")
for path in ROOTS:
    file_counts: dict[str, int] = {}
    for line, kind, attrs, declaration in blocks(path):
        print(f"{path}\t{line}\t{kind}\t{attrs}\t{declaration}")
        count += 1
        file_counts[kind] = file_counts.get(kind, 0) + 1
    by_file[str(path)] = file_counts

print(f"TOTAL_DECLARATIONS\t{count}")
for path, counts in by_file.items():
    print(f"COUNTS\t{path}\t{counts}")
