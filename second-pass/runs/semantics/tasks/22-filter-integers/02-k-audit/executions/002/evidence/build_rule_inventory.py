#!/usr/bin/env python3
"""Emit a sentence-level exhaustive inventory of the audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/22-filter-integers")
paths = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

start_re = re.compile(
    r"^(?:"
    r"requires\b|module\b|endmodule\b|"
    r"  (?:imports\b|syntax\b|configuration\b|rule\b|claim\b|context\b)"
    r")"
)
attr_re = re.compile(
    r"\[((?:"
    r"function|functional|total|symbol(?:\([^)]*\))?|no-evaluators|"
    r"simplification|anywhere|owise|concrete|macro-rec|macro|"
    r"priority(?:\([^)]*\))?|strict(?:\([^)]*\))?|seqstrict(?:\([^)]*\))?"
    r")(?:\s*,\s*(?:"
    r"function|functional|total|symbol(?:\([^)]*\))?|no-evaluators|"
    r"simplification|anywhere|owise|concrete|macro-rec|macro|"
    r"priority(?:\([^)]*\))?|strict(?:\([^)]*\))?|seqstrict(?:\([^)]*\))?"
    r"))*)\]"
)


def classify(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("requires "):
        return "requires"
    if stripped.startswith("module "):
        return "module"
    if stripped.startswith("endmodule"):
        return "endmodule"
    if stripped.startswith("imports "):
        return "import"
    if stripped.startswith("syntax "):
        attrs = ",".join(attr_re.findall(text))
        if "macro" in attrs:
            return "syntax-macro"
        if "function" in attrs:
            return "syntax-function"
        return "syntax"
    if stripped.startswith("configuration"):
        return "configuration"
    if stripped.startswith("context"):
        return "context"
    if stripped.startswith("claim"):
        return "claim"
    if stripped.startswith("rule"):
        if "[macro" in text or re.match(
            r"rule (?:FILTER-|compBody|compNest|compGuard|ListComp|GenExp)", stripped
        ):
            return "rule-macro"
        if "<" in text.split("=>", 1)[0]:
            return "rule-operational"
        return "rule-equational"
    return "other"


records: list[tuple[str, int, str]] = []
for path in paths:
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if start_re.match(line)]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        text = " ".join(
            line.strip() for line in block if line.strip() and not line.lstrip().startswith("//")
        )
        records.append((str(path.relative_to(ROOT)), start + 1, text))

print("file\tline\tkind\tattributes\ttext")
for relative, line, text in records:
    attributes = ";".join(attr_re.findall(text)).replace("\t", " ")
    print(
        f"{relative}\t{line}\t{classify(text)}\t{attributes}\t"
        f"{text.replace(chr(9), ' ')}"
    )
