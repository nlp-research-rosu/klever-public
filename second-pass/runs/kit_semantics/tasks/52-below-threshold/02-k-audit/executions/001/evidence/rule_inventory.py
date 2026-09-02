#!/usr/bin/env python3
"""Mechanical exhaustive inventory of fixed and proof-local K declarations."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


fixed_root = Path("/reference/reference-semantics")
fixed_files = [fixed_root / "semantics.k", *sorted((fixed_root / "semantics").glob("*.k"))]
local_files = [
    Path("/candidate/base-verification.k"),
    Path("/candidate/verification-loops.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/connection-spec.k"),
    Path("/candidate/loop-spec.k"),
    Path("/candidate/spec.k"),
]
files = fixed_files + local_files

start_re = re.compile(
    r"^(requires|module|endmodule)\b"
    r"|^  (imports|configuration|syntax|context|alias|rule|claim)\b"
)
known_attribute_re = re.compile(
    r"(?:strict\([^]]*\)|seqstrict\([^]]*\)|priority\(\d+\)|symbol\([^]]*\)|"
    r"\b(?:function|functional|total|simplification|owise|macro-rec|macro|"
    r"no-evaluators|concrete|anywhere|heat|cool|strict|seqstrict)\b)"
)


def classify(path: Path, kind: str) -> str:
    if str(path).startswith(str(fixed_root)):
        if kind == "rule":
            return "SUPPLIED_FIXED_SEMANTIC_RULE"
        if kind == "context":
            return "SUPPLIED_FIXED_EVALUATION_CONTEXT"
        if kind == "configuration":
            return "SUPPLIED_FIXED_CONFIGURATION"
        return "SUPPLIED_FIXED_DECLARATION"
    if path.name == "base-verification.k":
        return "DEFINITIONAL_SUMMARY"
    if path.name == "verification-loops.k":
        return "DERIVED_COMPARISON_SIMPLIFICATION"
    if path.name == "verification.k":
        return "OPERATIONAL_BRIDGE"
    if path.name == "connection-spec.k":
        return "BRIDGE_FREE_COMPARISON_CONNECTION_CLAIM"
    if path.name == "loop-spec.k":
        return "BRIDGE_FREE_CONTROL_CONNECTION_CLAIM"
    if path.name == "spec.k":
        return "ENTRY_TARGET_CLAIM"
    return "UNCLASSIFIED"


rows: list[dict[str, str | int]] = []
for path in files:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for number, (start, kind) in enumerate(starts):
        end = starts[number + 1][0] if number + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        # Drop blank/comment suffix belonging to the next conceptual section.
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        normalized = " ".join(
            piece for piece in (re.sub(r"\s+", " ", line.strip()) for line in block_lines) if piece
        )
        attributes = known_attribute_re.findall(normalized)
        rows.append(
            {
                "provenance": "fixed" if path in fixed_files else "candidate-local",
                "file": str(path),
                "start_line": start + 1,
                "end_line": start + len(block_lines),
                "kind": kind,
                "attributes": ",".join(attributes),
                "classification": classify(path, kind),
                "declaration": normalized,
            }
        )

output = Path("/audit-output/evidence/rule-inventory.tsv")
with output.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

kind_counts = Counter((row["provenance"], row["kind"]) for row in rows)
class_counts = Counter(row["classification"] for row in rows)
attribute_counts: Counter[str] = Counter()
for row in rows:
    attribute_counts.update(filter(None, str(row["attributes"]).split(",")))

summary_lines = [
    f"files={len(files)} fixed_files={len(fixed_files)} candidate_local_files={len(local_files)}",
    f"inventory_rows={len(rows)}",
    "kind_counts:",
]
summary_lines.extend(f"  {key[0]} {key[1]}={value}" for key, value in sorted(kind_counts.items()))
summary_lines.append("classification_counts:")
summary_lines.extend(f"  {key}={value}" for key, value in sorted(class_counts.items()))
summary_lines.append("attribute_counts:")
summary_lines.extend(f"  {key}={value}" for key, value in sorted(attribute_counts.items()))
summary_lines.append("opaque_or_no_evaluators:")
summary_lines.extend(
    f"  {row['file']}:{row['start_line']}-{row['end_line']} {row['declaration']}"
    for row in rows
    if "no-evaluators" in str(row["attributes"])
)

summary = "\n".join(summary_lines) + "\n"
Path("/audit-output/evidence/rule-inventory-summary.txt").write_text(summary)
print(summary, end="")
