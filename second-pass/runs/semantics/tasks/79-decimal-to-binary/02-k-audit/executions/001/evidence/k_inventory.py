#!/usr/bin/env python3
"""Produce an exhaustive statement inventory for the audited K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path

WORK = Path("/tmp/audit-work/79-decimal-to-binary")
SEMANTICS = WORK / "reference-semantics"
OUT_TSV = Path("/audit-output/evidence/k-rule-inventory.tsv")
OUT_REVIEW = Path("/audit-output/evidence/k-rule-review.tsv")
OUT_SUMMARY = Path("/audit-output/evidence/k-rule-inventory-summary.txt")

files = [SEMANTICS / "semantics.k"]
files.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
files.extend([WORK / "verification.k", WORK / "spec.k"])

start_re = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
next_re = re.compile(
    r"^\s*(?:configuration|syntax|context|rule|claim|module|endmodule)\b"
)
attr_names = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "strict",
    "seqstrict",
    "macro",
    "macro-rec",
)

rows: list[tuple[str, int, str, str, str, str]] = []
counts: collections.Counter[tuple[str, str]] = collections.Counter()
attr_counts: collections.Counter[str] = collections.Counter()

for path in files:
    text = path.read_text()
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        match = start_re.match(lines[index])
        if match is None:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not next_re.match(lines[index]):
            index += 1
        raw_block = "\n".join(lines[start:index]).strip()
        cleaned_lines = []
        for raw_line in raw_block.splitlines():
            without_comment = raw_line.split("//", 1)[0].rstrip()
            if without_comment.strip():
                cleaned_lines.append(without_comment)
        block = "\n".join(cleaned_lines)
        normalized = re.sub(r"\s+", " ", block)
        attrs = [name for name in attr_names if re.search(rf"\b{re.escape(name)}\b", block)]
        for attr in attrs:
            attr_counts[attr] += 1
        relative = str(path.relative_to(WORK))
        provenance = (
            "candidate-proof-extension"
            if path.name == "verification.k"
            else "candidate-positive-claim"
            if path.name == "spec.k"
            else "byte-identical-supplied-semantics"
        )
        rows.append(
            (
                relative,
                start + 1,
                kind,
                ",".join(attrs) if attrs else "-",
                provenance,
                normalized,
            )
        )
        counts[(relative, kind)] += 1

header = "file\tline\tkind\tattributes\tprovenance\tstatement\n"
body = "".join(
    "\t".join(
        [
            file,
            str(line),
            kind,
            attrs,
            provenance,
            statement.replace("\t", " "),
        ]
    )
    + "\n"
    for file, line, kind, attrs, provenance, statement in rows
)
OUT_TSV.write_text(header + body)

reached_lines = {
    "reference-semantics/semantics/syntax.k": {9, 37, 38, 39, 41, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        13,
        15,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        208,
        209,
        213,
        214,
        215,
    },
    "reference-semantics/semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "reference-semantics/semantics/call.k": {19, 20, 21, 31, 69},
    "reference-semantics/semantics/operators.k": {12},
    "reference-semantics/semantics/str.k": {13, 14, 15, 16, 20, 21, 22, 24},
    "reference-semantics/semantics/subscript.k": {
        27,
        28,
        44,
        49,
        50,
        51,
        52,
        54,
        55,
        56,
        61,
        63,
        68,
    },
    "reference-semantics/semantics/builtins.k": {
        17,
        108,
        114,
        115,
        116,
        117,
        118,
        119,
    },
    "reference-semantics/semantics/int.k": {19, 20},
}

review_header = (
    "file\tline\tkind\tattributes\tlocal_relevance\treview_disposition\tstatement\n"
)
review_rows = []
for file, line, kind, attrs, provenance, statement in rows:
    if file == "verification.k" and line == 12:
        relevance = "proof-critical"
        disposition = (
            "ordinary-math-sound-pure-slice-bridge;"
            "ground-fixed-semantics-connection-proved;"
            "bridge-free-symbolic-connection-not-closed"
        )
    elif file == "verification.k" and line == 20:
        relevance = "proof-critical"
        disposition = "sound-exact-body-entry-harness;full-module-auditor-claim-closed"
    elif file == "verification.k":
        relevance = "proof-critical"
        disposition = "sound-local-syntax-declaration"
    elif file == "spec.k":
        relevance = "entry-claim"
        disposition = "result-constraining-and-satisfiable"
    elif line in reached_lines.get(file, set()):
        relevance = "reachable-or-result-defining"
        disposition = "sound-on-formal-domain-under-byte-identical-supplied-semantics"
    else:
        relevance = "not-reachable-from-submitted-program-and-entry-claim"
        disposition = (
            "fixed-supplied-semantics-only;"
            "no-proof-local-conclusion-and-no-effect-on-this-theorem"
        )
    review_rows.append(
        "\t".join(
            [
                file,
                str(line),
                kind,
                attrs,
                relevance,
                disposition,
                statement.replace("\t", " "),
            ]
        )
        + "\n"
    )
OUT_REVIEW.write_text(review_header + "".join(review_rows))

summary_lines = [
    f"FILES: {len(files)}",
    f"INVENTORIED_STATEMENTS: {len(rows)}",
]
kind_totals = collections.Counter(row[2] for row in rows)
for kind in sorted(kind_totals):
    summary_lines.append(f"KIND_{kind.upper()}: {kind_totals[kind]}")
for attr in attr_names:
    summary_lines.append(f"ATTRIBUTE_{attr.upper()}: {attr_counts[attr]}")
summary_lines.append("PER_FILE_BEGIN")
for (relative, kind), count in sorted(counts.items()):
    summary_lines.append(f"{relative}\t{kind}\t{count}")
summary_lines.append("PER_FILE_END")
OUT_SUMMARY.write_text("\n".join(summary_lines) + "\n")

print("\n".join(summary_lines))
