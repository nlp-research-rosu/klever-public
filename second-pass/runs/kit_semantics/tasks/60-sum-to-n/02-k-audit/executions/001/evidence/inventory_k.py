#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule ledger.

The extractor treats each source statement beginning with module/imports,
configuration, syntax, context, rule, or claim as one record and includes its
continuation lines through the next statement marker.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(module|imports|configuration|syntax|context|rule|claim)\b"
)


def strip_comment(line: str) -> str:
    # These sources contain no quoted // tokens.
    return line.split("//", 1)[0].rstrip()


def classify(source: Path, kind: str, text: str) -> tuple[str, str]:
    if "reference-semantics/" in source.as_posix():
        origin = "SUPPLIED_FIXED_SEMANTICS"
    elif source.name == "verification.k":
        origin = "PROOF_LOCAL"
    else:
        origin = "SPECIFICATION"

    flags = []
    for flag in (
        "function",
        "total",
        "functional",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "concrete",
        "owise",
        "macro-rec",
        "macro",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", text):
            flags.append(flag)
    if kind == "rule" and "simplification" not in flags:
        flags.append("ordinary-rule")
    return origin, ",".join(flags) if flags else "-"


records = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        cleaned = strip_comment(line)
        match = START.match(cleaned)
        if match:
            starts.append((index, match.group(1)))
    starts.append((len(lines), "EOF"))
    for position in range(len(starts) - 1):
        begin, kind = starts[position]
        end, _ = starts[position + 1]
        chunks = [strip_comment(line).strip() for line in lines[begin:end]]
        chunks = [chunk for chunk in chunks if chunk]
        text = " ".join(chunks)
        origin, flags = classify(path, kind, text)
        records.append(
            (
                path.relative_to(ROOT).as_posix(),
                begin + 1,
                kind,
                origin,
                flags,
                re.sub(r"\s+", " ", text),
            )
        )

print("id\tfile\tline\tkind\torigin\tflags\tstatement")
for number, record in enumerate(records, 1):
    print(number, *record, sep="\t")

counts: dict[tuple[str, str], int] = {}
for _, _, kind, origin, _, _ in records:
    counts[(origin, kind)] = counts.get((origin, kind), 0) + 1
print("# SUMMARY", file=__import__("sys").stderr)
for (origin, kind), count in sorted(counts.items()):
    print(f"# {origin}\t{kind}\t{count}", file=__import__("sys").stderr)
print(f"# TOTAL\t{len(records)}", file=__import__("sys").stderr)
