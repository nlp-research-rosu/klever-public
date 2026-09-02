#!/usr/bin/env python3
"""Enumerate every declaration/rule in the selected K sources.

This is deliberately lexical: it preserves the full normalized declaration
text, source line, attributes, and origin so the static review can be checked
against the source without relying on candidate prose.
"""

from __future__ import annotations

import collections
import re
from pathlib import Path

WORK = Path("/tmp/audit-work/87-get-row")
BASE = WORK / "reference-semantics"
FILES = sorted(BASE.rglob("*.k")) + [WORK / "verification.k", WORK / "spec.k"]

START = re.compile(
    r'^\s*(requires(?=\s*")|module|imports|configuration|syntax|context|rule|claim|endmodule)\b'
)
ATTR_GROUP = re.compile(r"\[([^\]]+)\]")
ATTR_TOKEN = re.compile(
    r"\b(?:function|functional|total|macro-rec|macro|concrete|owise|"
    r"no-evaluators|simplification|anywhere|strict|seqstrict|priority|symbol)"
    r"(?:\([^)]*\))?"
)


def origin(path: Path) -> str:
    if path == WORK / "verification.k":
        return "candidate-proof-extension"
    if path == WORK / "spec.k":
        return "candidate-target-claim"
    return "trusted-supplied-semantics"


def disposition(path: Path, kind: str, block: str) -> str:
    if path == WORK / "spec.k" and kind == "claim":
        return "target-claim; dynamic closure and adequacy reviewed separately"
    if path == WORK / "spec.k":
        return "candidate target-spec scaffolding"
    if path == WORK / "verification.k":
        if "addMatch" in block:
            return (
                "valid definitional summary; two integer guards are disjoint and "
                "exhaustive; no execution replacement"
            )
        if "getRowClosure" in block:
            return (
                "surrogate-entry pinning gap; constructs a copied closure instead "
                "of deriving the binding by module execution"
            )
        if "getRowBody" in block:
            return (
                "surrogate-body pinning gap; textually restates the body but the "
                "proof does not load solution.mpy"
            )
        return "candidate proof scaffolding; reviewed in REVIEW.md"
    return "FIXED-BASELINE; used path reviewed; otherwise imported-unused"


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw = "\n".join(lines[start:stop]).strip()
        # Exclude comments and blank lines while preserving all declaration text.
        normalized_lines = []
        for line in raw.splitlines():
            code = line.split("//", 1)[0].strip()
            if code:
                normalized_lines.append(code)
        block = " ".join(normalized_lines)
        attributes = sorted(
            {
                token
                for group in ATTR_GROUP.findall(block)
                for token in ATTR_TOKEN.findall(group)
            }
        )
        rel = (
            str(path.relative_to(WORK))
            if path.is_relative_to(WORK)
            else str(path)
        )
        records.append(
            {
                "source": rel,
                "line": start + 1,
                "origin": origin(path),
                "kind": kind,
                "attributes": ";".join(attributes) if attributes else "-",
                "disposition": disposition(path, kind, block),
                "statement": block.replace("|", r"\|"),
            }
        )

kind_counts = collections.Counter(str(record["kind"]) for record in records)
origin_counts = collections.Counter(str(record["origin"]) for record in records)
attribute_counts = collections.Counter()
for record in records:
    attrs = str(record["attributes"])
    if attrs != "-":
        attribute_counts.update(attrs.split(";"))

print("# Exhaustive lexical K declaration/rule inventory")
print()
print(f"Files inventoried: {len(FILES)}")
print(f"Declarations inventoried: {len(records)}")
print("Kinds: " + ", ".join(f"{key}={kind_counts[key]}" for key in sorted(kind_counts)))
print(
    "Origins: "
    + ", ".join(f"{key}={origin_counts[key]}" for key in sorted(origin_counts))
)
print(
    "Attributes: "
    + (
        ", ".join(
            f"{key}={attribute_counts[key]}" for key in sorted(attribute_counts)
        )
        if attribute_counts
        else "none"
    )
)
print(
    "Functional declarations: "
    f"{attribute_counts['functional']}; simplification declarations/rules: "
    f"{attribute_counts['simplification']}; priority rules: "
    f"{sum(1 for record in records if 'priority(' in str(record['statement']))}; "
    "opaque/no-evaluator declarations: "
    f"{sum(1 for record in records if 'no-evaluators' in str(record['statement']))}"
)
print()
print(
    "| # | Source:line | Origin | Kind | Attributes | Audit disposition | "
    "Normalized declaration/rule |"
)
print("|---:|---|---|---|---|---|---|")
for index, record in enumerate(records, start=1):
    cells = [
        str(index),
        f"{record['source']}:{record['line']}",
        str(record["origin"]),
        str(record["kind"]),
        str(record["attributes"]),
        str(record["disposition"]),
        str(record["statement"]),
    ]
    cells = [cell.replace("\n", " ").replace("|", r"\|") for cell in cells]
    print("| " + " | ".join(cells) + " |")
