#!/usr/bin/env python3
"""Inventory every K declaration/rule in the audited source tree."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
OUT_CSV = Path("/audit-output/evidence/k_inventory.csv")
OUT_SUMMARY = Path("/audit-output/evidence/k_inventory_summary.txt")

files = sorted((ROOT / "reference-semantics").rglob("*.k"))
files.extend([ROOT / "verification.k", ROOT / "spec.k"])

record_start = re.compile(
    r"^\s{2}(requires|module|imports|syntax|configuration|context|rule|claim)\b"
)
record_boundary = re.compile(
    r"^\s{2}(requires|module|imports|syntax|configuration|context|rule|claim|endmodule)\b"
)


def audit_decision(relative: str, line: int, kind: str, text: str) -> str:
    if relative == "verification.k":
        if kind in {"syntax", "rule"} and (
            "encodeLoopBody" in text or "encodeFunctionBody" in text
        ):
            return "ACCEPTED_EXACT_AST_MACRO"
        if kind in {"syntax", "rule"}:
            return "ACCEPTED_DEFINITIONAL_MATHEMATICS"
    if relative == "spec.k" and kind == "claim":
        return "RECONSTRUCTED_POSITIVE_PROOF_OBLIGATION"
    if relative.startswith("reference-semantics/"):
        if "no-evaluators" in text or "OPAQUE" in text.upper():
            return "ACCEPTED_FIXED_OPAQUE_RULE_INERT_FOR_ENCODE"
        return "ACCEPTED_FIXED_SUPPLIED_SEMANTICS"
    return "STRUCTURAL_MODULE_DECLARATION"


rows: list[dict[str, str | int]] = []
for path in files:
    relative = str(path.relative_to(ROOT))
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        match = record_start.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines):
            line = lines[index]
            if record_boundary.match(line):
                break
            if re.match(r"^\s{2}//", line):
                break
            if not line.strip():
                break
            index += 1
        text = " ".join(part.strip() for part in lines[start:index] if part.strip())
        flags = [
            flag
            for flag in (
                "function",
                "total",
                "functional",
                "symbol",
                "no-evaluators",
                "priority",
                "simplification",
                "macro",
                "macro-rec",
                "concrete",
                "owise",
                "strict",
                "seqstrict",
            )
            if re.search(rf"\b{re.escape(flag)}\b", text)
        ]
        rows.append(
            {
                "id": len(rows) + 1,
                "file": relative,
                "line": start + 1,
                "kind": kind,
                "flags": ",".join(flags),
                "decision": audit_decision(relative, start + 1, kind, text),
                "declaration": text,
            }
        )

with OUT_CSV.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=["id", "file", "line", "kind", "flags", "decision", "declaration"],
    )
    writer.writeheader()
    writer.writerows(rows)

counts: dict[str, int] = {}
flags: dict[str, int] = {}
decisions: dict[str, int] = {}
for row in rows:
    kind = str(row["kind"])
    counts[kind] = counts.get(kind, 0) + 1
    decision = str(row["decision"])
    decisions[decision] = decisions.get(decision, 0) + 1
    for flag in str(row["flags"]).split(","):
        if flag:
            flags[flag] = flags.get(flag, 0) + 1

with OUT_SUMMARY.open("w", encoding="utf-8") as stream:
    stream.write(f"FILES: {len(files)}\n")
    stream.write(f"INVENTORY_RECORDS: {len(rows)}\n")
    for key in sorted(counts):
        stream.write(f"KIND {key}: {counts[key]}\n")
    for key in sorted(flags):
        stream.write(f"FLAG {key}: {flags[key]}\n")
    for key in sorted(decisions):
        stream.write(f"DECISION {key}: {decisions[key]}\n")
    stream.write("SIMPLIFICATION_RULES: ")
    stream.write(str(flags.get("simplification", 0)) + "\n")
    stream.write("FUNCTIONAL_DECLARATIONS: ")
    stream.write(str(flags.get("functional", 0)) + "\n")

print(OUT_SUMMARY.read_text(encoding="utf-8"), end="")
print(f"CSV: {OUT_CSV}")
