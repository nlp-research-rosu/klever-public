#!/usr/bin/env python3
"""Generate a line-addressed inventory of all local K declarations and rules."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/161-solve")
FILES = [ROOT / "reference-semantics" / "semantics.k"]
FILES += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
FILES += [ROOT / "verification.k", ROOT / "spec.k"]

START = re.compile(
    r'^(requires(?=\s+")|module\b|endmodule\b|  imports\b|  configuration\b|'
    r"  syntax\b|  context\b|  rule\b|  claim\b)"
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        first = lines[start].strip()
        kind = START.match(lines[start]).group(1).strip()
        if kind in {"rule", "claim", "syntax", "configuration", "context"}:
            body_lines = lines[start:end]
            while body_lines and (
                not body_lines[-1].strip()
                or body_lines[-1].lstrip().startswith("//")
            ):
                body_lines.pop()
        else:
            body_lines = [lines[start]]
        body = " ".join(
            line.strip()
            for line in body_lines
            if line.strip() and not line.lstrip().startswith("//")
        )
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", body):
                attrs.append(attr)
        if kind == "rule":
            if "simplification" in attrs:
                classification = "simplification-rule"
            elif "concrete" in attrs:
                classification = "concrete-rule"
            elif "priority" in attrs:
                classification = "priority-semantic-rule"
            elif "macro" in attrs or "macro-rec" in attrs:
                classification = "macro-rule"
            else:
                classification = "ordinary-rule"
        elif kind == "syntax":
            classification = "syntax-declaration"
        else:
            classification = kind
        yield {
            "file": path.relative_to(ROOT).as_posix(),
            "line": start + 1,
            "kind": kind,
            "classification": classification,
            "attributes": ",".join(attrs),
            "text": body,
        }


rows = [row for path in FILES for row in blocks(path)]
out = Path("/audit-output/evidence/rule_inventory.tsv")
with out.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=(
            "file",
            "line",
            "kind",
            "classification",
            "attributes",
            "text",
        ),
        dialect="excel-tab",
    )
    writer.writeheader()
    writer.writerows(rows)

counts = {}
for row in rows:
    key = (row["file"], row["classification"])
    counts[key] = counts.get(key, 0) + 1
print(f"inventory_rows={len(rows)}")
for (file, classification), count in sorted(counts.items()):
    print(f"{file}\t{classification}\t{count}")
