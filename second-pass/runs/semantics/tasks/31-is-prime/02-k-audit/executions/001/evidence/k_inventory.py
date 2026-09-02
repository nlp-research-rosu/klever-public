#!/usr/bin/env python3
"""Produce a line-addressable exhaustive K declaration/rule inventory."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/31-is-prime")
OUT_TEXT = Path("/audit-output/evidence/rule-inventory.txt")
OUT_JSON = Path("/audit-output/evidence/rule-inventory.json")

paths = [ROOT / "reference-semantics" / "semantics.k"]
paths.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
paths.extend([ROOT / "verification.k", ROOT / "spec.k"])

start_re = re.compile(
    r"^\s*(module\b|endmodule\b|imports\b|requires\s+\"|configuration\b|"
    r"syntax\b|rule\b|claim\b|context\b)"
)


def kind_of(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("requires "):
        return "requires-file"
    return stripped.split(maxsplit=1)[0]


def tags_for(kind: str, text: str) -> list[str]:
    tags: list[str] = []
    lower = text.lower()
    attributes = (
        "function",
        "total",
        "functional",
        "macro",
        "macro-rec",
        "simplification",
        "concrete",
        "owise",
        "anywhere",
        "no-evaluators",
        "strict",
        "seqstrict",
        "hook",
        "symbol",
        "priority",
    )
    for attribute in attributes:
        if re.search(rf"\b{re.escape(attribute)}(?:\b|\()", lower):
            tags.append(attribute)
    if kind == "rule":
        if re.match(r"^\s*rule\s+<k>", text):
            tags.append("k-cell-operational")
        elif "<" in text and ">" in text and "=>" in text:
            tags.append("cell-rewrite")
        else:
            tags.append("equational-or-term-rewrite")
    return sorted(set(tags))


records: list[dict[str, object]] = []
for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if start_re.match(line)]
    for index, start in enumerate(starts):
        end = starts[index + 1] - 1 if index + 1 < len(starts) else len(lines) - 1
        while end >= start and (
            not lines[end].strip() or lines[end].lstrip().startswith("//")
        ):
            end -= 1
        text = "\n".join(lines[start : end + 1]).strip()
        kind = kind_of(lines[start])
        relpath = str(path.relative_to(ROOT))
        records.append(
            {
                "file": relpath,
                "start_line": start + 1,
                "end_line": end + 1,
                "kind": kind,
                "tags": tags_for(kind, text),
                "text": text,
            }
        )

kind_counts = Counter(str(record["kind"]) for record in records)
tag_counts = Counter(
    str(tag) for record in records for tag in record["tags"]  # type: ignore[index]
)
file_counts = Counter(str(record["file"]) for record in records)

payload = {
    "source_root": str(ROOT),
    "files": [str(path.relative_to(ROOT)) for path in paths],
    "summary": {
        "record_count": len(records),
        "kind_counts": dict(sorted(kind_counts.items())),
        "tag_counts": dict(sorted(tag_counts.items())),
        "file_record_counts": dict(sorted(file_counts.items())),
    },
    "records": records,
}
OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

with OUT_TEXT.open("w", encoding="utf-8") as stream:
    stream.write(f"SOURCE_ROOT: {ROOT}\n")
    stream.write(f"RECORD_COUNT: {len(records)}\n")
    stream.write(f"KIND_COUNTS: {dict(sorted(kind_counts.items()))}\n")
    stream.write(f"TAG_COUNTS: {dict(sorted(tag_counts.items()))}\n")
    stream.write(f"FILE_RECORD_COUNTS: {dict(sorted(file_counts.items()))}\n")
    for number, record in enumerate(records, start=1):
        tags = ",".join(record["tags"]) or "none"  # type: ignore[arg-type]
        stream.write(
            f"\n[{number:04d}] {record['file']}:{record['start_line']}"
            f"-{record['end_line']} kind={record['kind']} tags={tags}\n"
        )
        for line in str(record["text"]).splitlines():
            stream.write(f"  {line}\n")

print(f"files={len(paths)}")
print(f"records={len(records)}")
print(f"kind_counts={dict(sorted(kind_counts.items()))}")
print(f"tag_counts={dict(sorted(tag_counts.items()))}")
print(f"text_inventory={OUT_TEXT}")
print(f"json_inventory={OUT_JSON}")
