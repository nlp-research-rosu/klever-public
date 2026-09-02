#!/usr/bin/env python3
"""Inventory all K declarations/rules without trusting candidate prose or caches."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/exchange-110-fresh")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.tsv")

START = re.compile(
    r"^(?:(requires|module|endmodule)\b|"
    r" {2}(imports|configuration|syntax(?:\s+priority|\s+priorities)?|"
    r"context|rule|claim|alias)\b)"
)
INTERESTING = {
    "function",
    "total",
    "functional",
    "macro",
    "macro-rec",
    "concrete",
    "simplification",
    "priority",
    "owise",
    "strict",
    "seqstrict",
    "symbol",
}


records: list[dict[str, object]] = []

for path in FILES:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[start].strip()
        kind_match = START.match(lines[start])
        assert kind_match is not None
        kind = kind_match.group(1) or kind_match.group(2)
        assert kind is not None
        if kind == "endmodule":
            text = first
        else:
            body = []
            for line in lines[start:end]:
                stripped = line.strip()
                if stripped and not stripped.startswith("//"):
                    body.append(stripped)
            text = " ".join(body)
        attributes = sorted(
            {
                attribute
                for attribute in INTERESTING
                if re.search(rf"\b{re.escape(attribute)}\b", text)
            }
        )
        semantic_class = ""
        if kind == "rule":
            semantic_class = "operational" if "<k>" in text else "equational"
        elif kind == "claim":
            semantic_class = "reachability-claim"
        elif kind.startswith("syntax"):
            semantic_class = "declaration"
        records.append(
            {
                "file": str(path.relative_to(ROOT)),
                "line": start + 1,
                "kind": kind,
                "class": semantic_class,
                "attributes": ",".join(attributes),
                "text": text.replace("\t", " "),
            }
        )

with OUTPUT.open("w") as stream:
    stream.write("file\tline\tkind\tclass\tattributes\ttext\n")
    for record in records:
        stream.write(
            "{file}\t{line}\t{kind}\t{class}\t{attributes}\t{text}\n".format(
                **record
            )
        )

counts_by_kind = collections.Counter(str(record["kind"]) for record in records)
rules_by_file = collections.Counter(
    str(record["file"]) for record in records if record["kind"] == "rule"
)
attribute_counts = collections.Counter(
    attribute
    for record in records
    for attribute in str(record["attributes"]).split(",")
    if attribute
)

print(f"inventory_path={OUTPUT}")
print(f"files={len(FILES)} records={len(records)}")
print("kind_counts=" + repr(dict(sorted(counts_by_kind.items()))))
print("attribute_counts=" + repr(dict(sorted(attribute_counts.items()))))
for file, count in sorted(rules_by_file.items()):
    print(f"rules[{file}]={count}")
