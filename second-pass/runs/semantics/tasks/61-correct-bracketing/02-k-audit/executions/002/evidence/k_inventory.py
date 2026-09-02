#!/usr/bin/env python3
"""Exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/proof")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(requires|module|imports|configuration|syntax|context|rule|claim|alias|endmodule)\b"
)


def remove_line_comment(line: str) -> str:
    quote = False
    escaped = False
    for index in range(len(line) - 1):
        char = line[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
        elif char == '"':
            quote = True
        elif line[index : index + 2] == "//":
            return line[:index]
    return line


def statements(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        stripped = remove_line_comment(line).strip()
        match = START.match(stripped)
        if match:
            starts.append((number, match.group(1)))
    for index, (number, kind) in enumerate(starts):
        next_number = starts[index + 1][0] if index + 1 < len(starts) else len(lines) + 1
        payload_lines = [
            remove_line_comment(line).strip()
            for line in lines[number - 1 : next_number - 1]
            if remove_line_comment(line).strip()
        ]
        yield number, kind, " ".join(payload_lines)


totals = collections.Counter()
by_file: dict[str, collections.Counter] = {}
flag_totals = collections.Counter()
entries = []
for path in FILES:
    rel = path.relative_to(ROOT).as_posix()
    file_counts = collections.Counter()
    for number, kind, payload in statements(path):
        file_counts[kind] += 1
        totals[kind] += 1
        flags = []
        for flag in [
            "function",
            "total",
            "functional",
            "no-evaluators",
            "symbol",
            "priority",
            "simplification",
            "owise",
            "concrete",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ]:
            if re.search(rf"\b{re.escape(flag)}\b", payload):
                flags.append(flag)
                flag_totals[flag] += 1
        entries.append((rel, number, kind, ",".join(flags) or "-", payload))
    by_file[rel] = file_counts

print("INVENTORY_SCOPE:")
for path in FILES:
    print(f"  {path}")
print("COUNTS_BY_FILE:")
for rel, counts in by_file.items():
    rendered = " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
    print(f"  {rel}: {rendered}")
print("TOTALS:")
for kind in sorted(totals):
    print(f"  {kind}={totals[kind]}")
print("ATTRIBUTE_OCCURRENCES_BY_STATEMENT:")
for flag in [
    "function",
    "total",
    "functional",
    "no-evaluators",
    "symbol",
    "priority",
    "simplification",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]:
    print(f"  {flag}={flag_totals[flag]}")
print("ENTRIES:")
for index, (rel, number, kind, flags, payload) in enumerate(entries, 1):
    print(f"{index:04d} {rel}:{number} kind={kind} flags={flags} :: {payload}")

line_rule_count = 0
line_syntax_count = 0
for path in FILES:
    for line in path.read_text().splitlines():
        stripped = remove_line_comment(line).strip()
        line_rule_count += int(stripped.startswith("rule "))
        line_syntax_count += int(stripped.startswith("syntax "))
assert line_rule_count == totals["rule"]
assert line_syntax_count == totals["syntax"]
print(f"CROSSCHECK line_rule_count={line_rule_count} inventory_rule_count={totals['rule']}")
print(f"CROSSCHECK line_syntax_count={line_syntax_count} inventory_syntax_count={totals['syntax']}")
print("SUMMARY: exhaustive statement-start inventory completed")
