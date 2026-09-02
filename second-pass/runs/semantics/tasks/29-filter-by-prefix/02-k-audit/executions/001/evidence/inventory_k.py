#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/29-filter-by-prefix/candidate-src")
SEMANTICS = SCRATCH / "reference-semantics"
FILES = [SEMANTICS / "semantics.k"]
FILES += sorted((SEMANTICS / "semantics").glob("*.k"))
FILES += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

START = re.compile(r"^\s*(configuration|context|rule|syntax|claim|alias)\b")
BOUNDARY = re.compile(
    r"(?:^\s*(?:configuration|context|rule|syntax|claim|alias|module|endmodule|imports)\b)"
    r"|(?:^requires\b)"
)


def rel(path: Path) -> str:
    if path.is_relative_to(SCRATCH):
        return str(path.relative_to(SCRATCH))
    return str(path)


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        match = START.match(lines[i])
        if not match:
            i += 1
            continue
        kind = match.group(1)
        start = i
        i += 1
        while i < len(lines) and not BOUNDARY.match(lines[i]):
            i += 1
        end = i
        statement = "\n".join(lines[start:end]).strip()
        normalized = re.sub(r"\s+", " ", re.sub(r"//.*", "", statement)).strip()
        attrs = sorted(
            set(
                re.findall(
                    r"priority\([^)]+\)|symbol\([^)]+\)|\b(?:function|functional|total|"
                    r"constructor|macro|simplification|owise|anywhere|strict|seqstrict|"
                    r"trusted|concrete|no-evaluators)\b",
                    normalized,
                )
            )
        )
        if kind == "rule":
            if "<k>" in normalized:
                role = "operational"
            else:
                role = "equation"
            if "simplification" in attrs:
                role += "+simplification"
        elif kind == "syntax":
            role = "declaration"
        elif kind == "claim":
            role = "reachability"
        else:
            role = kind
        records.append(
            {
                "file": rel(path),
                "start": start + 1,
                "end": end,
                "kind": kind,
                "role": role,
                "attrs": ", ".join(attrs) if attrs else "—",
                "text": normalized,
            }
        )

for record in records:
    file = str(record["file"])
    start = int(record["start"])
    if file.startswith("reference-semantics/"):
        disposition = (
            "FIXED-SUPPLIED: integrity-exact selected semantics; no candidate-local "
            "conclusion. Used-fragment fidelity and unused opaque boundaries are "
            "assessed in REVIEW.md."
        )
    elif file == "verification.k" and start in (28, 29):
        disposition = (
            "SOUND WITH ADEQUACY BRIDGE: exact empty/cons iterator equations for "
            "proof-only stringList; isomorphic to list iteration but not itself a "
            "source-language list value."
        )
    elif file == "verification.k" and start in (34, 36, 40):
        disposition = (
            "SOUND: exhaustive, disjoint, structurally descending definition of "
            "prefix filtering."
        )
    elif file == "verification.k" and start in (46, 48):
        disposition = (
            "SOUND: finite ValSeq right-identity/associativity lemma; overlaps agree "
            "with the fixed valSeqConcat equations."
        )
    elif file == "verification.k" and start == 54:
        disposition = (
            "SOUND OBSERVER: reads the returned heap list, preserves all cells and "
            "continuation, and constrains structural equality."
        )
    elif file == "verification.k":
        disposition = (
            "SOUND DECLARATION/MACRO: exact submitted AST or typed constructor; "
            "details in REVIEW.md."
        )
    elif file == "spec.k":
        disposition = "CLAIM: independently reconstructed and audited in REVIEW.md."
    else:
        disposition = "REVIEWED."
    record["disposition"] = disposition

counts = collections.Counter((r["kind"], r["role"]) for r in records)
file_counts = collections.Counter(r["file"] for r in records)

print("# Exhaustive K declaration/rule inventory")
print()
print("Generated from clean scratch source. Each row is one top-level K declaration,")
print("context, configuration, rule, alias, or reachability claim.")
print()
print("## Counts")
print()
print(f"- Files: {len(FILES)}")
print(f"- Inventory records: {len(records)}")
for (kind, role), count in sorted(counts.items()):
    print(f"- `{kind}` / `{role}`: {count}")
print()
print("### Records by file")
print()
for file, count in sorted(file_counts.items()):
    print(f"- `{file}`: {count}")
print()
print("## Records")
print()
print("| # | Source | Kind | Role | Attributes | Audit disposition | Normalized declaration/rule |")
print("|---:|---|---|---|---|---|---|")
for number, record in enumerate(records, 1):
    text = str(record["text"]).replace("|", "\\|").replace("`", "\\`")
    source = f'{record["file"]}:{record["start"]}-{record["end"]}'
    print(
        f"| {number} | `{source}` | {record['kind']} | {record['role']} | "
        f"{record['attrs']} | {record['disposition']} | {text} |"
    )
