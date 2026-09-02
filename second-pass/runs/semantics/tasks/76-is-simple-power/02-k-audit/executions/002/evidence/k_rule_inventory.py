#!/usr/bin/env python3
"""Build a sentence-level inventory of the supplied and proof-local K sources."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


START = re.compile(
    r"^(?:(?P<top>requires|module|endmodule)\b|"
    r"  (?P<indented>imports|syntax|configuration|context|rule|claim)\b)"
)
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "opaque",
    "macro",
    "strict",
    "seqstrict",
    "priority",
    "owise",
    "simplification",
    "concrete",
    "symbol",
)


def without_line_comment(line: str) -> str:
    quoted = False
    escaped = False
    for index, character in enumerate(line):
        if escaped:
            escaped = False
            continue
        if character == "\\" and quoted:
            escaped = True
            continue
        if character == '"':
            quoted = not quoted
            continue
        if not quoted and line[index : index + 2] == "//":
            return line[:index].rstrip()
    return line.rstrip()


def sentences(path: Path) -> list[tuple[int, str, str]]:
    result: list[tuple[int, str, str]] = []
    active_line = 0
    active_kind = ""
    active: list[str] = []
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        line = without_line_comment(raw)
        match = START.match(line)
        if match:
            if active:
                result.append((active_line, active_kind, " ".join(active).strip()))
            active_line = line_number
            active_kind = match.group("top") or match.group("indented") or "UNKNOWN"
            active = [line.strip()]
        elif active and line.strip():
            active.append(line.strip())
    if active:
        result.append((active_line, active_kind, " ".join(active).strip()))
    return result


paths = [Path(argument) for argument in sys.argv[1:]]
if not paths:
    raise SystemExit("usage: k_rule_inventory.py FILE [FILE ...]")

overall_kinds: collections.Counter[str] = collections.Counter()
overall_attrs: collections.Counter[str] = collections.Counter()
for path in paths:
    file_sentences = sentences(path)
    kinds = collections.Counter(kind for _line, kind, _text in file_sentences)
    attrs: collections.Counter[str] = collections.Counter()
    for _line, kind, text in file_sentences:
        if kind not in {"syntax", "rule", "context", "configuration"}:
            continue
        bracket_text = " ".join(re.findall(r"\[([^\]]*)\]", text))
        for attribute in ATTRIBUTES:
            if re.search(rf"\b{re.escape(attribute)}\b", bracket_text):
                attrs[attribute] += 1
    overall_kinds.update(kinds)
    overall_attrs.update(attrs)
    print(f"FILE {path} kinds={dict(sorted(kinds.items()))} attrs={dict(sorted(attrs.items()))}")
    for line_number, kind, text in file_sentences:
        print(f"  {path}:{line_number} [{kind}] {text}")

print(f"OVERALL kinds={dict(sorted(overall_kinds.items()))}")
print(f"OVERALL attrs={dict(sorted(overall_attrs.items()))}")
