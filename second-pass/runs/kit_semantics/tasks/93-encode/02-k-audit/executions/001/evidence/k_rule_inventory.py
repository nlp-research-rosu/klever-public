#!/usr/bin/env python3
"""Exhaustive source-level inventory of K declarations, contexts, rules, and claims."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
FILES = sorted(SEMANTICS_ROOT.rglob("*.k"))
FILES.extend([Path("/candidate/verification.k"), Path("/candidate/spec.k")])

START = re.compile(
    r"^(?:requires|module|endmodule)\b|^  (?:imports|syntax|rule|context|configuration|claim)\b"
)
KIND = re.compile(
    r"^\s*(requires|module|endmodule|imports|syntax|rule|context|configuration|claim)\b"
)
ATTRIBUTE_NAMES = [
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "symbol",
    "no-evaluators",
]


def normalized(block: list[str]) -> str:
    content = []
    for line in block:
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if "//" in stripped:
            stripped = stripped.split("//", 1)[0].rstrip()
        if stripped:
            content.append(stripped)
    return " ".join(content)


counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
classification_counts: Counter[str] = Counter()
opaque_declarations: list[tuple[Path, int, str]] = []
records: list[str] = []

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[start]
        match = KIND.match(first)
        assert match is not None, (path, start + 1, first)
        kind = match.group(1)
        block_text = normalized(lines[start:end])
        counts[kind] += 1
        attrs = [name for name in ATTRIBUTE_NAMES if re.search(rf"\b{re.escape(name)}\b", block_text)]
        for attr in attrs:
            attribute_counts[attr] += 1
        classification = kind
        if kind == "rule":
            classification = "operational-rule" if "<k>" in block_text else "equational-rule"
            if "macro" in block_text:
                classification = "macro-rule"
            elif "concrete" in attrs:
                classification += "+concrete"
            if "priority" in attrs:
                classification += "+priority"
            if "owise" in attrs:
                classification += "+owise"
        elif kind == "syntax":
            classification = "syntax-declaration"
            if "function" in attrs:
                classification += "+function"
            if "total" in attrs:
                classification += "+total"
            if "functional" in attrs:
                classification += "+functional"
            if "no-evaluators" in attrs:
                classification += "+opaque"
                opaque_declarations.append((path, start + 1, block_text))
            if "macro" in attrs or "macro-rec" in attrs:
                classification += "+macro"
        records.append(
            f"{path}:{start + 1}\t{classification}\tattrs={','.join(attrs) or '-'}\t{block_text}"
        )
        classification_counts[classification] += 1

print("FILES")
for path in FILES:
    print(f"{path}\tsha256_pending_in_01-provenance-or-source-tree")
print()
print("COUNTS")
for key, value in sorted(counts.items()):
    print(f"{key}={value}")
for key, value in sorted(classification_counts.items()):
    print(f"classification:{key}={value}")
for key in ATTRIBUTE_NAMES:
    print(f"attribute:{key}={attribute_counts[key]}")
print(f"opaque_declaration_count={len(opaque_declarations)}")
print()
print("OPAQUE_DECLARATIONS")
for path, line, declaration in opaque_declarations:
    print(f"{path}:{line}\t{declaration}")
print()
print("EXHAUSTIVE_RECORDS")
for record in records:
    print(record)
