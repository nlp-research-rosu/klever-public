#!/usr/bin/env python3
"""Inventory K declarations and rules without trusting candidate prose."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/case")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r'^(?:requires\s+"|\s*(?:module\b|endmodule\b|imports\b|configuration\b|'
    r"syntax\b|context\b|rule\b|claim\b))"
)


def normalize(lines: list[str]) -> str:
    return " ".join(part.strip() for part in lines if part.strip())


def classify(text: str) -> str:
    stripped = text.lstrip()
    first = stripped.split(maxsplit=1)[0] if stripped else ""
    if first == "rule":
        if "[simplification" in text:
            return "simplification-rule"
        if "[macro" in text:
            return "macro-rule"
        return "ordinary-rule"
    if first == "claim":
        return "reachability-claim"
    if first == "syntax":
        attrs = []
        for attr in (
            "function",
            "total",
            "functional",
            "macro",
            "strict",
            "seqstrict",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", text):
                attrs.append(attr)
        return "syntax" + (":" + ",".join(attrs) if attrs else "")
    return first


rows: list[dict[str, object]] = []
for path in FILES:
    raw = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(raw) if START.match(line) and not line.lstrip().startswith("//")]
    for pos, begin in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(raw)
        # Drop trailing comments/blank lines belonging to the following section.
        block = raw[begin:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        text = normalize(block)
        rows.append(
            {
                "file": str(path.relative_to(ROOT)),
                "line": begin + 1,
                "kind": classify(text),
                "priority": ",".join(re.findall(r"priority\(([^)]+)\)", text)),
                "owise": "yes" if "[owise" in text else "",
                "text": text,
            }
        )

writer = csv.DictWriter(
    __import__("sys").stdout,
    fieldnames=["file", "line", "kind", "priority", "owise", "text"],
    delimiter="\t",
    lineterminator="\n",
)
writer.writeheader()
writer.writerows(rows)
