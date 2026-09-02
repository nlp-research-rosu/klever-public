#!/usr/bin/env python3
"""Enumerate every local K declaration/rule in the supplied and proof-local sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SUPPLIED_ROOT = Path("/reference/reference-semantics")
FILES = [SUPPLIED_ROOT / "semantics.k"]
FILES.extend(sorted((SUPPLIED_ROOT / "semantics").glob("*.k")))
FILES.append(Path("/candidate/verification.k"))

START = re.compile(r"^  (syntax|rule|configuration|context|claim)\b")
MODULE = re.compile(r"^module\s+(\S+)")


def normalized(block: list[str]) -> str:
    return " ".join(part.strip() for part in block if part.strip())


records: list[dict[str, object]] = []
source_rule_count = 0
source_syntax_count = 0

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    module = "(outside-module)"
    index = 0
    while index < len(lines):
        module_match = MODULE.match(lines[index])
        if module_match:
            module = module_match.group(1)
        start_match = START.match(lines[index])
        if not start_match:
            index += 1
            continue
        kind = start_match.group(1)
        begin = index
        index += 1
        while index < len(lines):
            if START.match(lines[index]) or lines[index].startswith("endmodule"):
                break
            index += 1
        block = lines[begin:index]
        text = normalized(block)
        attrs: list[str] = []
        for attribute in (
            "function",
            "total",
            "functional",
            "macro",
            "macro-rec",
            "simplification",
            "priority",
            "owise",
            "concrete",
            "symbol",
            "no-evaluators",
            "strict",
            "seqstrict",
            "hook",
            "token",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", text):
                attrs.append(attribute)
        if kind == "rule":
            source_rule_count += 1
            if "simplification" in attrs:
                classification = "simplification-rule"
            elif "priority" in attrs:
                classification = "priority-rule"
            elif "concrete" in attrs:
                classification = "concrete-rule"
            elif "owise" in attrs:
                classification = "owise-rule"
            else:
                classification = "ordinary-rule"
        elif kind == "syntax":
            source_syntax_count += 1
            if "no-evaluators" in attrs:
                classification = "opaque-symbol-declaration"
            elif "macro" in attrs or "macro-rec" in attrs:
                classification = "macro-declaration"
            elif "function" in attrs:
                classification = "function-declaration"
            else:
                classification = "syntax-declaration"
        else:
            classification = kind
        records.append(
            {
                "path": str(path),
                "module": module,
                "line": begin + 1,
                "end_line": index,
                "kind": kind,
                "classification": classification,
                "attrs": attrs,
                "text": text,
            }
        )

counts = collections.Counter(str(record["classification"]) for record in records)
attribute_counts = collections.Counter(
    attribute for record in records for attribute in record["attrs"]  # type: ignore[union-attr]
)

print("INVENTORY_VERSION 1")
print("FILES", len(FILES))
for path in FILES:
    print("FILE", path)
print("RECORDS", len(records))
print("SOURCE_SYNTAX_STARTS", source_syntax_count)
print("SOURCE_RULE_STARTS", source_rule_count)
print("CLASSIFICATION_COUNTS", dict(sorted(counts.items())))
print("ATTRIBUTE_RECORD_COUNTS", dict(sorted(attribute_counts.items())))
print("INVENTORY_BEGIN")
for number, record in enumerate(records, 1):
    attrs = ",".join(record["attrs"]) if record["attrs"] else "-"
    print(
        f"{number:04d}\t{record['classification']}\t{record['module']}\t"
        f"{record['path']}:{record['line']}-{record['end_line']}\t"
        f"attrs={attrs}\t{record['text']}"
    )
print("INVENTORY_END")
