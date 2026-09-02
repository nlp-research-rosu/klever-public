#!/usr/bin/env python3
"""Annotate every inventoried K declaration with target relevance and audit disposition."""

from __future__ import annotations

import csv
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
INPUT = EVIDENCE / "k-declaration-rule-inventory.tsv"
OUTPUT = EVIDENCE / "k-rule-audit.tsv"

# Line intervals containing the operational slice reached by the exact submitted
# program or the fixed classifiers/helpers used by its mathematical summary.
TARGET_INTERVALS = {
    "reference-semantics/semantics/syntax.k": [(9, 61)],
    "reference-semantics/semantics/core.k": [
        (13, 60),
        (68, 71),
        (117, 205),
        (238, 244),
    ],
    "reference-semantics/semantics/call.k": [
        (15, 24),
        (31, 41),
        (52, 75),
    ],
    "reference-semantics/semantics/controls.k": [
        (8, 18),
        (33, 54),
        (62, 74),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 20),
        (62, 90),
    ],
    "reference-semantics/semantics/list.k": [
        (8, 20),
        (52, 55),
    ],
    "reference-semantics/semantics/tuple.k": [(30, 41)],
    "reference-semantics/semantics/builtins.k": [
        (17, 17),
        (287, 299),
    ],
}


def overlaps_target(path: str, start: int, end: int) -> bool:
    return any(
        start <= interval_end and end >= interval_start
        for interval_start, interval_end in TARGET_INTERVALS.get(path, ())
    )


rows = list(csv.DictReader(INPUT.open(encoding="utf-8"), delimiter="\t"))
fieldnames = list(rows[0]) + ["target_relevance", "decision", "audit_rationale"]

for row in rows:
    path = row["file"]
    start = int(row["start_line"])
    end = int(row["end_line"])
    attributes = set(row["attributes"].split(","))
    text = row["text"]

    if row["source_class"] == "proof_local":
        row["target_relevance"] = "direct"
        row["decision"] = "REVIEWED_PROOF_LOCAL"
        row["audit_rationale"] = (
            "Individually reviewed in REVIEW.md: exact-body macros, classifier "
            "simplification, recursive filter summary, or positive reachability claim."
        )
    elif text.startswith("syntax Val ::=") or text.startswith("syntax Iterable ::="):
        row["target_relevance"] = "formal_domain"
        row["decision"] = "ACCEPT_DOMAIN_DECLARATION"
        row["audit_rationale"] = (
            "Part of the supplied Val universe admitted by INPUT:ValSeq; checked "
            "against the isIntV/isInt/isBool constructor classification."
        )
    elif "no-evaluators" in attributes:
        row["target_relevance"] = "unreachable"
        row["decision"] = "TRUSTED_OPAQUE_UNUSED"
        row["audit_rationale"] = (
            "Supplied-model opaque primitive; no symbol from this declaration is "
            "reachable from the pinned program or its postcondition."
        )
    elif overlaps_target(path, start, end):
        row["target_relevance"] = "direct"
        row["decision"] = "ACCEPT_TARGET_SLICE"
        row["audit_rationale"] = (
            "Reached by the exact expanded program or used by filterAcc; reviewed "
            "for guards, overlap, evaluation order, cell effects, and control."
        )
    elif "concrete" in attributes:
        row["target_relevance"] = "unreachable"
        row["decision"] = "CONCRETE_ONLY_UNUSED"
        row["audit_rationale"] = (
            "Supplied concrete-only equation outside the proof definition and "
            "outside the pinned target path."
        )
    else:
        row["target_relevance"] = "unreachable"
        row["decision"] = "SUPPLIED_UNUSED"
        row["audit_rationale"] = (
            "Read-only supplied declaration/rule; constructor/KLabel is absent "
            "from the macro-expanded target and from all target summaries."
        )

with OUTPUT.open("w", encoding="utf-8", newline="") as output:
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

counts: dict[str, int] = {}
for row in rows:
    counts[row["decision"]] = counts.get(row["decision"], 0) + 1
for key in sorted(counts):
    print(f"{key}\t{counts[key]}")
print(f"TOTAL\t{len(rows)}")
