#!/usr/bin/env python3
"""Build a line-addressable exhaustive declaration/rule inventory."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/audit-131-digits/candidate")
OUTPUT_MD = Path("/audit-output/evidence/rule_inventory.md")
OUTPUT_JSON = Path("/audit-output/evidence/rule_inventory.json")

files = sorted((WORK / "reference-semantics").rglob("*.k"))
files.extend([WORK / "verification.k", WORK / "spec.k"])

start_re = re.compile(r"^\s*(configuration|syntax|context(?:\s+alias)?|rule|claim)\b")
attr_names = [
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
]

entries = []
for path in files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        while end > start + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        text = "\n".join(lines[start:end]).rstrip()
        code_text = "\n".join(
            line.split("//", 1)[0] for line in lines[start:end]
        )
        bracket_text = " ".join(re.findall(r"\[([^\]]*)\]", code_text))
        attrs = [
            name
            for name in attr_names
            if re.search(
                rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])",
                bracket_text,
            )
        ]
        relative = str(path.relative_to(WORK))
        entries.append(
            {
                "id": len(entries) + 1,
                "file": relative,
                "start": start + 1,
                "end": end,
                "kind": kind,
                "attributes": attrs,
                "text": text,
            }
        )

declared_functions = {}
ruled_heads = set()
for entry in entries:
    if entry["kind"] == "syntax" and "function" in entry["attributes"]:
        head = re.search(r"::=.*?\b([#A-Za-z][#A-Za-z0-9_-]*)\s*\(", entry["text"], re.S)
        if head:
            declared_functions[head.group(1)] = entry["id"]
    if entry["kind"] == "rule":
        head = re.search(r"\brule\s+(?:<[^>]+>\s*)?(?:\{\s*)?([#A-Za-z][#A-Za-z0-9_-]*)\s*\(", entry["text"], re.S)
        if head:
            ruled_heads.add(head.group(1))

opaque_local_functions = sorted(
    (name, entry_id)
    for name, entry_id in declared_functions.items()
    if name not in ruled_heads
)

OUTPUT_JSON.write_text(
    json.dumps(
        {
            "entries": entries,
            "opaque_local_functions": opaque_local_functions,
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

counts = Counter(entry["kind"] for entry in entries)
attribute_counts = Counter(
    attr for entry in entries for attr in entry["attributes"]
)

with OUTPUT_MD.open("w", encoding="utf-8") as output:
    output.write("# Exhaustive K declaration and rule inventory\n\n")
    output.write(
        "Sources: fresh scratch copy of the supplied reference semantics, "
        "`verification.k`, and `spec.k`.\n\n"
    )
    output.write(f"Total inventory entries: {len(entries)}\n\n")
    output.write(f"Kind counts: {dict(sorted(counts.items()))}\n\n")
    output.write(
        f"Attribute-bearing entry counts: {dict(sorted(attribute_counts.items()))}\n\n"
    )
    output.write(
        "Locally declared function symbols with no directly detected defining "
        f"rule head: {opaque_local_functions}\n\n"
    )
    for entry in entries:
        attrs = ", ".join(entry["attributes"]) if entry["attributes"] else "none"
        output.write(
            f"## K{entry['id']:04d} — {entry['file']}:{entry['start']}"
            f"-{entry['end']} — {entry['kind']} — attributes: {attrs}\n\n"
        )
        output.write("```k\n")
        output.write(entry["text"])
        output.write("\n```\n\n")

print(f"entries={len(entries)}")
print(f"kind_counts={dict(sorted(counts.items()))}")
print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
print(f"opaque_local_functions={opaque_local_functions}")
