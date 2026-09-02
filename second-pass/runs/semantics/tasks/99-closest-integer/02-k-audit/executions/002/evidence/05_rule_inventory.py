#!/usr/bin/env python3
"""Exhaustive inventory of K source declarations and sentences."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
OUT = Path("/audit-output/evidence/05_rule_inventory.tsv")

START = re.compile(
    r"^\s*(module|endmodule|imports|syntax|configuration|"
    r"context(?:\s+alias)?|rule|claim)\b"
)
ATTRIBUTES = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "concrete",
    "simplification",
    "priority",
    "owise",
    "strict",
    "seqstrict",
    "macro",
]

# All materially reached fixed-semantic sentences occur in these modules. The
# TSV retains every other sentence as fixed-baseline/unreached rather than
# silently omitting it.
RELEVANT_FILES = {
    "reference-semantics/semantics.k",
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/float.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/builtins.k",
    "reference-semantics/semantics/call.k",
    "verification.k",
    "spec.k",
}


def strip_line_comment(line: str) -> str:
    # K files in this corpus do not place // inside string literals on sentence
    # lines. Preserve quoted operator "/" and other punctuation.
    return line.split("//", 1)[0].rstrip()


records: list[dict[str, str | int]] = []
for path in FILES:
    relative = path.relative_to(ROOT).as_posix()
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if line.startswith('requires "'):
            starts.append((index, "requires"))
            continue
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw = "\n".join(lines[index:next_index])
        cleaned_lines = [
            strip_line_comment(line).strip()
            for line in raw.splitlines()
            if strip_line_comment(line).strip()
        ]
        text = " ".join(cleaned_lines)
        attrs = ",".join(
            attribute
            for attribute in ATTRIBUTES
            if re.search(rf"\b{re.escape(attribute)}\b", text)
        )
        if relative == "verification.k":
            audit_class = "candidate-proof-extension"
        elif relative == "spec.k":
            audit_class = "target-claim"
        elif relative in RELEVANT_FILES:
            audit_class = "fixed-supplied/reached-or-import"
        else:
            audit_class = "fixed-supplied/unreached"
        if relative == "verification.k" and kind == "rule":
            if "rule runClosest(" in text:
                assessment = "sound-fresh-entry-wrapper"
            elif "rule closestBody()" in text:
                assessment = "sound-definitional-body-identity"
            elif "nearestAway(" in text:
                assessment = "sound-expression-definition/not-a-closeness-theorem"
            else:
                assessment = "candidate-rule/no-false-witness-identified"
        elif (
            relative == "reference-semantics/semantics/float.k"
            and kind == "rule"
            and "intToF(intPart(CS))" in text
        ):
            assessment = "false-vs-python-full-domain/witness-1e1"
        elif relative == "spec.k":
            assessment = "target-claim/to-be-judged-for-adequacy"
        elif relative.startswith("reference-semantics/"):
            if audit_class.endswith("unreached"):
                assessment = "fixed-supplied-unreached/no-false-witness-identified"
            else:
                assessment = "fixed-supplied-selected/no-false-witness-identified"
        else:
            assessment = "declaration-or-module-structure"
        records.append(
            {
                "id": len(records) + 1,
                "file": relative,
                "line": index + 1,
                "kind": kind,
                "attributes": attrs,
                "audit_class": audit_class,
                "assessment": assessment,
                "text": text,
            }
        )

with OUT.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "file",
            "line",
            "kind",
            "attributes",
            "audit_class",
            "assessment",
            "text",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(records)

kind_counts = Counter(str(record["kind"]) for record in records)
attribute_counts = Counter(
    attribute
    for record in records
    for attribute in str(record["attributes"]).split(",")
    if attribute
)
file_counts = Counter(str(record["file"]) for record in records)
class_counts = Counter(str(record["audit_class"]) for record in records)

print(f"source_file_count={len(FILES)}")
print(f"inventory_record_count={len(records)}")
print(f"kind_counts={dict(sorted(kind_counts.items()))}")
print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
print(f"class_counts={dict(sorted(class_counts.items()))}")
for file, count in sorted(file_counts.items()):
    print(f"file_count {file} {count}")
print(f"inventory_path={OUT}")
