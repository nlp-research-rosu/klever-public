#!/usr/bin/env python3
"""Textual inventory of every top-level K declaration in the audited sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/source")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(configuration|syntax\s+priority|syntax\s+associativity|"
    r"syntax\s+lexical|syntax|rule|claim|context\s+alias|context)\b"
)
FEATURES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "strict",
    "seqstrict",
    "anywhere",
)


def records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for pos, (index, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        for probe in range(index + 1, end):
            if re.match(r"^\s*endmodule\b", lines[probe]):
                end = probe
                break
        text = "\n".join(lines[index:end]).strip()
        yield index + 1, kind.replace(" ", "_"), text


def disposition(path: Path, line: int, kind: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("reference-semantics/"):
        return (
            "ACCEPTED_SELECTED_SUPPLIED_SEMANTICS:"
            "byte/type-identical trusted baseline; not a candidate proof extension"
        )
    if rel == "verification.k":
        if kind == "syntax":
            if line == 8:
                return "SOUND_DEFINITIONAL:exact AST abbreviations"
            if line == 65:
                return "SOUND_MATH:is-delimiter/is-whitespace predicates over Int"
            if line == 76:
                return "SOUND_DEFINITIONAL:structural scanner summaries over IntSeq"
        if kind == "rule":
            if line in (11, 53):
                return "SOUND_DEFINITIONAL:expands to exact submitted AST fragment"
            if line in (68, 71):
                return "SOUND_MATH:truthful total Boolean equation"
            if line in (80, 81, 94, 95, 105, 106):
                return (
                    "SOUND_MATH:disjoint/exhaustive structural recursion; "
                    "strict tail descent"
                )
        return "REVIEWED_NO_OTHER_EXTENSION_CLASS"
    if rel == "spec.k" and kind == "claim":
        if line in (8, 45, 81):
            return (
                "SOUND_RESTRICTED_CLAIM:exact loop/control/cell footprint; "
                "mutually proved, but no universal entry claim"
            )
        if line in (117, 144):
            return "SOUND_GROUND_ENTRY:exact result for one literal prompt example"
    return "REVIEWED"


all_rows = []
counts = collections.Counter()
feature_counts = collections.Counter()
for path in FILES:
    for line, kind, text in records(path):
        rel = path.relative_to(ROOT).as_posix()
        code = "\n".join(re.sub(r"//.*$", "", part) for part in text.splitlines()).strip()
        flat = " ".join(part.strip() for part in code.splitlines() if part.strip())
        present = [feature for feature in FEATURES if re.search(rf"\b{re.escape(feature)}\b", code)]
        all_rows.append(
            (
                rel,
                line,
                kind,
                ",".join(present) or "-",
                disposition(path, line, kind),
                flat,
            )
        )
        counts[kind] += 1
        for feature in present:
            feature_counts[feature] += 1

print("COUNTS_BY_KIND")
for key in sorted(counts):
    print(f"{key}\t{counts[key]}")
print("COUNTS_BY_FEATURE")
for key in FEATURES:
    print(f"{key}\t{feature_counts[key]}")
print("\nsource\tline\tkind\tfeatures\treview_disposition\tdeclaration")
for row in all_rows:
    print("\t".join(str(value) for value in row))
