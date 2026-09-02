#!/usr/bin/env python3
"""Generate an exhaustive, reviewer-authored inventory of local K declarations."""

from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/candidate-src")
OUT = Path("/audit-output/evidence")


def blocks(path: Path, keyword: str) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if re.match(rf"^\s*{re.escape(keyword)}(?:\s|$)", line)
    ]
    result: list[tuple[int, str]] = []
    stop = re.compile(
        r"^\s*(?:rule|claim|syntax|configuration|module|endmodule|imports|requires)\b"
    )
    for index in starts:
        end = index + 1
        while end < len(lines) and not stop.match(lines[end]):
            end += 1
        text = " ".join(piece.strip() for piece in lines[index:end] if piece.strip())
        result.append((index + 1, text))
    return result


semantic_assessment = {
    55: ("ordinary-semantic", "module harness schedules body then exact flip_case call"),
    58: ("ordinary-semantic", "left-to-right statement-list sequencing"),
    60: ("ordinary-semantic", "function definition installs untranslated body"),
    63: ("ordinary-semantic", "selected function body executes with one argument binding"),
    67: ("ordinary-semantic", "return expression is evaluated before return control"),
    69: ("ordinary-semantic", "environment lookup"),
    72: ("ordinary-semantic", "string literal construction"),
    74: ("ordinary-semantic", "attribute receiver evaluates first"),
    75: ("ordinary-semantic", "string attribute binds name and receiver"),
    78: ("ordinary-semantic", "zero-argument callee evaluates before invocation"),
    79: ("trusted-primitive-bridge", "string.swapcase dispatches to defined pySwapCase"),
    82: ("ordinary-semantic", "returned value ends the sole call and clears local env"),
    91: ("definitional-summary", "empty-string pySwapCase base case"),
    92: ("definitional-summary", "nonempty pySwapCase recurses by computed UTF-8 width"),
    101: ("definitional-summary", "one-byte UTF-8 leading-byte case"),
    103: ("definitional-summary", "two-byte UTF-8 leading-byte case"),
    106: ("definitional-summary", "three-byte UTF-8 leading-byte case"),
    109: ("definitional-summary", "four-byte UTF-8 leading-byte case"),
    112: ("definitional-summary", "owise invalid-byte fallback width one"),
}

rule_rows: list[dict[str, str | int]] = []
for filename in ("semantic.k", "unicode-case.k", "verification.k"):
    path = ROOT / filename
    for line, text in blocks(path, "rule"):
        attrs = ",".join(re.findall(r"\[(.*?)\]", text))
        guard = ""
        if " requires " in text:
            guard = text.split(" requires ", 1)[1]
        if filename == "semantic.k":
            classification, assessment = semantic_assessment[line]
        elif filename == "unicode-case.k":
            classification = "definitional-summary"
            if "[owise]" in text:
                assessment = (
                    "identity on the exact complement of 2,816 mapped code points; "
                    "exhaustively checked by 05_unicode_rule_audit.py"
                )
            else:
                assessment = (
                    "ground CPython 3.10.12 swapcase equation; every row "
                    "exhaustively checked by 05_unicode_rule_audit.py"
                )
        else:
            classification = "definitional-summary"
            assessment = "transparent alias flipSpec(S) = pySwapCase(S)"
        rule_rows.append(
            {
                "file": filename,
                "line": line,
                "kind": classification,
                "attributes": attrs,
                "guard": guard,
                "assessment": assessment,
                "text": text,
            }
        )

syntax_rows: list[dict[str, str | int]] = []
for filename in ("semantic.k", "unicode-case.k", "verification.k"):
    path = ROOT / filename
    for line, text in blocks(path, "syntax"):
        attrs = ",".join(re.findall(r"\[(.*?)\]", text))
        syntax_rows.append(
            {
                "file": filename,
                "line": line,
                "attributes": attrs,
                "text": text,
            }
        )

claim_rows = [
    {"file": "spec-original.k", "line": line, "text": text}
    for line, text in blocks(ROOT / "spec-original.k", "claim")
]

with (OUT / "rule-inventory.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=rule_rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(rule_rows)

with (OUT / "syntax-inventory.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=syntax_rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(syntax_rows)

with (OUT / "claim-inventory.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=claim_rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(claim_rows)

function_syntax = [row for row in syntax_rows if "function" in str(row["attributes"])]
total_syntax = [row for row in syntax_rows if "total" in str(row["attributes"])]
owise_rules = [row for row in rule_rows if "owise" in str(row["attributes"])]
simplification_rules = [
    row for row in rule_rows if "simplification" in str(row["attributes"])
]
priority_rules = [
    row for row in rule_rows
    if re.search(r"\bpriority\b", str(row["attributes"]))
]
opaque_syntax = [
    row for row in syntax_rows
    if re.search(r"\b(?:symbolic|opaque)\b", str(row["attributes"]))
]

print(f"syntax_declaration_count={len(syntax_rows)}")
print(f"rule_count={len(rule_rows)}")
print(
    "rule_counts_by_file="
    + repr({
        filename: sum(row["file"] == filename for row in rule_rows)
        for filename in ("semantic.k", "unicode-case.k", "verification.k")
    })
)
print(f"claim_count={len(claim_rows)}")
print(f"configuration_count={len(blocks(ROOT / 'semantic.k', 'configuration'))}")
print(f"function_declaration_count={len(function_syntax)}")
for row in function_syntax:
    print(f"function={row['file']}:{row['line']} {row['text']}")
print(f"total_declaration_count={len(total_syntax)}")
for row in total_syntax:
    print(f"total={row['file']}:{row['line']} {row['text']}")
print(f"owise_rule_count={len(owise_rules)}")
for row in owise_rules:
    print(f"owise={row['file']}:{row['line']} {row['text']}")
print(f"simplification_rule_count={len(simplification_rules)}")
print(f"priority_rule_count={len(priority_rules)}")
print(f"opaque_or_symbolic_declaration_count={len(opaque_syntax)}")
print(f"rule_inventory={OUT / 'rule-inventory.tsv'}")
print(f"syntax_inventory={OUT / 'syntax-inventory.tsv'}")
print(f"claim_inventory={OUT / 'claim-inventory.tsv'}")

expected = {
    "syntax": 14,
    "rules": 2837,
    "claims": 3,
    "configuration": 1,
    "functions": 4,
    "total": 2,
    "owise": 2,
}
actual = {
    "syntax": len(syntax_rows),
    "rules": len(rule_rows),
    "claims": len(claim_rows),
    "configuration": len(blocks(ROOT / "semantic.k", "configuration")),
    "functions": len(function_syntax),
    "total": len(total_syntax),
    "owise": len(owise_rules),
}
print(f"expected_counts={expected}")
print(f"actual_counts={actual}")
if actual != expected or simplification_rules or priority_rules or opaque_syntax:
    raise SystemExit(1)
