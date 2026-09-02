#!/usr/bin/env python3
"""Emit a line-addressed exhaustive inventory of candidate-visible K constructs."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/28-concatenate")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
STARTERS = (
    "requires ",
    "module ",
    "imports ",
    "configuration",
    "syntax ",
    "context ",
    "rule ",
    "claim",
    "endmodule",
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "simplification",
    "simplifier",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "no-evaluators",
    "symbol",
    "strict",
    "seqstrict",
)


def starts_record(line: str) -> bool:
    stripped = line.strip()
    return line.startswith(("module ", "requires ")) or (
        line.startswith("  ") and not line.startswith("    ") and stripped.startswith(STARTERS)
    )


def kind_of(text: str) -> str:
    first = text.lstrip()
    for kind in ("requires", "module", "imports", "configuration", "syntax", "context", "rule", "claim", "endmodule"):
        if first.startswith(kind):
            return kind
    return "other"


totals: Counter[str] = Counter()
attribute_totals: Counter[str] = Counter()

for path in FILES:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if starts_record(line)]
    records = []
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = lines[start:stop]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        if not block:
            continue
        text = "\n".join(block)
        kind = kind_of(text)
        attrs = [name for name in ATTRIBUTES if re.search(rf"\b{re.escape(name)}\b", text)]
        records.append((start + 1, kind, attrs, text))
        totals[kind] += 1
        for attr in attrs:
            attribute_totals[attr] += 1

    relative = path.relative_to(ROOT)
    provenance = (
        "PROOF-LOCAL"
        if relative in (Path("verification.k"), Path("spec.k"))
        else "TRUSTED-SUPPLIED"
    )
    print(f"===== FILE {relative} ({provenance}) =====")
    file_counts = Counter(kind for _, kind, _, _ in records)
    print("COUNTS " + " ".join(f"{key}={file_counts[key]}" for key in sorted(file_counts)))
    for ordinal, (line, kind, attrs, text) in enumerate(records, 1):
        attr_text = ",".join(attrs) if attrs else "-"
        print(f"\n[{ordinal:03d}] line={line} kind={kind} attrs={attr_text}")
        print(text)
    print()

print("===== GLOBAL COUNTS =====")
print("records " + " ".join(f"{key}={totals[key]}" for key in sorted(totals)))
print("attributes " + " ".join(f"{key}={attribute_totals[key]}" for key in sorted(attribute_totals)))
