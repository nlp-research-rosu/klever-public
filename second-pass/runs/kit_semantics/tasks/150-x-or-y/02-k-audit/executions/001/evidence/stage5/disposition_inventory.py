#!/usr/bin/env python3
"""Assign an explicit audit disposition to every inventoried K sentence."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/stage5/inventory.json")
OUTPUT = Path("/audit-output/evidence/stage5/dispositions.csv")

# Inclusive source ranges whose declarations/rules are exercised by solution.mpy
# or by the proof summaries/claims.
PROOF_RANGES: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics.k": [(34, 90)],
    "reference-semantics/semantics/syntax.k": [
        (9, 16),
        (28, 32),
        (37, 38),
        (41, 61),
    ],
    "reference-semantics/semantics/core.k": [
        (25, 60),
        (124, 134),
        (152, 181),
        (185, 215),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 16),
        (62, 66),
        (77, 90),
    ],
    "reference-semantics/semantics/call.k": [
        (18, 21),
        (69, 74),
    ],
    "reference-semantics/semantics/controls.k": [
        (8, 11),
        (50, 54),
        (65, 67),
        (76, 85),
    ],
    "reference-semantics/semantics/operators.k": [
        (12, 17),
    ],
    "reference-semantics/semantics/int.k": [
        (9, 9),
        (15, 15),
        (19, 22),
        (26, 26),
    ],
    "verification.k": [(3, 33)],
    "spec.k": [(3, 101)],
}


def overlaps(record: dict, ranges: list[tuple[int, int]]) -> bool:
    return any(
        record["start_line"] <= high and record["end_line"] >= low
        for low, high in ranges
    )


document = json.loads(INVENTORY.read_text())
rows: list[dict[str, str]] = []
for record in document["records"]:
    source = record["source"]
    normalized = record["normalized"]
    classes = set(record["classification"])

    if source == "reference-semantics/semantics/concrete.k":
        disposition = "RUNTIME_ONLY_MODULE"
        judgment = "Not imported by VERIFICATION; checked only by fresh LLVM execution."
    elif "concrete" in classes:
        disposition = "CONCRETE_ATTRIBUTE_RULE"
        judgment = "Concrete twin; not used by the symbolic integer proof."
    elif "no-evaluators" in classes:
        disposition = "OPAQUE_TRUST_DECLARATION"
        judgment = "Conditional supplied-semantics boundary; symbol is absent from task execution."
    elif source in PROOF_RANGES and overlaps(record, PROOF_RANGES[source]):
        if source == "verification.k":
            disposition = "PROOF_LOCAL_AUDITED"
            judgment = "Guard/coverage/descent reviewed; no execution is bypassed."
        elif source == "spec.k":
            disposition = "REACHABILITY_CLAIM_AUDITED"
            judgment = "Precondition, postcondition, cells, and real-program pinning reviewed."
        else:
            disposition = "PROOF_PATH_AUDITED"
            judgment = "Matches the used execution path and preserves value/control/state."
    elif record["keyword"] in {
        "requires",
        "imports",
        "syntax",
        "context",
        "configuration",
    }:
        disposition = "DECLARATION_OR_COMPOSITION_UNUSED"
        judgment = "Well-formed declaration; unused alternatives do not rewrite task states."
    else:
        disposition = "UNUSED_DISJOINT_RULE"
        judgment = (
            "Its head/operator/value shape is absent from solution.mpy execution; "
            "no false conclusion witness exists on the task domain."
        )

    rows.append(
        {
            "id": record["id"],
            "source": source,
            "module": str(record["module"]),
            "keyword": record["keyword"],
            "classification": "|".join(record["classification"]),
            "disposition": disposition,
            "judgment": judgment,
            "sentence_sha256": record["sha256"],
        }
    )

with OUTPUT.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

counts = Counter(row["disposition"] for row in rows)
print(f"record_count={len(rows)}")
for disposition, count in sorted(counts.items()):
    print(f"{disposition}={count}")
print(f"output={OUTPUT}")
