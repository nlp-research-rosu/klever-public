#!/usr/bin/env python3
"""Emit an exhaustive, source-located inventory of local K declarations."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/115-max-fill")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(r"^\s*(configuration|syntax|context|rule|claim|alias)\b")
BOUNDARY = re.compile(r"^\s*(module|endmodule|imports|requires)\b")


def compact(lines: list[str]) -> str:
    kept = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("//"):
            continue
        kept.append(text)
    return " ".join(kept)


records = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        match = START.match(lines[start])
        assert match
        end_limit = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        end = end_limit
        for i in range(start + 1, end_limit):
            if BOUNDARY.match(lines[i]):
                end = i
                break
        while end > start + 1 and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        body = compact(lines[start:end])
        attrs = sorted(set(re.findall(
            r"\b(function|total|functional|simplification|priority|opaque|macro|"
            r"concrete|owise|strict|seqstrict|symbol|no-evaluators)\b",
            body,
        )))
        records.append({
            "path": str(path.relative_to(ROOT)),
            "start": start + 1,
            "end": end,
            "kind": match.group(1),
            "attrs": attrs,
            "body": body,
        })

counts = Counter(r["kind"] for r in records)
file_counts = Counter(r["path"] for r in records)
attribute_counts = Counter(attr for r in records for attr in r["attrs"])
print("# Exhaustive local K declaration inventory")
print()
print(f"Files: {len(FILES)}")
print(f"Declarations: {len(records)}")
print("Counts: " + ", ".join(f"{kind}={counts[kind]}" for kind in sorted(counts)))
print("Attribute-bearing declaration counts: " + ", ".join(
    f"{attr}={attribute_counts[attr]}" for attr in sorted(attribute_counts)
))
print()
print("Per-file declaration counts:")
for path in sorted(file_counts):
    print(f"- `{path}`: {file_counts[path]}")
print()
print("Extraction rule: every source line beginning with `configuration`, `syntax`, "
      "`context`, `rule`, `claim`, or `alias`; continuations run to the next "
      "declaration/module boundary. Attributes are lexically classified.")
print()

for index, rec in enumerate(records, 1):
    location = f"{rec['path']}:{rec['start']}"
    if rec["end"] > rec["start"]:
        location += f"-{rec['end']}"
    attrs = ", ".join(rec["attrs"]) if rec["attrs"] else "none"
    print(f"{index}. `{rec['kind']}` — `{location}` — attributes: {attrs}")
    print()
    print(f"   `{rec['body'].replace('`', chr(39))}`")
    print()
