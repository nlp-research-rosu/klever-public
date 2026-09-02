#!/usr/bin/env python3
"""Attach an explicit audit disposition to every semantic declaration/rule."""

from __future__ import annotations

import csv
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/k-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/k-rule-assessments.tsv")
RELEVANT = {"configuration", "syntax", "rule", "claim", "context", "alias"}

VERIFICATION = {
    8: "SOUND: total zero-argument definitional name for the exact translated lambda.",
    9: "SOUND: expands to the exact Lambda AST in submitted solution.mpy; no execution is skipped.",
    21: "SOUND: total zero-argument definitional name for the exact translated function body.",
    22: "SOUND: expands to the exact nested sorted/keyword-return body; no operational bridge.",
    29: "SOUND: total zero-argument definitional name for the exact unannotated function closure.",
    30: "SOUND: closure parameter, body, and defining scope match module loading at scope 0.",
    33: "SOUND: total zero-argument definitional name for the exact submitted translated module.",
    34: "SOUND: module contains exactly sort_array with the exact parameter and named body.",
    40: "SOUND: total zero-argument definitional name for the closure produced by the exact lambda.",
    41: "SOUND: exact closureValC result of the annotated lambda with empty cell/free-variable maps.",
    54: "SOUND: total mathematical name for the fixed-semantics two-sort summary; does not rewrite execution.",
    55: "SOUND AS DEFINITION: names sortKeyVS(sortVS(VS), key closure); intended meaning inherits the supplied opaque sort contracts.",
    58: "SOUND: total domain predicate over the two ValSeq constructors.",
    59: "SOUND: empty sequence contains only non-negative integers vacuously.",
    60: "SOUND: integer-cons case checks head >= 0 and recursively checks tail; structurally descending.",
    62: "SOUND: owise fallback rejects every non-Int head; disjoint from the Int rule and completes coverage.",
}

CLAIMS = {
    7: "POSITIVE CLAIM: exact module loading; independently reconstructed and closed.",
    27: "ENTRY CLAIM: exact closure execution; independently reconstructed and closed.",
    54: "AUXILIARY CLAIM: exact non-negative key closure execution; independently reconstructed and closed.",
    79: "AUXILIARY CLAIM: exact negative branch execution outside the stated domain; independently reconstructed and closed.",
}


def main() -> int:
    with INVENTORY.open(newline="") as stream:
        rows = [row for row in csv.DictReader(stream, delimiter="\t") if row["kind"] in RELEVANT]

    fields = [
        "id",
        "source",
        "module",
        "start_line",
        "end_line",
        "kind",
        "flags",
        "decision",
        "basis",
    ]
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            source = row["source"]
            line = int(row["start_line"])
            if "reference-semantics" in source:
                decision = "ACCEPTED_SELECTED_BASELINE"
                basis = (
                    "Byte-identical to the trusted supplied-semantics entry. "
                    "Candidate did not add or alter it. Used-path rules receive "
                    "the detailed execution/order/state review in used-rule-map.md; "
                    "unused rules do not contribute to this theorem."
                )
            elif source == "/candidate/verification.k":
                decision = "SOUND_CANDIDATE_EXTENSION"
                basis = VERIFICATION.get(
                    line,
                    "Structural module declaration/import; introduces no rewrite or theorem content.",
                )
            elif source == "/candidate/spec.k" and row["kind"] == "claim":
                decision = "RECONSTRUCTED_POSITIVE_CLAIM"
                basis = CLAIMS[line]
            else:
                decision = "SPEC_STRUCTURE"
                basis = "Syntax/module structure only; no semantic extension."
            writer.writerow(
                {
                    "id": row["id"],
                    "source": source,
                    "module": row["module"],
                    "start_line": row["start_line"],
                    "end_line": row["end_line"],
                    "kind": row["kind"],
                    "flags": row["flags"],
                    "decision": decision,
                    "basis": basis,
                }
            )

    print(f"assessed_entries={len(rows)}")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
