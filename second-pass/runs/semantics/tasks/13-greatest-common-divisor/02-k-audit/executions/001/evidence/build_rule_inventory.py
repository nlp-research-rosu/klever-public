#!/usr/bin/env python3
"""Build a complete, line-addressed inventory of K declarations and rules."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/source")
OUTPUT = Path("/audit-output/evidence/stage5_rule_inventory.md")
SUMMARY = Path("/audit-output/evidence/stage5_rule_inventory_summary.json")

source_files = sorted((WORK / "reference-semantics").rglob("*.k"))
source_files.extend([WORK / "verification.k", WORK / "spec.k"])

start_re = re.compile(r"^\s*(syntax|configuration|context|rule|claim)\b")
boundary_re = re.compile(
    r"^\s*(?:module|endmodule|imports|syntax|configuration|context|rule|claim)\b"
)
attribute_re = re.compile(r"\[([^\]]+)\]", re.DOTALL)
known_bare_attributes = {
    "anywhere",
    "assoc",
    "bracket",
    "comm",
    "concrete",
    "function",
    "functional",
    "macro",
    "macro-rec",
    "no-evaluators",
    "owise",
    "preserves-definedness",
    "right",
    "left",
    "simplification",
    "strict",
    "token",
    "total",
}
known_attribute_prefixes = (
    "format(",
    "hook(",
    "klabel(",
    "label(",
    "priority(",
    "seqstrict(",
    "symbol(",
    "symbolic(",
    "unit(",
)


def compact(text: str) -> str:
    return " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    )


def split_attribute_list(raw: str) -> list[str]:
    parts = []
    current = []
    depth = 0
    for character in raw:
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        if character == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    parts.append("".join(current).strip())
    return parts


items = []
for path in source_files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if start_re.match(line)]
    for position, start in enumerate(starts):
        candidate_end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        end = candidate_end
        # Module/import boundaries can occur after the final item in a module.
        for index in range(start + 1, candidate_end):
            if boundary_re.match(lines[index]) and not start_re.match(lines[index]):
                end = index
                break
        block = "\n".join(lines[start:end]).rstrip()
        match = start_re.match(lines[start])
        assert match is not None
        kind = match.group(1)
        attributes = []
        code_without_comments = "\n".join(
            line for line in block.splitlines() if not line.lstrip().startswith("//")
        )
        for raw in attribute_re.findall(code_without_comments):
            for part in split_attribute_list(raw):
                if part in known_bare_attributes or part.startswith(known_attribute_prefixes):
                    attributes.append(part)

        if kind == "rule":
            if any(attr.startswith("priority") for attr in attributes):
                category = "priority rule"
            elif "simplification" in attributes:
                category = "simplification rule"
            elif "owise" in attributes:
                category = "owise rule"
            elif "concrete" in attributes:
                category = "concrete rule"
            else:
                category = "ordinary rule"
        elif kind == "syntax":
            if "no-evaluators" in attributes:
                category = "opaque-symbol syntax"
            elif "function" in attributes or "functional" in attributes:
                category = "function syntax"
            elif "total" in attributes:
                category = "total syntax"
            elif "macro" in attributes or "macro-rec" in attributes:
                category = "macro syntax"
            else:
                category = "syntax"
        else:
            category = kind

        items.append(
            {
                "file": str(path.relative_to(WORK)),
                "line": start + 1,
                "kind": kind,
                "category": category,
                "attributes": attributes,
                "text": compact(block),
            }
        )

counts_by_category = Counter(item["category"] for item in items)
counts_by_kind = Counter(item["kind"] for item in items)
counts_by_file = Counter(item["file"] for item in items)
attribute_counts = Counter(attribute for item in items for attribute in item["attributes"])

opaque = [
    f"{item['file']}:{item['line']} {item['text']}"
    for item in items
    if "no-evaluators" in item["attributes"]
]
functional = [
    f"{item['file']}:{item['line']} {item['text']}"
    for item in items
    if "functional" in item["attributes"]
]
total = [
    f"{item['file']}:{item['line']} {item['text']}"
    for item in items
    if "total" in item["attributes"]
]
simplifications = [
    f"{item['file']}:{item['line']} {item['text']}"
    for item in items
    if "simplification" in item["attributes"]
]
priorities = [
    f"{item['file']}:{item['line']} {item['text']}"
    for item in items
    if any(attribute.startswith("priority") for attribute in item["attributes"])
]

summary = {
    "source_file_count": len(source_files),
    "item_count": len(items),
    "counts_by_kind": dict(sorted(counts_by_kind.items())),
    "counts_by_category": dict(sorted(counts_by_category.items())),
    "counts_by_file": dict(sorted(counts_by_file.items())),
    "attribute_counts": dict(sorted(attribute_counts.items())),
    "opaque_no_evaluators": opaque,
    "functional_declarations": functional,
    "total_declaration_count": len(total),
    "simplification_rule_count": len(simplifications),
    "priority_rule_count": len(priorities),
}
SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K declaration and rule inventory\n\n")
    stream.write(
        "Generated independently from the fresh scratch source. Each item begins "
        "at the cited source line; multi-line bodies, guards, and attributes are "
        "normalized onto one line.\n\n"
    )
    stream.write("## Summary\n\n")
    stream.write(f"- Source files: {len(source_files)}\n")
    stream.write(f"- Inventoried items: {len(items)}\n")
    for category, count in sorted(counts_by_category.items()):
        stream.write(f"- {category}: {count}\n")
    stream.write(f"- Declarations carrying `total`: {len(total)}\n")
    stream.write(f"- Declarations carrying `functional`: {len(functional)}\n")
    stream.write(f"- Rules carrying `simplification`: {len(simplifications)}\n")
    stream.write(f"- Rules carrying a priority: {len(priorities)}\n")
    stream.write(f"- Declarations carrying `no-evaluators`: {len(opaque)}\n\n")

    current_file = None
    for index, item in enumerate(items, start=1):
        if item["file"] != current_file:
            current_file = item["file"]
            stream.write(f"## `{current_file}`\n\n")
        attrs = ", ".join(item["attributes"]) if item["attributes"] else "none"
        stream.write(
            f"{index}. `{item['file']}:{item['line']}` — **{item['category']}**; "
            f"attributes: `{attrs}` — `{item['text']}`\n\n"
        )

print(json.dumps(summary, indent=2))
