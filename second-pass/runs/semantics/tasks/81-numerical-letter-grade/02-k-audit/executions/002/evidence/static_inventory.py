#!/usr/bin/env python3
"""Lexical inventory of every outer K sentence in the supplied and proof files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


OUTER = re.compile(r"^\s*(configuration|syntax|rule|context|claim|alias)\b")
ATTRIBUTE = re.compile(r"\[([^\[\]]+)\]")


def decision(source_class: str, kind: str, start: int) -> tuple[str, str]:
    if source_class == "SUPPLIED_SEMANTICS":
        return (
            "ACCEPT_SELECTED_SUPPLIED_BASELINE",
            "Launcher-trusted supplied semantics; unchanged recursive byte comparison. "
            "Used-path rules receive additional manual review.",
        )
    if source_class == "SPEC":
        if kind == "claim":
            return (
                "PROOF_OBLIGATION",
                "Reachability claim, not an axiom; adequacy and circularity use reviewed separately.",
            )
        return ("ACCEPT_DECLARATION", "Spec module/import structure.")

    # Candidate verification.k decisions are deliberately source-line-specific.
    if start in {7, 8, 48, 49}:
        return (
            "ACCEPT_EXACT_PROGRAM_MACRO",
            "Macro expansion mechanically equals the trusted-regenerated constructor body.",
        )
    if start in {58, 59}:
        return (
            "ACCEPT_PINNED_INVOCATION_HARNESS",
            "Fresh proof-only entry constructor expands to an exact closure invocation.",
        )
    if start in {65, 66}:
        return (
            "ACCEPT_DEFINITIONAL_STRING_SUMMARY",
            "letter(S) is exactly the fixed semantics string representation.",
        )
    if start in {68, 69}:
        return (
            "MIXED_DECLARATION_REVIEW_ROWS_BELOW",
            "eqFour/above declarations are aliases; gpaEqFour is separately declared below.",
        )
    if start == 70:
        return (
            "REJECT_RESULT_BEARING_ORACLE",
            "Fresh total opaque Bool affects branch, returned grade, and postcondition.",
        )
    if start == 72:
        return (
            "REJECT_UNJUSTIFIED_OPERATIONAL_BRIDGE",
            "Preempts fixed Float equality without a bridge-free connection theorem.",
        )
    if start == 76:
        return (
            "REJECT_CIRCULAR_ALIAS",
            "Postcondition summary reuses the same unconstrained gpaEqFour atom.",
        )
    if start == 77:
        return (
            "ACCEPT_ALIAS_TO_FIXED_PRIMITIVE",
            "above is a direct name for the supplied gtF primitive.",
        )
    if start in {82, 85, 86, 90, 94}:
        return (
            "SYNTHETIC_INPUT_REPRESENTATION_GAP",
            "Defines/iterates proof-only numericValues terms; no fixed-semantics theorem "
            "connects them to real vCons input lists.",
        )
    if start == 99 or 100 <= start <= 190:
        return (
            "STRUCTURALLY_VALID_BUT_ORACLE_DEPENDENT",
            "Guard cascade mirrors program control, but A+ equality depends on gpaEqFour.",
        )
    if start in {204, 205, 206, 210}:
        return (
            "ACCEPT_STRUCTURAL_SUMMARY_WITH_DOMAIN_GAP",
            "Guard-free descending fold is internally valid over NumericGrades, "
            "but depends on proof-only input representation.",
        )
    if start in {215, 216, 217, 219}:
        return (
            "ACCEPT_STRUCTURAL_SUMMARY_WITH_DOMAIN_GAP",
            "Guard-free descending last-element fold is internally valid over NumericGrades.",
        )
    return ("MANUAL_REVIEW_REQUIRED", "Unclassified candidate-local sentence.")


def inventory_file(path: Path, source_class: str) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    starts = []
    for index, line in enumerate(lines, 1):
        match = OUTER.match(line)
        if match:
            starts.append((index, match.group(1)))
    rows = []
    for item_index, (start, kind) in enumerate(starts):
        next_start = starts[item_index + 1][0] if item_index + 1 < len(starts) else len(lines) + 1
        end = next_start - 1
        while end >= start and lines[end - 1].strip() in {"", "endmodule"}:
            end -= 1
        sentence = "\n".join(lines[start - 1 : end])
        attrs = []
        for match in ATTRIBUTE.finditer(sentence):
            attrs.extend(token.strip() for token in match.group(1).split(","))
        flags = [
            flag
            for flag in (
                "function",
                "functional",
                "total",
                "no-evaluators",
                "concrete",
                "priority",
                "simplification",
                "macro",
                "owise",
            )
            if flag in sentence
        ]
        disposition, rationale = decision(source_class, kind, start)
        rows.append(
            {
                "source": str(path),
                "source_class": source_class,
                "kind": kind,
                "start_line": start,
                "end_line": end,
                "sha256": hashlib.sha256(sentence.encode()).hexdigest(),
                "attributes": attrs,
                "flags": flags,
                "disposition": disposition,
                "rationale": rationale,
                "text": sentence,
            }
        )
    return rows


parser = argparse.ArgumentParser()
parser.add_argument("--json", action="store_true")
arguments = parser.parse_args()

rows: list[dict] = []
semantics_root = Path("/reference/reference-semantics")
for path in sorted(semantics_root.rglob("*.k")):
    rows.extend(inventory_file(path, "SUPPLIED_SEMANTICS"))
rows.extend(inventory_file(Path("/candidate/verification.k"), "PROOF_LOCAL"))
rows.extend(inventory_file(Path("/candidate/spec.k"), "SPEC"))

if arguments.json:
    print(json.dumps({"schema_version": 1, "sentences": rows}, indent=2, sort_keys=True))
else:
    counts: dict[tuple[str, str], int] = {}
    dispositions: dict[str, int] = {}
    for row in rows:
        key = (row["source_class"], row["kind"])
        counts[key] = counts.get(key, 0) + 1
        dispositions[row["disposition"]] = dispositions.get(row["disposition"], 0) + 1
    print(f"TOTAL_SENTENCES={len(rows)}")
    for key, count in sorted(counts.items()):
        print(f"COUNT source_class={key[0]} kind={key[1]} value={count}")
    for name, count in sorted(dispositions.items()):
        print(f"DISPOSITION name={name} value={count}")
    proof_rows = [row for row in rows if row["source_class"] == "PROOF_LOCAL"]
    print(f"PROOF_LOCAL_SENTENCES={len(proof_rows)}")
    for row in proof_rows:
        text_head = row["text"].splitlines()[0].strip()
        print(
            f"ROW line={row['start_line']}-{row['end_line']} kind={row['kind']} "
            f"flags={','.join(row['flags']) or '-'} "
            f"decision={row['disposition']} head={text_head}"
        )
    opaque = [
        row
        for row in rows
        if row["kind"] == "syntax" and "no-evaluators" in row["flags"]
    ]
    print(f"OPAQUE_DECLARATION_SENTENCES={len(opaque)}")
    for row in opaque:
        print(
            f"OPAQUE source={row['source']} line={row['start_line']} "
            f"head={row['text'].splitlines()[0].strip()}"
        )
    print("STATIC_INVENTORY_OK")
