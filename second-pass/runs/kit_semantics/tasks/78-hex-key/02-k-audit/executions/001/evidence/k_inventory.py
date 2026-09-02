#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^\s*(syntax|configuration|context|rule|claim|macro|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:syntax|configuration|context|rule|claim|macro|alias|"
    r"module|endmodule|imports|requires)\b"
)
MODULE = re.compile(r"^\s*module\s+(\S+)")


def strip_line_comment(line: str) -> str:
    in_string = False
    escaped = False
    index = 0
    while index < len(line):
        character = line[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif character == "/" and index + 1 < len(line) and line[index + 1] == "/":
            return line[:index]
        index += 1
    return line


def clean_construct(lines: list[str]) -> str:
    while lines and (not lines[-1].strip() or lines[-1].lstrip().startswith("//")):
        lines.pop()
    without_comments = []
    for line in lines:
        line = strip_line_comment(line)
        without_comments.append(line.strip())
    return " ".join(part for part in without_comments if part)


if len(sys.argv) < 2:
    raise SystemExit("usage: k_inventory.py FILE_OR_DIRECTORY [...]")

paths: list[Path] = []
for argument in sys.argv[1:]:
    path = Path(argument)
    if path.is_dir():
        paths.extend(sorted(path.rglob("*.k")))
    else:
        paths.append(path)
paths = sorted(dict.fromkeys(path.resolve() for path in paths))

records: list[dict[str, str | int]] = []
for path in paths:
    source = path.read_text().splitlines()
    current_module = ""
    modules_at_line: dict[int, str] = {}
    for number, line in enumerate(source, start=1):
        module_match = MODULE.match(line)
        if module_match:
            current_module = module_match.group(1)
        modules_at_line[number] = current_module

    starts = [
        (index, START.match(line).group(1))
        for index, line in enumerate(source)
        if START.match(line)
    ]
    for position, (start_index, kind) in enumerate(starts):
        end_index = len(source)
        if position + 1 < len(starts):
            end_index = starts[position + 1][0]
        for candidate in range(start_index + 1, end_index):
            if BOUNDARY.match(source[candidate]):
                end_index = candidate
                break
        text = clean_construct(source[start_index:end_index])
        attributes = []
        for attribute in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "owise",
            "concrete",
            "macro-rec",
            "macro",
            "strict",
            "seqstrict",
            "hook",
            "token",
            "bracket",
            "assoc",
            "comm",
            "unit",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", text):
                attributes.append(attribute)
        if kind == "syntax":
            category = "syntax-declaration"
        elif kind == "configuration":
            category = "configuration"
        elif kind == "context":
            category = "evaluation-context"
        elif kind == "claim":
            category = "reachability-claim"
        elif "simplification" in attributes:
            category = "simplification-rule"
        elif "macro" in attributes or "macro-rec" in attributes:
            category = "macro-rule"
        elif "<k>" in text:
            category = "operational-rule"
        else:
            category = "equational-rule"

        if kind == "syntax":
            disposition = "DECLARATION_REVIEW_REQUIRED"
        elif path.name == "verification.k":
            disposition = "PROOF_LOCAL_REVIEW_REQUIRED"
        elif path.name == "spec.k":
            disposition = "CLAIM_REVIEW_REQUIRED"
        else:
            disposition = "SUPPLIED_SEMANTICS_REVIEW_REQUIRED"
        records.append(
            {
                "file": str(path),
                "line": start_index + 1,
                "module": modules_at_line[start_index + 1],
                "kind": kind,
                "category": category,
                "attributes": ",".join(attributes) if attributes else "-",
                "opaque": (
                    "yes"
                    if "no-evaluators" in attributes
                    or ("symbol" in attributes and "concrete" not in attributes)
                    else "no"
                ),
                "disposition": disposition,
                "text": text.replace("\t", " "),
            }
        )

print(
    "id\tfile\tline\tmodule\tkind\tcategory\tattributes\topaque"
    "\tdisposition\ttext"
)
for index, record in enumerate(records, start=1):
    print(
        f"K{index:04d}\t{record['file']}\t{record['line']}\t"
        f"{record['module']}\t{record['kind']}\t{record['category']}\t"
        f"{record['attributes']}\t{record['opaque']}\t"
        f"{record['disposition']}\t{record['text']}"
    )

kind_counts = Counter(str(record["kind"]) for record in records)
category_counts = Counter(str(record["category"]) for record in records)
attribute_counts = Counter()
for record in records:
    for attribute in str(record["attributes"]).split(","):
        if attribute != "-":
            attribute_counts[attribute] += 1
opaque_count = sum(record["opaque"] == "yes" for record in records)

print(f"# SUMMARY records={len(records)}", file=sys.stderr)
print(f"# SUMMARY kinds={dict(sorted(kind_counts.items()))}", file=sys.stderr)
print(
    f"# SUMMARY categories={dict(sorted(category_counts.items()))}",
    file=sys.stderr,
)
print(
    f"# SUMMARY attributes={dict(sorted(attribute_counts.items()))}",
    file=sys.stderr,
)
print(f"# SUMMARY opaque={opaque_count}", file=sys.stderr)
