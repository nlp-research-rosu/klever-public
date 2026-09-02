#!/usr/bin/env python3
"""Build a line-addressable inventory of supplied and proof-local K declarations."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
OUTPUT = Path("/audit-output/evidence")
SOURCES = [
    *sorted((SCRATCH / "reference-semantics").rglob("*.k")),
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

START_RE = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|"
    r"syntax(?:\s+priority|\s+priorities)?|rule|claim|context(?:\s+alias)?)\b"
)
DECL_RE = re.compile(
    r"^\s*(configuration|syntax(?:\s+priority|\s+priorities)?|"
    r"rule|claim|context(?:\s+alias)?)\b"
)
ATTR_WORDS = (
    "function",
    "total",
    "functional",
    "opaque",
    "macro",
    "priority",
    "simplification",
    "owise",
    "anywhere",
    "concrete",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
)


def normalized(block: list[str]) -> str:
    pieces = []
    for line in block:
        line = re.sub(r"//.*$", "", line).strip()
        if line:
            pieces.append(line)
    return re.sub(r"\s+", " ", " ".join(pieces))


records: list[dict[str, object]] = []
for path in SOURCES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START_RE.match(line)]
    for position, start in enumerate(starts):
        declaration = DECL_RE.match(lines[start])
        if declaration is None:
            continue
        next_start = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = lines[start:next_start]
        text = normalized(block)
        leading = declaration.group(1)
        kind = leading.replace(" ", "_")
        attrs = [word for word in ATTR_WORDS if re.search(rf"\b{word}\b", text)]
        if kind == "rule":
            if "simplification" in attrs:
                role = "simplification_rule"
            elif "priority" in attrs:
                role = "priority_rule"
            elif "owise" in attrs:
                role = "owise_rule"
            else:
                role = "ordinary_rule"
        elif kind.startswith("syntax"):
            if "function" in attrs or "functional" in attrs:
                role = "function_declaration"
            elif "macro" in attrs:
                role = "macro_declaration"
            else:
                role = "syntax_declaration"
        else:
            role = kind
        records.append(
            {
                "id": len(records) + 1,
                "source_class": (
                    "proof_local"
                    if path.name in {"verification.k", "spec.k"}
                    else "supplied_semantics"
                ),
                "file": str(path.relative_to(SCRATCH)),
                "start_line": start + 1,
                "end_line": next_start,
                "kind": kind,
                "role": role,
                "attributes": ",".join(attrs) or "-",
                "text": text,
            }
        )

with (OUTPUT / "k-declaration-rule-inventory.tsv").open(
    "w", encoding="utf-8", newline=""
) as output:
    writer = csv.DictWriter(output, fieldnames=list(records[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(records)

summary = {
    "source_files": [str(path.relative_to(SCRATCH)) for path in SOURCES],
    "source_file_count": len(SOURCES),
    "record_count": len(records),
    "by_source_class": Counter(str(record["source_class"]) for record in records),
    "by_kind": Counter(str(record["kind"]) for record in records),
    "by_role": Counter(str(record["role"]) for record in records),
    "attribute_occurrences": Counter(
        attribute
        for record in records
        for attribute in str(record["attributes"]).split(",")
        if attribute != "-"
    ),
    "opaque_records": [
        record["id"] for record in records if "opaque" in str(record["attributes"])
    ],
}

with (OUTPUT / "k-inventory-summary.json").open("w", encoding="utf-8") as output:
    json.dump(summary, output, indent=2, sort_keys=True)
    output.write("\n")

print(json.dumps(summary, indent=2, sort_keys=True))
