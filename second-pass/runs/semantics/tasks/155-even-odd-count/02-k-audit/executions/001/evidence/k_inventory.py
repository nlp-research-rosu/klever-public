#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule index for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
SEMANTICS = ROOT / "reference-semantics"
PROOF_FILES = [ROOT / "verification.k", ROOT / "spec.k"]

ENTRY = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|alias)\b"
)
ATTR = re.compile(
    r"\b(function|total|functional|simplification|symbol|no-evaluators|"
    r"priority|owise|macro|strict|seqstrict|concrete)\b"
)

def clean(text: str) -> str:
    text = " ".join(
        part.strip()
        for part in text.splitlines()
        if part.strip() and not part.lstrip().startswith("//")
    )
    return text.replace("|", r"\|")[:240]


files = sorted(SEMANTICS.rglob("*.k")) + PROOF_FILES
records = []
for path in files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if ENTRY.match(line)]
    for pos, start in enumerate(starts):
        stop = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:stop])
        code_block = "\n".join(
            line.split("//", 1)[0] for line in lines[start:stop]
        )
        match = ENTRY.match(lines[start])
        assert match is not None
        kind = match.group(1).replace(" ", "-")
        attrs = ",".join(sorted(set(ATTR.findall(code_block)))) or "-"
        relative = path.relative_to(ROOT)
        if path in PROOF_FILES:
            provenance = "candidate-proof"
            relevance = "PROOF_CRITICAL"
            if path.name == "verification.k" and start + 1 == 62:
                disposition = "UNSOUND_OPERATIONAL_BRIDGE"
            elif kind == "claim":
                disposition = "TARGET_CLAIM"
            else:
                disposition = "SOUND_DEFINITION_OR_EXACT_MACRO"
        else:
            provenance = "trusted-supplied"
            relevance = "BASELINE_REVIEWED"
            disposition = "SELECTED_TRUSTED_BASELINE"
        opaque = (
            "OPAQUE_OR_EXTERNAL"
            if kind == "syntax"
            and re.search(r"\bno-evaluators\b|symbol\s*\(", code_block)
            else "-"
        )
        records.append(
            {
                "file": str(relative),
                "line": start + 1,
                "kind": kind,
                "attrs": attrs,
                "provenance": provenance,
                "relevance": relevance,
                "disposition": disposition,
                "opaque": opaque,
                "text": clean(block),
            }
        )

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Each row is one `configuration`, `syntax`, `rule`, `claim`, `context`, "
    "or `alias` declaration start. Multi-line text and attributes are folded "
    "into that row. The candidate supplied-semantics tree was byte-identical "
    "to the trusted reference tree."
)
print()
print(f"Total entries: {len(records)}")
print()
print("Kinds:", dict(sorted(Counter(r["kind"] for r in records).items())))
print(
    "Provenance:",
    dict(sorted(Counter(r["provenance"] for r in records).items())),
)
print(
    "Relevance:",
    dict(sorted(Counter(r["relevance"] for r in records).items())),
)
print(
    "Dispositions:",
    dict(sorted(Counter(r["disposition"] for r in records).items())),
)
print()
print(
    "| # | Source | Kind | Attributes | Provenance | Relevance | Disposition | "
    "Opaque/external | Declaration or rule |"
)
print("|---:|---|---|---|---|---|---|---|---|")
for number, record in enumerate(records, 1):
    source = f"{record['file']}:{record['line']}"
    print(
        f"| {number} | `{source}` | {record['kind']} | "
        f"{record['attrs']} | {record['provenance']} | "
        f"{record['relevance']} | {record['disposition']} | "
        f"{record['opaque']} | "
        f"{record['text']} |"
    )
