#!/usr/bin/env python3
"""Mechanical inventory of candidate-local K declarations and rules."""

from __future__ import annotations

import json
import re
from pathlib import Path


FILES = [
    Path("/tmp/audit-work/47-median/candidate-src/semantic.k"),
    Path("/tmp/audit-work/47-median/candidate-src/verification.k"),
]
DIRECTIVE = re.compile(
    r"^\s*(?:requires\b|module\b|endmodule\b|imports\b|syntax\b|rule\b|configuration\b)"
)


def collect_record(lines: list[str], start: int) -> str:
    parts = [lines[start].strip()]
    for index in range(start + 1, len(lines)):
        if DIRECTIVE.match(lines[index]):
            break
        stripped = lines[index].strip()
        if stripped and not stripped.startswith("//"):
            parts.append(stripped)
    return " ".join(parts)


for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    syntax_records = []
    rule_records = []
    configuration_records = []
    module = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("module "):
            module = stripped.split()[1]
        if stripped.startswith("syntax "):
            syntax_records.append(
                {
                    "line": index + 1,
                    "module": module,
                    "text": collect_record(lines, index),
                }
            )
        elif stripped.startswith("rule "):
            rule_records.append(
                {
                    "line": index + 1,
                    "module": module,
                    "text": collect_record(lines, index),
                }
            )
        elif stripped == "configuration" or stripped.startswith("configuration "):
            configuration_records.append(
                {
                    "line": index + 1,
                    "module": module,
                    "text": collect_record(lines, index),
                }
            )

    all_text = "\n".join(lines)
    attributes = {
        name: len(re.findall(rf"\b{name}\b", all_text))
        for name in [
            "function",
            "total",
            "functional",
            "simplification",
            "anywhere",
            "priority",
            "owise",
            "opaque",
            "trusted",
        ]
    }
    print(
        "FILE_SUMMARY "
        + json.dumps(
            {
                "path": str(path),
                "syntax_declarations": len(syntax_records),
                "rules": len(rule_records),
                "configurations": len(configuration_records),
                "attribute_word_counts": attributes,
            },
            sort_keys=True,
        )
    )
    for number, record in enumerate(syntax_records, 1):
        print("SYNTAX " + json.dumps({"number": number, **record}, sort_keys=True))
    for number, record in enumerate(configuration_records, 1):
        print("CONFIG " + json.dumps({"number": number, **record}, sort_keys=True))
    for number, record in enumerate(rule_records, 1):
        print("RULE " + json.dumps({"number": number, **record}, sort_keys=True))
