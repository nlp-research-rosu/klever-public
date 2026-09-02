#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory from the audited K sources."""

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/36-fizz-buzz")
paths = [ROOT / "reference-semantics" / "semantics.k"]
paths.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
paths.extend([ROOT / "verification.k", ROOT / "spec.k"])

start_re = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
boundary_re = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|module|endmodule|imports?)\b"
)
attribute_names = [
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "no-evaluators",
    "symbol",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]


def disposition(path: Path, kind: str, block: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "verification.k":
        return "proof-local-manual-review"
    if rel == "spec.k":
        return "proof-claim-manual-review"
    if rel == "reference-semantics/semantics.k":
        return "supplied-semantics-assembly"
    basename = path.name
    if basename in {
        "syntax.k",
        "core.k",
        "controls.k",
        "operators.k",
        "int.k",
        "bool.k",
        "functions.k",
        "call.k",
    }:
        return "supplied-module-containing-used-path"
    return "supplied-module-unreachable-from-submitted-constructors"


rows = []
for path in paths:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    for ordinal, (start, kind) in enumerate(starts):
        end = len(lines)
        for candidate in range(start + 1, len(lines)):
            if boundary_re.match(lines[candidate]):
                end = candidate
                break
        block = " ".join(part.strip() for part in lines[start:end] if part.strip())
        attrs = []
        for name in attribute_names:
            if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?:\(|\b)", block):
                attrs.append(name)
        rel = path.relative_to(ROOT).as_posix()
        rows.append(
            {
                "id": len(rows) + 1,
                "source": rel,
                "line": start + 1,
                "kind": kind,
                "attributes": ",".join(attrs) if attrs else "-",
                "disposition": disposition(path, kind, block),
                "statement": block,
            }
        )

out_tsv = Path("/audit-output/evidence/rule_inventory.tsv")
with out_tsv.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "source",
            "line",
            "kind",
            "attributes",
            "disposition",
            "statement",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

counts = Counter(row["kind"] for row in rows)
attrs = Counter()
for row in rows:
    for attr in row["attributes"].split(","):
        if attr != "-":
            attrs[attr] += 1
dispositions = Counter(row["disposition"] for row in rows)

out_summary = Path("/audit-output/evidence/rule_inventory_summary.txt")
with out_summary.open("w") as stream:
    print(f"files={len(paths)} entries={len(rows)}", file=stream)
    print("kinds=" + repr(dict(sorted(counts.items()))), file=stream)
    print("attributes=" + repr(dict(sorted(attrs.items()))), file=stream)
    print("dispositions=" + repr(dict(sorted(dispositions.items()))), file=stream)
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        selected = [row for row in rows if row["source"] == rel]
        local_counts = Counter(row["kind"] for row in selected)
        print(f"{rel}: entries={len(selected)} kinds={dict(sorted(local_counts.items()))}", file=stream)

print(out_tsv)
print(out_summary)
print(f"files={len(paths)} entries={len(rows)}")
