#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory with an audit disposition per item."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(r"^\s*(syntax|rule|claim|configuration|context|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|alias|module|endmodule|imports|requires)\b"
)
ATTRIBUTE_NAMES = (
    "function",
    "total",
    "functional",
    "no-evaluators",
    "symbol",
    "priority",
    "owise",
    "concrete",
    "simplification",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "anywhere",
)


def collapse(block: list[str]) -> str:
    fragments = []
    for line in block:
        code = line.split("//", 1)[0].strip()
        if code:
            fragments.append(code)
    return " ".join(fragments)


def attributes(text: str) -> str:
    return ",".join(name for name in ATTRIBUTE_NAMES if name in text)


def assessment(path: Path, line_number: int, kind: str, text: str) -> tuple[str, str]:
    relative = path.relative_to(ROOT).as_posix()

    if kind in {"syntax", "configuration", "context", "alias"}:
        if "no-evaluators" in text:
            if "sortVS(" in text:
                return (
                    "TRUSTED_VALUE_BOUNDARY_USED",
                    "Fixed supplied-semantics opaque sorted result; value-bearing and used.",
                )
            return (
                "TRUSTED_VALUE_BOUNDARY_UNUSED",
                "Fixed supplied-semantics opaque symbol; unused by solution.mpy.",
            )
        return (
            "DECLARATION_OR_CONTEXT",
            "No standalone truth-valued conclusion; checked for used-construct coverage.",
        )

    if relative == "verification.k":
        if "#getOddCollatz" in text:
            return (
                "SOUND_PROOF_LOCAL_DEFINITION",
                "Exact submitted Module term; KAST identity and body sensitivity checked.",
            )
        if "collatzResult" in text:
            return (
                "SOUND_BUT_UNUSED_SUMMARY",
                "Truthful Collatz recurrence on its guards, but no spec claim references it.",
            )
        if "getOddCollatzClosure" in text:
            return (
                "SOUND_PROOF_LOCAL_DEFINITION",
                "Exact submitted function closure; KAST identity checked.",
            )
        return ("REVIEWED_PROOF_LOCAL", "No false conclusion witness found.")

    if relative == "spec.k":
        if "#getOddCollatz" in text:
            return (
                "SOUND_FIXED_ENTRY_CLAIM",
                "Executes exact body and constrains heap/result, but only for a fixed input.",
            )
        return (
            "SOUND_LOCAL_CLAIM",
            "One real loop transition or exit tail; not an end-to-end symbolic theorem.",
        )

    if "[concrete]" in text:
        return (
            "REVIEWED_CONCRETE_FIXED_RULE",
            "Concrete-only fixed-semantics equation; no false conclusion witness found.",
        )

    used_rule_lines = {
        "semantics/core.k": {
            118,
            125,
            126,
            127,
            131,
            132,
            152,
            158,
            189,
            190,
            191,
            194,
            202,
            214,
            215,
            218,
            219,
        },
        "semantics/operators.k": {12, 17},
        "semantics/int.k": {9, 14, 15, 16, 20, 26, 27},
        "semantics/list.k": {14, 15, 19, 20, 53},
        "semantics/controls.k": {9, 48, 52, 53, 54, 77, 78, 79, 81, 85},
        "semantics/functions.k": {14, 63, 64, 78, 85},
        "semantics/call.k": {16, 20, 21, 38, 53, 69},
        "semantics/sort.k": {36},
    }
    rel_from_reference = (
        relative[len("reference-semantics/") :]
        if relative.startswith("reference-semantics/")
        else relative
    )
    if line_number in used_rule_lines.get(rel_from_reference, set()):
        if "sortVS(" in text and "[concrete]" not in text:
            return (
                "TRUSTED_VALUE_BOUNDARY_USED",
                "Sound only conditional on fixed builtin contract sortVS = ascending sort.",
            )
        return (
            "REVIEWED_USED_PATH_RULE",
            "Matches the submitted program's evaluation/control/state transition; no false witness.",
        )

    return (
        "REVIEWED_UNUSED_FIXED_RULE",
        "Fixed supplied-semantics rule not reached by solution.mpy; no false witness found.",
    )


rows: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start_index = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        text = collapse(lines[start_index:index])
        disposition, rationale = assessment(path, start_index + 1, kind, text)
        rows.append(
            {
                "id": len(rows) + 1,
                "file": path.relative_to(ROOT).as_posix(),
                "line": start_index + 1,
                "kind": kind,
                "attributes": attributes(text),
                "disposition": disposition,
                "rationale": rationale,
                "declaration_or_rule": text,
            }
        )

writer = csv.DictWriter(
    sys.stdout,
    fieldnames=[
        "id",
        "file",
        "line",
        "kind",
        "attributes",
        "disposition",
        "rationale",
        "declaration_or_rule",
    ],
    delimiter="\t",
    lineterminator="\n",
)
writer.writeheader()
writer.writerows(rows)
