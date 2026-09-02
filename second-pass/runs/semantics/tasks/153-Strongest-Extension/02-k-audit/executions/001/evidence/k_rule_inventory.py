#!/usr/bin/env python3
"""Lexical inventory of every K declaration/rule in the audited source tree."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/tmp/audit-work/reconstruction")
sources = sorted((ROOT / "reference-semantics").rglob("*.k"))
sources += [ROOT / "verification.k", ROOT / "spec.k"]

start_kinds = [
    ("REQUIRES", re.compile(r"^requires\b")),
    ("MODULE", re.compile(r"^module\b")),
    ("ENDMODULE", re.compile(r"^endmodule\b")),
    ("IMPORTS", re.compile(r"^imports\b")),
    ("CONFIGURATION", re.compile(r"^configuration\b")),
    ("SYNTAX", re.compile(r"^syntax\b")),
    ("RULE", re.compile(r"^rule\b")),
    ("CLAIM", re.compile(r"^claim\b")),
    ("CONTEXT", re.compile(r"^context\b")),
    ("ALIAS", re.compile(r"^alias\b")),
]
attribute_words = re.compile(
    r"\b(function|total|functional|simplification|priority|concrete|owise|symbol)\b"
)

totals = Counter()
per_file: dict[str, Counter[str]] = defaultdict(Counter)
records: list[tuple[str, int, str, str, str]] = []

for source in sources:
    relative = str(source.relative_to(ROOT))
    lines = source.read_text().splitlines()
    in_syntax = False
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        code = stripped.split("//", 1)[0].rstrip()
        if not code:
            in_syntax = False
            continue

        kind = None
        for candidate, pattern in start_kinds:
            if pattern.match(code):
                kind = candidate
                break

        if kind == "SYNTAX":
            in_syntax = True
        elif in_syntax and code.startswith("|"):
            kind = "SYNTAX_ALT"
        elif kind is not None:
            in_syntax = False

        attrs = ",".join(sorted(set(attribute_words.findall(code))))
        if kind is not None:
            totals[kind] += 1
            per_file[relative][kind] += 1
            records.append((relative, number, kind, attrs, stripped))
        elif attrs:
            totals["ATTRIBUTE_LINE"] += 1
            per_file[relative]["ATTRIBUTE_LINE"] += 1
            records.append((relative, number, "ATTRIBUTE_LINE", attrs, stripped))

print("# Exhaustive lexical K declaration and rule inventory")
print()
print(
    "Each source line beginning a K declaration/rule is listed. Continued "
    "syntax alternatives and separate attribute lines are listed explicitly."
)
print()
print("## Totals")
print()
for kind, count in sorted(totals.items()):
    print(f"- {kind}: {count}")
print()
print("## Per-file counts")
print()
for relative in sorted(per_file):
    counts = ", ".join(
        f"{kind}={count}" for kind, count in sorted(per_file[relative].items())
    )
    print(f"- `{relative}`: {counts}")
print()
print("## Records")
print()
print("| File:line | Kind | Attributes | Source |")
print("|---|---|---|---|")
for relative, number, kind, attrs, source_line in records:
    escaped = source_line.replace("|", "\\|").replace("`", "\\`")
    print(f"| `{relative}:{number}` | {kind} | {attrs or '-'} | `{escaped}` |")
