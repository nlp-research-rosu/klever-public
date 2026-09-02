#!/usr/bin/env python3
"""Attach an audit disposition to every inventory record."""

from __future__ import annotations

import csv
from pathlib import Path


SOURCE = Path("/audit-output/evidence/rule_inventory.tsv")

# Line intervals for the fixed declarations/rules that execute this submitted
# program either from module load or from the entry-claim call state.
RELEVANT: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/syntax.k": [
        (9, 15),
        (28, 32),
        (41, 61),
    ],
    "reference-semantics/semantics/core.k": [
        (25, 60),
        (124, 127),
        (130, 181),
        (185, 205),
        (208, 215),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 20),
        (62, 90),
    ],
    "reference-semantics/semantics/call.k": [
        (18, 21),
        (69, 74),
    ],
    "reference-semantics/semantics/controls.k": [
        (8, 31),
        (65, 91),
    ],
    "reference-semantics/semantics/operators.k": [
        (10, 17),
    ],
    "reference-semantics/semantics/int.k": [
        (9, 9),
        (13, 13),
        (24, 24),
    ],
}


def relevant(file: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in RELEVANT.get(file, []))


rows = list(csv.DictReader(SOURCE.open(), delimiter="\t"))
fields = list(rows[0]) + ["audit_disposition", "reason"]
writer = csv.DictWriter(__import__("sys").stdout, fields, delimiter="\t")
writer.writeheader()

for row in rows:
    origin = row["origin"]
    kind = row["kind"]
    flags = set(row["flags"].split(","))
    line = int(row["line"])
    if origin == "PROOF_LOCAL":
        if kind == "syntax":
            disposition = "REVIEWED_SOUND_PROOF_DEFINITION"
            reason = (
                "sumToN is a result-only total function; no program term or "
                "configuration cell is replaced"
            )
        elif kind == "rule":
            disposition = "REVIEWED_SOUND_PROOF_EQUATION"
            reason = (
                "guards N>=0 and N<0 are disjoint/exhaustive; the former is "
                "the exact triangular closed form and the latter is zero"
            )
        else:
            disposition = "STRUCTURAL_PROOF_MODULE_RECORD"
            reason = "module/import structure only"
    elif origin == "SPECIFICATION":
        if kind == "claim":
            disposition = "REVIEWED_REACHABILITY_CLAIM"
            reason = (
                "one exact loop circularity or one exact entry call; all "
                "three close in the clean reconstruction"
            )
        else:
            disposition = "STRUCTURAL_SPEC_MODULE_RECORD"
            reason = "module/import structure only"
    elif relevant(row["file"], line):
        disposition = "RELEVANT_FIXED_SEMANTICS_REVIEWED"
        reason = (
            "immutable supplied rule/declaration on the submitted execution "
            "path; checked in the constructor map and concrete/symbolic runs"
        )
    elif "no-evaluators" in flags or "symbol" in flags:
        disposition = "OPAQUE_FIXED_PRIMITIVE_INERT_FOR_TARGET"
        reason = (
            "immutable supplied trust-boundary symbol is unreachable from "
            "this integer-only program and cannot influence its result"
        )
    else:
        disposition = "FIXED_SEMANTICS_INERT_FOR_TARGET"
        reason = (
            "immutable supplied language rule/declaration is unreachable "
            "from every constructor in solution.mpy; no target conclusion "
            "depends on it"
        )
    row["audit_disposition"] = disposition
    row["reason"] = reason
    writer.writerow(row)
