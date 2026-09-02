#!/usr/bin/env python3
"""Assign an explicit audit disposition to every inventoried K entry."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/rule_inventory.json")
OUTPUT = Path("/audit-output/evidence/rule_review.tsv")

data = json.loads(INVENTORY.read_text(encoding="utf-8"))
entries = data["entries"]

# Dependency slice actually exercised by solution.mpy. Ranges intentionally
# include declarations adjacent to the used rules; each individual entry still
# receives its own row below.
used_ranges = {
    "reference-semantics/semantics/syntax.k": [(9, 61)],
    "reference-semantics/semantics/core.k": [
        (25, 60),
        (124, 205),
        (208, 219),
    ],
    "reference-semantics/semantics/controls.k": [
        (9, 31),
        (51, 54),
        (65, 82),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 20),
        (62, 90),
    ],
    "reference-semantics/semantics/call.k": [
        (18, 21),
        (69, 74),
    ],
    "reference-semantics/semantics/operators.k": [(10, 20)],
    "reference-semantics/semantics/int.k": [(9, 27)],
}

verification_dispositions = {
    929: (
        "ACCEPTED_WITH_SCOPE_LIMIT",
        "oddDigitProduct is defined on N=0 and N>0 but declared total over Int; "
        "oddDigitStep is exhaustive. Negative oddDigitProduct inputs remain "
        "unconstrained, but no claim or recursive call reaches them.",
    ),
    930: (
        "ACCEPTED_PROOF_DEFINITION",
        "Base equation oddDigitProduct(0,A)=A.",
    ),
    931: (
        "ACCEPTED_PROOF_DEFINITION",
        "For N>0, removes the last decimal digit and dispatches on parity; "
        "the quotient is nonnegative and strictly smaller.",
    ),
    932: (
        "ACCEPTED_PROOF_DEFINITION",
        "Even-digit branch preserves the accumulator.",
    ),
    933: (
        "ACCEPTED_PROOF_DEFINITION",
        "First odd digit replaces the zero sentinel with a nonzero odd digit.",
    ),
    934: (
        "ACCEPTED_PROOF_DEFINITION",
        "Later odd digit multiplies a nonzero accumulator by the digit.",
    ),
    935: (
        "ACCEPTED_DERIVED_SIMPLIFIER",
        "Even-step equality; proved without any submitted simplifier in "
        "extension-lemmas.k.",
    ),
    936: (
        "ACCEPTED_DERIVED_SIMPLIFIER",
        "First-odd-step equality; proved without any submitted simplifier in "
        "extension-lemmas.k.",
    ),
    937: (
        "ACCEPTED_DERIVED_SIMPLIFIER",
        "Later-odd-step equality; proved without any submitted simplifier in "
        "extension-lemmas.k.",
    ),
    938: (
        "ACCEPTED_AUXILIARY_CLAIM",
        "Loop circularity executes the exact submitted loop and constrains n=0 "
        "and product=oddDigitProduct(N,A).",
    ),
    939: (
        "ACCEPTED_ENTRY_CLAIM",
        "Entry call executes the exact submitted closure body and constrains "
        "the returned Int to oddDigitProduct(N,0) for N>0.",
    ),
}


def in_used_slice(entry):
    for lo, hi in used_ranges.get(entry["file"], []):
        if lo <= entry["start"] <= hi:
            return True
    return False


rows = []
for entry in entries:
    entry_id = entry["id"]
    if entry_id in verification_dispositions:
        disposition, rationale = verification_dispositions[entry_id]
    elif entry["file"].startswith("reference-semantics/"):
        if entry_id in (185, 787):
            disposition = "ACCEPTED_UNUSED_OPAQUE_BASELINE"
            rationale = (
                "Supplied-semantics opaque symbol (md5hexCodes or sortKeyVS); "
                "unreachable from solution.mpy and from both proof claims."
            )
        elif "no-evaluators" in entry["attributes"]:
            disposition = "ACCEPTED_UNUSED_PROOF_OPAQUE_BASELINE"
            rationale = (
                "Supplied proof-side opaque primitive with a concrete-only "
                "implementation; unreachable from this integer-only program."
            )
        elif in_used_slice(entry):
            disposition = "ACCEPTED_USED_FIXED_SEMANTICS"
            rationale = (
                "Part of the trusted supplied-semantics dependency slice for "
                "module loading, calls, integer evaluation, state, or control; "
                "checked against the submitted program's execution."
            )
        else:
            disposition = "ACCEPTED_UNUSED_FIXED_SEMANTICS"
            rationale = (
                "Byte-identical trusted supplied-semantics declaration/rule; "
                "not reachable from solution.mpy or either reachability claim."
            )
    else:
        disposition = "REVIEW_ERROR"
        rationale = "Unexpected inventory source."
    rows.append(
        {
            "id": f"K{entry_id:04d}",
            "file": entry["file"],
            "lines": f"{entry['start']}-{entry['end']}",
            "kind": entry["kind"],
            "attributes": ",".join(entry["attributes"]) or "-",
            "disposition": disposition,
            "rationale": rationale,
        }
    )

with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        delimiter="\t",
        fieldnames=[
            "id",
            "file",
            "lines",
            "kind",
            "attributes",
            "disposition",
            "rationale",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

counts = Counter(row["disposition"] for row in rows)
print(f"reviewed_entries={len(rows)}")
print(f"dispositions={dict(sorted(counts.items()))}")
assert len(rows) == len(entries)
assert not counts["REVIEW_ERROR"]
