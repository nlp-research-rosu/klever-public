#!/usr/bin/env python3
"""Produce a line-numbered inventory of K declarations, rules, and claims."""

from __future__ import annotations

import re
import sys
from pathlib import Path


START = re.compile(
    r"^(?:"
    r"requires\s+|"
    r"module\s+|"
    r"endmodule\b|"
    r"\s+(?:imports|configuration|syntax|context(?:\s+alias)?|rule|claim|priority)\b"
    r")"
)

ATTRIBUTE_WORDS = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "simplification",
    "simplifier",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).rstrip()
        yield start + 1, text


def kind_of(text: str) -> str:
    first = text.lstrip()
    if first.startswith("syntax "):
        return "syntax"
    if first.startswith("configuration"):
        return "configuration"
    if first.startswith("rule "):
        return "operational-rule" if "<k>" in text else "equational-rule"
    if first.startswith("claim "):
        return "claim"
    if first.startswith("context"):
        return "context"
    if first.startswith("priority"):
        return "priority-declaration"
    if first.startswith("imports "):
        return "import"
    if first.startswith("requires "):
        return "require"
    if first.startswith("module "):
        return "module"
    if first.startswith("endmodule"):
        return "endmodule"
    return "other"


def attributes(text: str) -> str:
    found = [word for word in ATTRIBUTE_WORDS if re.search(rf"\b{re.escape(word)}\b", text)]
    return ", ".join(found) if found else "none"


paths = [Path(argument) for argument in sys.argv[1:]]
if not paths:
    raise SystemExit("usage: k_inventory.py FILE [FILE ...]")

records = []
for path in paths:
    for line, text in blocks(path):
        records.append((path, line, kind_of(text), attributes(text), text))

print("# Exhaustive K source inventory")
print()
print(
    "This mechanical inventory covers every top-level module/include/import, "
    "configuration, syntax declaration, context, rule, priority declaration, "
    "and claim in the supplied semantics plus candidate proof sources."
)
print()
print("## Counts")
print()
by_kind: dict[str, int] = {}
by_attribute: dict[str, int] = {}
for _, _, kind, _, _ in records:
    by_kind[kind] = by_kind.get(kind, 0) + 1
for _, _, _, attrs, _ in records:
    if attrs != "none":
        for attribute in attrs.split(", "):
            by_attribute[attribute] = by_attribute.get(attribute, 0) + 1
for kind in sorted(by_kind):
    print(f"- {kind}: {by_kind[kind]}")
print(f"- total: {len(records)}")
print()
print("### Attribute/classifier occurrences by record")
print()
for attribute in sorted(by_attribute):
    print(f"- {attribute}: {by_attribute[attribute]}")

for path in paths:
    print()
    print(f"## {path}")
    path_records = [record for record in records if record[0] == path]
    print()
    print(f"Records: {len(path_records)}")
    for _, line, kind, attrs, text in path_records:
        print()
        print(f"### line {line}: {kind}")
        print()
        print(f"Attributes/classifiers: {attrs}")
        print()
        print("```k")
        print(text)
        print("```")
