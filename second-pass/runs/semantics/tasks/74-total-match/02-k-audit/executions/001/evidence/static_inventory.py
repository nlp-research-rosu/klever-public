#!/usr/bin/env python3
"""Create an exhaustive sentence-level inventory of the audited K sources."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/candidate-src")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence")

START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|rule|context|claim)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")
ATTRIBUTE_TOKEN = re.compile(
    r"\b(?:functional|function|total|simplification|owise|concrete|"
    r"macro-rec|macro|no-evaluators|anywhere|assoc|comm|token|bracket|"
    r"left|right|non-assoc|avoid|prefer)\b|"
    r"\b(?:priority|strict|seqstrict|symbol|hook|unit|element|wrapElement|"
    r"format|color)\([^)]*\)"
)
FUNCTION_PRODUCTION = re.compile(
    r"([#A-Za-z_][#A-Za-z0-9_-]*)\s*\([^)]*\)\s*"
    r"\[([^\]]*\bfunction\b[^\]]*)\]",
    re.DOTALL,
)


def sentences(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for number, line in enumerate(lines, start=1):
        match = START.match(line)
        if match:
            if current is not None:
                result.append(current)
            current = {
                "file": str(path.relative_to(ROOT)),
                "line": number,
                "kind": match.group(1),
                "lines": [line],
            }
        elif current is not None:
            cast_lines = current["lines"]
            assert isinstance(cast_lines, list)
            cast_lines.append(line)
    if current is not None:
        result.append(current)
    return result


def normalize(lines: list[str]) -> str:
    kept = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("//") or not stripped:
            continue
        kept.append(stripped)
    return " ".join(kept)


def disposition(file: str, line: int, kind: str) -> str:
    if file.startswith("reference-semantics/"):
        if kind in {"syntax", "rule", "context", "configuration"}:
            return "ACCEPTED_FIXED_SUPPLIED_BASELINE"
        return "STRUCTURAL_FIXED_SUPPLIED_BASELINE"
    if file == "verification.k":
        if kind == "rule" and line == 86:
            return "REJECT_UNSOUND_OPERATIONAL_BRIDGE"
        if line in {112, 113}:
            return "REJECT_REAL_PROGRAM_PINNING_GAP"
        if kind in {"syntax", "rule"}:
            return "ACCEPT_PROOF_LOCAL_DEFINITION_OR_ADAPTER"
        return "STRUCTURAL_PROOF_MODULE"
    if file == "spec.k":
        if kind == "claim" and line == 10:
            return "CLOSES_BUT_DOES_NOT_JUSTIFY_BRIDGE_MATCH_DOMAIN"
        if kind == "claim":
            return "CLOSES_UNDER_REJECTED_THEORY"
        return "STRUCTURAL_SPEC_MODULE"
    return "REVIEWER_ARTIFACT"


paths = sorted(SEMANTICS.rglob("*.k")) + [ROOT / "verification.k", ROOT / "spec.k"]
all_sentences: list[dict[str, object]] = []
for path in paths:
    all_sentences.extend(sentences(path))

rows: list[dict[str, object]] = []
rule_texts: list[str] = []
for index, sentence in enumerate(all_sentences, start=1):
    lines = sentence["lines"]
    assert isinstance(lines, list)
    text = normalize(lines)
    kind = str(sentence["kind"])
    attrs = sorted(
        {
            token.group(0)
            for match in ATTR.finditer(text)
            for token in ATTRIBUTE_TOKEN.finditer(match.group(1))
        }
    )
    if kind == "rule":
        rule_texts.append(text)
    rows.append(
        {
            "id": index,
            "file": sentence["file"],
            "line": sentence["line"],
            "kind": kind,
            "attributes": ";".join(attrs),
            "disposition": disposition(
                str(sentence["file"]), int(sentence["line"]), kind
            ),
            "text": text,
        }
    )

with (OUTPUT / "rule-inventory.tsv").open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "file",
            "line",
            "kind",
            "attributes",
            "disposition",
            "text",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

function_symbols: dict[str, list[tuple[str, int, str]]] = {}
for row in rows:
    if row["kind"] != "syntax":
        continue
    text = str(row["text"])
    for match in FUNCTION_PRODUCTION.finditer(text):
        symbol, attrs = match.groups()
        function_symbols.setdefault(symbol, []).append(
            (str(row["file"]), int(row["line"]), attrs)
        )

opaque_rows = []
for symbol, declarations in sorted(function_symbols.items()):
    lhs_definitions = 0
    for rule_text in rule_texts:
        lhs = rule_text.split("=>", 1)[0]
        if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(symbol)}\s*\(", lhs):
            lhs_definitions += 1
    for file, line, attrs in declarations:
        opaque_rows.append(
            {
                "symbol": symbol,
                "file": file,
                "line": line,
                "attributes": attrs,
                "lhs_definition_count": lhs_definitions,
                "classification": (
                    "NO_DIRECT_LOCAL_EQUATION_OPAQUE_OR_EXTENSIBLE"
                    if lhs_definitions == 0
                    else "LOCALLY_EQUATED"
                ),
            }
        )

with (OUTPUT / "opaque-symbol-inventory.tsv").open(
    "w", encoding="utf-8", newline=""
) as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "symbol",
            "file",
            "line",
            "attributes",
            "lhs_definition_count",
            "classification",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(opaque_rows)

kind_counts = Counter(str(row["kind"]) for row in rows)
attribute_counts = Counter()
for row in rows:
    for attribute in str(row["attributes"]).split(";"):
        if attribute:
            attribute_counts[attribute] += 1
disposition_counts = Counter(str(row["disposition"]) for row in rows)
summary = {
    "files": len(paths),
    "sentences": len(rows),
    "kind_counts": dict(sorted(kind_counts.items())),
    "attribute_counts": dict(sorted(attribute_counts.items())),
    "disposition_counts": dict(sorted(disposition_counts.items())),
    "function_declarations": len(opaque_rows),
    "function_declarations_without_direct_equation": sum(
        row["lhs_definition_count"] == 0 for row in opaque_rows
    ),
}
(OUTPUT / "rule-inventory-summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(summary, indent=2, sort_keys=True))
