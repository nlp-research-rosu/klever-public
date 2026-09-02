#!/usr/bin/env python3
"""Lexical source inventory for every local K sentence in the audit definition."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
OUTPUT = Path("/audit-output/evidence/stage5")
SOURCES = [
    WORK / "reference-semantics/semantics.k",
    *sorted((WORK / "reference-semantics/semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]
KEYWORDS = (
    "requires",
    "syntax",
    "rule",
    "configuration",
    "context",
    "claim",
    "alias",
    "imports",
)


def starts_sentence(line: str) -> str | None:
    stripped = line.lstrip()
    for keyword in KEYWORDS:
        if keyword == "requires" and line != stripped:
            continue
        if stripped == keyword or stripped.startswith(keyword + " "):
            return keyword
    return None


def attributes(text: str) -> list[str]:
    result: list[str] = []
    for group in re.findall(r"\[([^\[\]]*)\]", text, flags=re.S):
        result.extend(
            token.strip()
            for token in group.split(",")
            if token.strip()
        )
    return result


records: list[dict] = []
source_documents: list[dict] = []
for source in SOURCES:
    relative = source.relative_to(WORK).as_posix()
    text = source.read_text()
    lines = text.splitlines()
    source_documents.append(
        {
            "path": relative,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "line_count": len(lines),
        }
    )
    module = None
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("module "):
            module = stripped.split()[1]
            index += 1
            continue
        if stripped == "endmodule":
            module = None
            index += 1
            continue
        keyword = starts_sentence(lines[index])
        if keyword is None:
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines):
            next_stripped = lines[index].strip()
            if next_stripped == "endmodule" or next_stripped.startswith("module "):
                break
            if starts_sentence(lines[index]) is not None:
                break
            index += 1
        body = "\n".join(lines[start:index]).rstrip()
        attrs = attributes(body)
        classification: list[str] = []
        if keyword == "syntax":
            classification.append("syntax")
            for name in [
                "function",
                "functional",
                "total",
                "macro",
                "macro-rec",
                "hook",
                "strict",
                "seqstrict",
                "token",
                "assoc",
                "comm",
                "unit",
                "no-evaluators",
            ]:
                if any(
                    token == name or token.startswith(name + "(")
                    for token in attrs
                ):
                    classification.append(name)
        elif keyword == "rule":
            classification.append("rule")
            if any(token.startswith("priority(") for token in attrs):
                classification.append("priority")
            for name in [
                "simplification",
                "concrete",
                "symbolic",
                "owise",
                "anywhere",
                "macro",
            ]:
                if name in attrs:
                    classification.append(name)
            if len(classification) == 1:
                classification.append("ordinary")
        else:
            classification.append(keyword)
        record_id = f"{relative}:{start + 1}-{index}"
        records.append(
            {
                "id": record_id,
                "source": relative,
                "module": module,
                "start_line": start + 1,
                "end_line": index,
                "keyword": keyword,
                "classification": classification,
                "attributes": attrs,
                "normalized": " ".join(body.split()),
                "text": body,
                "sha256": hashlib.sha256(body.encode()).hexdigest(),
            }
        )

document = {
    "schema_version": 1,
    "sources": source_documents,
    "record_count": len(records),
    "records": records,
}
(OUTPUT / "inventory.json").write_text(json.dumps(document, indent=2) + "\n")

counts = Counter()
for record in records:
    counts[record["keyword"]] += 1
    for classification in record["classification"]:
        counts[f"class:{classification}"] += 1

markdown = [
    "# Exhaustive local K source inventory",
    "",
    "Generated lexically from the fresh scratch copy. Every outer K sentence is",
    "identified by source line span; exact source text and SHA-256 are in",
    "`inventory.json`.",
    "",
    "## Counts",
    "",
]
for key, value in sorted(counts.items()):
    markdown.append(f"- `{key}`: {value}")
markdown.extend(["", "## Records", ""])
for record in records:
    classes = ",".join(record["classification"])
    attrs = ",".join(record["attributes"]) or "-"
    markdown.append(
        f"- `{record['id']}` module `{record['module']}`; "
        f"class `{classes}`; attrs `{attrs}`; "
        f"SHA-256 `{record['sha256']}`; `{record['normalized']}`"
    )
(OUTPUT / "inventory.md").write_text("\n".join(markdown) + "\n")

print(f"source_count={len(SOURCES)}")
print(f"record_count={len(records)}")
for key, value in sorted(counts.items()):
    print(f"{key}={value}")
print(f"json={OUTPUT / 'inventory.json'}")
print(f"markdown={OUTPUT / 'inventory.md'}")
