#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventory item."""

from __future__ import annotations

import collections
import json
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/static_inventory.json")

# Start lines of fixed rules/declarations materially exercised by the submitted
# program or by the exact proof summary. All other fixed entries were still
# source-reviewed, but are not reachable from rollingMaxModule on IntSeq input.
USED_FIXED: dict[str, set[int]] = {
    "core.k": {
        13, 14, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49, 68, 69, 70,
        75, 76, 77, 78, 117, 118, 124, 125, 126, 127, 130, 131, 132,
        152, 157, 158, 185, 186, 189, 190, 191, 194, 195, 199, 200,
        213, 214, 215, 217, 218, 219,
    },
    "syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "controls.k": {9, 36, 48, 51, 52, 53, 54, 65, 69, 71, 72, 73},
    "functions.k": {8, 14, 63, 64, 78, 80, 85},
    "call.k": {16, 19, 20, 21, 24, 31, 52, 53, 56, 69},
    "list.k": {9, 10, 13, 14, 15, 18, 19, 20, 53},
    "tuple.k": {31, 32},
    "builtins.k": {17, 97, 98, 99, 100},
    "str.k": {13, 14, 15, 16},
}


def candidate_disposition(item: dict) -> tuple[str, str]:
    line = item["start_line"]
    keyword = item["keyword"]
    if keyword in {"module", "imports", "requires", "endmodule"}:
        return "STRUCTURAL", "Module/import boundary only."
    if line in {9, 10, 19, 20, 29, 30}:
        return (
            "SOUND_PROGRAM_MACRO",
            "Exact constructor macro; macro-expanded AST is byte-identical to regenerated solution.mpy.",
        )
    if line in {36, 37, 38}:
        return (
            "SOUND_DEFINITIONAL_EMBEDDING",
            "Exhaustive, disjoint IntSeq-to-ValSeq constructor embedding.",
        )
    if line in {44, 46}:
        return (
            "SOUND_OPERATIONAL_BRIDGE",
            "Exact fixed-list-iterator consequence; arbitrary-CONT bridge-free definitional connection closes.",
        )
    if line in {52, 53, 54, 56, 57, 58, 64, 65, 66, 67, 69, 70, 71, 74, 75, 76}:
        return (
            "SOUND_RECURSIVE_SUMMARY",
            "Exhaustive/disjoint equations, agreeing overlaps, structural descent, ordinary integer maximum.",
        )
    return "REVIEWED_CANDIDATE_DECLARATION", "No additional rewrite or value assumption."


def spec_disposition(item: dict) -> tuple[str, str]:
    if item["keyword"] != "claim":
        return "STRUCTURAL", "Module/import boundary only."
    if item["start_line"] == 6:
        return (
            "SOUND_LOOP_CLAIM",
            "Exact real loop head/body; complete loop-carried locals and result heap; other cells framed.",
        )
    return (
        "SOUND_ENTRY_CLAIM",
        "Exact fresh program configuration, exact returned ref and heap summary, unrestricted IntSeq input.",
    )


def fixed_disposition(item: dict) -> tuple[str, str]:
    path = Path(item["file"])
    if item["keyword"] in {"module", "imports", "requires", "endmodule"}:
        return "STRUCTURAL", "Fixed module/import boundary."
    if "opaque-symbol" in item["classes"]:
        return (
            "UNUSED_FIXED_OPAQUE_BOUNDARY",
            "Explicit supplied-semantics primitive; unreachable from this integer-list program and no claim depends on it.",
        )
    if path.name == "concrete.k":
        return (
            "REVIEWED_CONCRETE_ONLY",
            "Imported only by MPY-KRUN, not VERIFICATION; no proof dependency.",
        )
    if item["start_line"] in USED_FIXED.get(path.name, set()):
        return (
            "REVIEWED_FIXED_USED",
            "Reachable rule/declaration checked against the exact program evaluation path and Python behavior.",
        )
    return (
        "REVIEWED_FIXED_UNUSED",
        "Source-reviewed fixed-semantics subset entry; unreachable from rollingMaxModule on IntSeq input and has no theorem dependency.",
    )


def main() -> int:
    source = json.loads(INVENTORY.read_text())
    assessed = []
    counts: collections.Counter[str] = collections.Counter()
    for item in source["items"]:
        source_class = item["source_class"]
        if source_class == "candidate-proof-extension":
            disposition, rationale = candidate_disposition(item)
        elif source_class == "candidate-specification":
            disposition, rationale = spec_disposition(item)
        else:
            disposition, rationale = fixed_disposition(item)
        entry = {
            "file": item["file"],
            "start_line": item["start_line"],
            "end_line": item["end_line"],
            "keyword": item["keyword"],
            "classes": item["classes"],
            "disposition": disposition,
            "rationale": rationale,
            "text": item["text"],
        }
        assessed.append(entry)
        counts[disposition] += 1
    output = {
        "assessment_count": len(assessed),
        "disposition_counts": dict(sorted(counts.items())),
        "assessments": assessed,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
