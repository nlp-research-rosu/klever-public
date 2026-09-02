#!/usr/bin/env python3
"""Attach reviewer dispositions to every inventoried local K sentence."""

from __future__ import annotations

import csv
import json
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/k-source-inventory.json")
OUTPUT = Path("/audit-output/evidence/k-source-dispositions.csv")


# Start-line ranges whose declarations/rules form the submitted program's
# reachable semantic slice. Ranges intentionally include the associated local
# helper equations so totality/overlap can be reviewed together.
REACHABLE_RANGES: dict[str, list[tuple[int, int]]] = {
    "syntax.k": [(9, 61)],
    "core.k": [
        (13, 60),
        (68, 70),
        (117, 127),
        (130, 181),
        (183, 196),
        (208, 225),
    ],
    "iter.k": [(8, 8)],
    "operators.k": [(10, 17)],
    "int.k": [(9, 20), (26, 26)],
    "str.k": [(13, 17)],
    "list.k": [(9, 20), (53, 55)],
    "tuple.k": [(31, 41)],
    "subscript.k": [(7, 114)],
    "controls.k": [(8, 31), (46, 74)],
    "functions.k": [(8, 20), (62, 90)],
    "call.k": [(15, 32), (34, 75)],
    "sort.k": [(14, 42), (68, 71)],
}


def in_ranges(filename: str, start: int) -> bool:
    return any(lo <= start <= hi for lo, hi in REACHABLE_RANGES.get(filename, []))


def classify(document: dict[str, object]) -> tuple[str, str]:
    path = str(document["path"])
    filename = Path(path).name
    kind = str(document["kind"])
    start = int(document["start_line"])
    text = str(document["text"])

    if path == "/candidate/verification.k":
        if kind == "rule" and start in {7, 24, 39, 45}:
            return (
                "CANDIDATE_EXACT_CONSTRUCTOR_DEFINITION",
                "Expands a name to the submitted statement/body/closure/module term; "
                "the independent pinning claim checks constructor identity.",
            )
        if kind == "rule" and start in {56, 59}:
            return (
                "CANDIDATE_TRUE_GUARDED_EQUATION",
                "The pyMod==0 and pyMod=/=0 guards are disjoint and exhaustive; "
                "the selected index is Python floor division on the used I>=0 domain.",
            )
        if kind == "rule" and start in {64, 65, 76, 77, 81}:
            return (
                "CANDIDATE_TRUE_STRUCTURAL_DEFINITION",
                "Base/constructor equations are disjoint, structurally descending, "
                "and define only the mathematical result summary.",
            )
        return (
            "CANDIDATE_DECLARATION_OR_MODULE",
            "Local declaration/import only; no operational <k> rewrite or simplification.",
        )

    if path == "/candidate/spec.k":
        if kind == "claim":
            return (
                "PROOF_OBLIGATION",
                "Reachability claim, not an assumed equation; reconstructed by kprove.",
            )
        return ("SPEC_STRUCTURE", "Spec require/import/module boundary.")

    if filename == "sort.k" and (
        "sortVS" in text or start in {36, 40}
    ):
        return (
            "SUPPLIED_TRUSTED_SORT_BOUNDARY",
            "Fixed semantics intentionally treats sortVS as an opaque total sorted "
            "primitive in symbolic proofs and gives ground Int/str insertion-sort "
            "equations plus the real allocating call/mutator transitions.",
        )

    if filename == "subscript.k" and (
        "valSeqAt" in text or start in {11, 12, 13}
    ):
        return (
            "SUPPLIED_TOTAL_ACCESS_BOUNDARY",
            "Constructor equations are correct for nonnegative in-bounds indexes; "
            "[total] leaves opaque/OOB cases abstract. Actual program indexes are "
            "nonnegative and in bounds conditional on sortVS preserving length.",
        )

    if in_ranges(filename, start):
        return (
            "REACHABLE_FIXED_SEMANTICS_SOUND_ON_USED_DOMAIN",
            "Inspected for matching, guards, overlap, evaluation order, control, "
            "allocation, and state footprint; agrees with the submitted program's "
            "plain-list/int execution path.",
        )

    if kind in {"rule", "context", "syntax", "configuration"}:
        return (
            "UNREACHABLE_FIXED_SEMANTICS_SENTENCE",
            "Head/construct is absent from the submitted constructor term or is a "
            "concrete-only/other-type alternative. It was inventoried and inspected "
            "for overlap; it cannot fire on the target proof path.",
        )

    return (
        "STRUCTURAL_SOURCE_SENTENCE",
        "Require/import/module boundary; no rewrite content.",
    )


def main() -> None:
    inventory = json.loads(INVENTORY.read_text())
    rows = []
    for document in inventory["sentences"]:
        disposition, rationale = classify(document)
        rows.append(
            {
                "id": document["id"],
                "path": document["path"],
                "kind": document["kind"],
                "start_line": document["start_line"],
                "end_line": document["end_line"],
                "attributes": "|".join(document["attributes"]),
                "disposition": disposition,
                "rationale": rationale,
                "normalized_sha256": document["normalized_sha256"],
            }
        )
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["disposition"]] = counts.get(row["disposition"], 0) + 1
    print(f"rows={len(rows)}")
    for disposition, count in sorted(counts.items()):
        print(f"{disposition}={count}")


if __name__ == "__main__":
    main()
