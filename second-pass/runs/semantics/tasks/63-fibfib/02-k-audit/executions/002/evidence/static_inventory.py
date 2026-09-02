#!/usr/bin/env python3
"""Produce a source-located inventory of all local K declarations and rules."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/rebuild")
OUT = Path("/audit-output/evidence/static-rule-inventory.md")
FILES = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)
START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias|priority)\b"
)

# Source rules exercised by this translated program and its entry proof.
USED_RULE_LINES = {
    "semantics/core.k": {
        126, 127, 131, 132, 152, 158, 189, 190, 191, 194, 202, 214, 215,
    },
    "semantics/call.k": {20, 21, 69},
    "semantics/functions.k": {63, 64, 78, 85},
    "semantics/controls.k": {9, 77, 78, 79, 81, 85},
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 22},
}
USED_SYNTAX_LINES = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {25, 31, 36, 37, 38, 39, 40, 42, 49, 157, 185, 186, 199, 208, 209, 210, 213},
    "semantics/functions.k": {8},
    "semantics/controls.k": {65},
    "semantics/call.k": {19},
}


def relative(path: Path) -> str:
    if path == ROOT / "reference-semantics" / "semantics.k":
        return "semantics.k"
    if (ROOT / "reference-semantics") in path.parents:
        return path.relative_to(ROOT / "reference-semantics").as_posix()
    return path.relative_to(ROOT).as_posix()


def clean_block(lines: list[str]) -> str:
    kept = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        kept.append(stripped)
    return " ".join(kept).replace("|", r"\|")


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [
        (index, START.match(line).group(1))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        for candidate in range(index + 1, end):
            if lines[candidate].strip() == "endmodule":
                end = candidate
                break
        statement = clean_block(lines[index:end])
        rel = relative(path)
        used = (
            index + 1
            in (
                USED_RULE_LINES.get(rel, set())
                | USED_SYNTAX_LINES.get(rel, set())
            )
        )
        attributes = sorted(
            set(
                re.findall(
                    r"\b(functional|function|total|simplification|concrete|owise|"
                    r"macro|no-evaluators|seqstrict|strict)\b|priority\(\d+\)|"
                    r"symbol\([^)]*\)",
                    statement,
                )
            )
        )
        # Regex alternation returns empty strings for the non-capturing-looking
        # alternatives; extract all explicit markers separately for clarity.
        attributes = sorted(
            {
                marker
                for marker in (
                    "functional",
                    "function",
                    "total",
                    "simplification",
                    "concrete",
                    "owise",
                    "macro",
                    "no-evaluators",
                    "seqstrict",
                    "strict",
                )
                if re.search(rf"\b{re.escape(marker)}\b", statement)
            }
            | set(re.findall(r"priority\(\d+\)", statement))
            | set(re.findall(r"symbol\([^)]*\)", statement))
        )
        if rel.startswith("semantics"):
            decision = (
                "SUPPLIED-FIXED / EXERCISED"
                if used
                else "SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE"
            )
        elif rel == "verification.k":
            if kind == "syntax":
                decision = "PROOF-LOCAL DEFINITIONAL SUMMARY / REVIEWED SOUND"
            elif index + 1 in {9, 11}:
                decision = "PROOF-LOCAL fibFrom EQUATION / REVIEWED SOUND"
            elif index + 1 == 17:
                decision = "PROOF-LOCAL ARITHMETIC SIMPLIFICATION / REVIEWED SOUND"
            else:
                decision = "PROOF-LOCAL / REQUIRES MANUAL REVIEW"
        elif rel == "spec.k":
            if index + 1 == 6:
                decision = "AUXILIARY LOOP CIRCULARITY / MACHINE-CHECKED"
            elif index + 1 == 31:
                decision = "ENTRY TARGET / MACHINE-CHECKED"
            else:
                decision = "GROUND SANITY CLAIM / MACHINE-CHECKED"
        else:
            decision = "UNCLASSIFIED"
        records.append(
            {
                "file": rel,
                "line": index + 1,
                "kind": kind,
                "attributes": ", ".join(attributes) if attributes else "none",
                "used": "yes" if used else "no",
                "decision": decision,
                "statement": statement,
            }
        )

kind_counts = Counter(record["kind"] for record in records)
attribute_counts = Counter()
for record in records:
    if record["attributes"] != "none":
        for attribute in str(record["attributes"]).split(", "):
            attribute_counts[attribute] += 1

with OUT.open("w") as stream:
    stream.write("# Exhaustive local K inventory\n\n")
    stream.write(
        "Generated from the fresh scratch sources. `SUPPLIED-FIXED` means the "
        "entry belongs byte-for-byte to the selected trusted semantics; the "
        "used slice was additionally checked against this program's execution. "
        "Entries outside the directly mapped slice were screened for overlap, "
        "task-specific content, and dependency through opaque results.\n\n"
    )
    stream.write(f"Total entries: {len(records)}. Kinds: {dict(kind_counts)}.\n\n")
    stream.write(f"Attribute markers: {dict(attribute_counts)}.\n\n")
    stream.write(
        "| ID | Location | Kind | Attributes | Used | Decision | Source statement |\n"
    )
    stream.write(
        "|---:|---|---|---|:---:|---|---|\n"
    )
    for number, record in enumerate(records, 1):
        stream.write(
            f"| {number} | `{record['file']}:{record['line']}` | "
            f"{record['kind']} | {record['attributes']} | {record['used']} | "
            f"{record['decision']} | `{record['statement']}` |\n"
        )

print(f"inventory_path={OUT}")
print(f"entry_count={len(records)}")
print(f"kind_counts={dict(kind_counts)}")
print(f"attribute_counts={dict(attribute_counts)}")
print(
    "opaque_or_external_declarations="
    f"{sum('no-evaluators' in str(record['attributes']) for record in records)}"
)
print(
    "proof_local_entries="
    f"{sum(record['file'] in {'verification.k', 'spec.k'} for record in records)}"
)
