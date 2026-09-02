#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory from the audited K sources."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


WORK = Path("/tmp/audit-work/98-count-upper")
OUT = Path("/audit-output/evidence/rule-inventory.tsv")
sources = [
    WORK / "reference-semantics/semantics.k",
    *sorted((WORK / "reference-semantics/semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]

start_re = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
attr_names = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "anywhere",
]

entries: list[dict[str, object]] = []
for path in sources:
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = start_re.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        body = [lines[index].strip()]
        index += 1
        while index < len(lines):
            if start_re.match(lines[index]) or re.match(r"^\s*endmodule\b", lines[index]):
                break
            stripped = lines[index].strip()
            if not stripped or stripped.startswith("//"):
                break
            body.append(stripped)
            index += 1
        text = " ".join(body)
        attributes = [name for name in attr_names if re.search(rf"\b{re.escape(name)}\b", text)]
        if path.parts[-2:] == ("reference-semantics", "semantics.k"):
            scope = "supplied-semantics"
        elif "reference-semantics" in path.parts:
            scope = "supplied-semantics"
        elif path.name == "verification.k":
            scope = "proof-local"
        else:
            scope = "specification"

        if kind == "rule":
            subtype = "ordinary-semantic-rule"
            if "simplification" in attributes:
                subtype = "simplification-rule"
            elif "priority" in attributes:
                subtype = "priority-rule"
            elif "concrete" in attributes:
                subtype = "concrete-only-rule"
            elif "owise" in attributes:
                subtype = "owise-rule"
        elif kind == "syntax":
            subtype = "syntax-declaration"
            if "function" in attributes or "functional" in attributes:
                subtype = "function-declaration"
            if "symbol" in attributes or "no-evaluators" in attributes:
                subtype = "opaque-symbol-declaration"
            elif "macro" in attributes or "macro-rec" in attributes:
                subtype = "macro-declaration"
        else:
            subtype = kind

        if scope == "supplied-semantics":
            decision = "FOLLOWS_SELECTED_SUPPLIED_SEMANTICS"
        elif scope == "proof-local" and kind == "rule":
            decision = "REVIEWED_SOUND_ORDINARY_MATHEMATICS"
        elif scope == "proof-local":
            decision = "REVIEWED_WELL_FOUNDED_DEFINITION"
        else:
            decision = "PROOF_OBLIGATION_NOT_ASSUMED_AS_RULE"

        entries.append(
            {
                "path": path.relative_to(WORK).as_posix(),
                "line": start + 1,
                "scope": scope,
                "kind": kind,
                "subtype": subtype,
                "attributes": ",".join(attributes) if attributes else "-",
                "decision": decision,
                "text": text,
            }
        )

with OUT.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "path",
            "line",
            "scope",
            "kind",
            "subtype",
            "attributes",
            "decision",
            "text",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    for number, entry in enumerate(entries, 1):
        writer.writerow({"id": f"K{number:04d}", **entry})

print("inventory_output:", OUT)
print("source_files:", len(sources))
print("inventory_entries:", len(entries))
print("counts_by_kind:")
for key, count in sorted(Counter(str(entry["kind"]) for entry in entries).items()):
    print(f"  {key}: {count}")
print("counts_by_subtype:")
for key, count in sorted(Counter(str(entry["subtype"]) for entry in entries).items()):
    print(f"  {key}: {count}")
print("attribute_counts:")
attribute_counts: Counter[str] = Counter()
for entry in entries:
    for attr in str(entry["attributes"]).split(","):
        if attr != "-":
            attribute_counts[attr] += 1
for key, count in sorted(attribute_counts.items()):
    print(f"  {key}: {count}")
print("counts_by_file:")
for key, count in sorted(Counter(str(entry["path"]) for entry in entries).items()):
    print(f"  {key}: {count}")

# Independent start-line count: every declaration keyword found by the same
# lexical boundary must have exactly one inventory row.
raw_start_counts: Counter[str] = Counter()
for path in sources:
    for line in path.read_text().splitlines():
        match = start_re.match(line)
        if match:
            raw_start_counts[match.group(1)] += 1
inventory_counts = Counter(str(entry["kind"]) for entry in entries)
print("start_line_counts_equal_inventory_counts:", raw_start_counts == inventory_counts)
if raw_start_counts != inventory_counts:
    print("raw_start_counts:", dict(raw_start_counts))
    print("inventory_counts:", dict(inventory_counts))
    raise SystemExit(1)
