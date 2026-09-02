#!/usr/bin/env python3
"""Emit an exhaustive, source-located K declaration/rule inventory."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/144-simplify")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "loop-spec.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(module|endmodule|imports|syntax|configuration|"
    r"rule|claim|context)\b"
)
ITEM = re.compile(r"^\s*(syntax|configuration|rule|claim|context)\b")


def one_line(block: str) -> str:
    return re.sub(r"\s+", " ", block).strip()


totals: Counter[str] = Counter()
records: list[str] = []

for path in FILES:
    relative = path.relative_to(ROOT)
    provenance = (
        "trusted-fixed"
        if str(relative).startswith("reference-semantics/")
        else "proof-local"
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    module = "(outside-module)"
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("module "):
            module = stripped.split()[1]
            index += 1
            continue
        match = ITEM.match(lines[index])
        if not match:
            index += 1
            continue
        item_type = match.group(1)
        start = index
        index += 1
        while index < len(lines):
            if START.match(lines[index]):
                break
            index += 1
        block = "\n".join(lines[start:index])
        normalized = one_line(block)
        digest = hashlib.sha256(block.encode()).hexdigest()[:16]
        attributes = []
        for attribute in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "simplification",
            "owise",
            "priority",
            "strict",
            "seqstrict",
            "macro",
            "concrete",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", block):
                attributes.append(attribute)

        if item_type == "rule":
            semantic_kind = (
                "operational"
                if "<k>" in block or "~>" in block
                else "equational"
            )
            if "simplification" in attributes:
                semantic_kind += "+simplification"
            if "priority" in attributes:
                semantic_kind += "+priority"
        elif item_type == "syntax":
            semantic_kind = "declaration"
            if "no-evaluators" in attributes:
                semantic_kind += "+opaque"
            elif "function" in attributes:
                semantic_kind += "+function"
        elif item_type == "context":
            semantic_kind = "evaluation-context"
        elif item_type == "claim":
            semantic_kind = "reachability-claim"
        else:
            semantic_kind = "configuration"

        key = f"{provenance}:{item_type}:{semantic_kind}"
        totals[key] += 1
        records.append(
            "|".join(
                (
                    item_type.upper(),
                    provenance,
                    f"{relative}:{start + 1}",
                    module,
                    semantic_kind,
                    ",".join(attributes) or "-",
                    digest,
                    normalized,
                )
            )
        )

print("FORMAT: TYPE|PROVENANCE|LOCATION|MODULE|KIND|ATTRIBUTES|SHA256-16|TEXT")
print("SUMMARY:")
for key, count in sorted(totals.items()):
    print(f"{key}={count}")
print(f"TOTAL_RECORDS={len(records)}")
print("RECORDS:")
for record in records:
    print(record)
