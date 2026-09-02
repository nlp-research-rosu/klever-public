#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/15-string-sequence/candidate-src")
files = sorted((ROOT / "reference-semantics").rglob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]

STARTS = (
    "configuration",
    "syntax ",
    "rule ",
    "context ",
    "claim ",
    "macro ",
    "alias ",
)


def strip_comment(line: str) -> str:
    # None of these sources puts // inside a quoted K string.
    return line.split("//", 1)[0].rstrip()


inventory = []
for path in files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, raw in enumerate(lines):
        stripped = strip_comment(raw).strip()
        if stripped.startswith(STARTS):
            starts.append(index)
    for pos, start in enumerate(starts):
        stop = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        block_lines = []
        for raw in lines[start:stop]:
            cleaned = strip_comment(raw).strip()
            if cleaned in {"endmodule"}:
                break
            if cleaned:
                block_lines.append(cleaned)
        text = " ".join(block_lines)
        lead = block_lines[0] if block_lines else ""
        if lead.startswith("syntax "):
            kind = "syntax"
        elif lead.startswith("rule "):
            kind = "rule"
        elif lead.startswith("context "):
            kind = "context"
        elif lead.startswith("configuration"):
            kind = "configuration"
        elif lead.startswith("claim "):
            kind = "claim"
        elif lead.startswith("macro "):
            kind = "macro"
        else:
            kind = "alias"
        attrs = []
        attribute_patterns = (
            r"\bfunction\b",
            r"\bfunctional\b",
            r"\btotal\b",
            r"\bno-evaluators\b",
            r"\bsymbol\([^)]+\)",
            r"\bpriority\(\d+\)",
            r"\bowise\b",
            r"\bconcrete\b",
            r"\bsimplification\b",
            r"\bmacro-rec\b",
            r"\bmacro\b",
            r"\bseqstrict\([^)]+\)",
            r"(?<!seq)\bstrict(?:\([^)]+\))?",
        )
        for pattern in attribute_patterns:
            match = re.search(pattern, text)
            if match:
                attrs.append(match.group(0))
        if "reference-semantics" in path.parts:
            source_class = "fixed_supplied_semantics"
        elif path.name == "verification.k":
            source_class = "candidate_proof_extension"
        else:
            source_class = "candidate_claim"
        inventory.append(
            {
                "id": len(inventory) + 1,
                "file": path.relative_to(ROOT).as_posix(),
                "line": start + 1,
                "kind": kind,
                "attributes": attrs,
                "source_class": source_class,
                "text": text,
            }
        )

print("inventory_format=json-lines")
print(f"files={len(files)}")
print(f"items={len(inventory)}")
kind_counts = {}
attribute_counts = {}
source_counts = {}
for item in inventory:
    kind_counts[item["kind"]] = kind_counts.get(item["kind"], 0) + 1
    source_counts[item["source_class"]] = source_counts.get(item["source_class"], 0) + 1
    for attribute in item["attributes"]:
        attribute_counts[attribute] = attribute_counts.get(attribute, 0) + 1
print(f"kind_counts={json.dumps(kind_counts, sort_keys=True)}")
print(f"attribute_counts={json.dumps(attribute_counts, sort_keys=True)}")
print(f"source_counts={json.dumps(source_counts, sort_keys=True)}")
per_file = {}
for item in inventory:
    counts = per_file.setdefault(item["file"], {})
    counts[item["kind"]] = counts.get(item["kind"], 0) + 1
print(f"per_file_counts={json.dumps(per_file, sort_keys=True)}")
for item in inventory:
    print(json.dumps(item, sort_keys=True))
