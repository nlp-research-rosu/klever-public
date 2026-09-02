#!/usr/bin/env python3
"""Mechanical inventory of every K declaration in the supplied and local theory."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


roots = [
    ("supplied", Path("/reference/reference-semantics")),
    ("proof-local", Path("/candidate")),
]
local_names = {
    "verification.k",
    "spec.k",
    "connection-verification.k",
    "connection-spec.k",
}
start_re = re.compile(
    r"^(requires)\b"
    r"|^\s*(module|imports|syntax|configuration|context|rule|claim|endmodule)\b"
)
attribute_names = (
    "function",
    "functional",
    "total",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "priority",
    "owise",
    "simplification",
    "concrete",
    "symbol",
    "no-evaluators",
)

records: list[tuple[str, str, int, str, str, list[str]]] = []
for origin, root in roots:
    paths = sorted(root.rglob("*.k"))
    if origin == "proof-local":
        paths = [path for path in paths if path.name in local_names and path.parent == root]
    for path in paths:
        lines = path.read_text().splitlines()
        starts = [
            index
            for index, line in enumerate(lines)
            if start_re.match(line) and not line.lstrip().startswith("//")
        ]
        for position, start in enumerate(starts):
            end = starts[position + 1] if position + 1 < len(starts) else len(lines)
            first = start_re.match(lines[start])
            assert first is not None
            kind = first.group(1) or first.group(2)
            block_lines = lines[start:end]
            while block_lines and (
                not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
            ):
                block_lines.pop()
            flattened = " ".join(
                piece.strip()
                for line in block_lines
                for piece in [line]
                if piece.strip() and not piece.lstrip().startswith("//")
            )
            attrs = [
                name
                for name in attribute_names
                if re.search(rf"(?<![A-Za-z-]){re.escape(name)}(?:\(|\b)", flattened)
            ]
            records.append(
                (
                    origin,
                    str(path),
                    start + 1,
                    kind,
                    flattened.replace("|", "\\|"),
                    attrs,
                )
            )

kind_counts = Counter(record[3] for record in records)
origin_counts = Counter(record[0] for record in records)
attribute_counts = Counter(attr for record in records for attr in record[5])

print("# Mechanical K declaration and rule inventory")
print()
print("COMMAND: `python3 /audit-output/evidence/05_rule_inventory.py > "
      "/audit-output/evidence/05_rule_inventory.md`")
print()
print("This inventories every declaration start in all 25 supplied `.k` files and")
print("the four candidate source theory/spec files; compiled definitions are excluded.")
print()
print("## Counts")
print()
print(f"- Total records: {len(records)}")
print(f"- Origins: {dict(sorted(origin_counts.items()))}")
print(f"- Kinds: {dict(sorted(kind_counts.items()))}")
print(f"- Attributes: {dict(sorted(attribute_counts.items()))}")
print()
print("## Records")
print()
print("| Origin | File:line | Kind | Attributes | Complete declaration block |")
print("|---|---|---|---|---|")
for origin, path, line, kind, block, attrs in records:
    print(
        f"| {origin} | `{path}:{line}` | {kind} | "
        f"{', '.join(attrs) if attrs else '—'} | `{block}` |"
    )
print()
print("SCRIPT_EXIT=0")
