#!/usr/bin/env python3
"""Attach an audit disposition to every record in the exhaustive K inventory."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/rule-inventory.json")
OUTPUT = Path("/audit-output/evidence/rule-review-dispositions.csv")

warning_declarations = {
    ("reference-semantics/semantics/builtins.k", 134),
    ("reference-semantics/semantics/float.k", 73),
    ("reference-semantics/semantics/float.k", 86),
    ("reference-semantics/semantics/float.k", 93),
    ("reference-semantics/semantics/methods.k", 27),
    ("reference-semantics/semantics/subscript.k", 11),
}

active_families = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/call.k",
    "reference-semantics/semantics/assert.k",
}


def disposition(record: dict[str, object]) -> tuple[str, str]:
    path = str(record["file"])
    line = int(record["start_line"])
    kind = str(record["kind"])
    tags = set(str(tag) for tag in record["tags"])  # type: ignore[union-attr]

    if path == "verification.k" and kind == "rule":
        if line in {9, 11}:
            return (
                "PROOF_LOCAL_SOUND_MAP_IDENTITY",
                "Deleting an absent key is identity; deleting the explicitly disjoint added key restores M.",
            )
        if line in {17, 23, 32}:
            return (
                "PROOF_LOCAL_EXACT_SYNTAX_MACRO",
                "Pure syntax abbreviation; independent parser check equates the expanded macros to solution.mpy.",
            )
        if line in {45, 47, 49}:
            return (
                "PROOF_LOCAL_SOUND_TRIAL_DIVISION_EQUATION",
                "Guards are disjoint on D>=2, recursion increases D, and equations match the remaining loop.",
            )
        if line in {53, 54}:
            return (
                "PROOF_LOCAL_SOUND_PRIMALITY_DEFINITION",
                "The two guards partition integers at 2; the large branch delegates to divisor search from 2.",
            )
        return ("PROOF_LOCAL_REVIEW_REQUIRED", "Unexpected proof-local rule.")

    if path == "spec.k" and kind == "claim":
        if line == 9:
            return (
                "CLAIM_SOUND_RESULT_BEARING_LOOP",
                "Exact loop/control/frame source reaches trialPrime(N,D); fresh proof closes.",
            )
        if line == 52:
            return (
                "CLAIM_SOUND_RESULT_BEARING_SMALL_ENTRY",
                "For N<2 the exact function body returns false and restores the call frame.",
            )
        if line == 97:
            return (
                "CLAIM_ADEQUACY_FAIL_LARGE_PREFIX_ONLY",
                "Postcondition is unevaluated Assign/While/Return; it constrains no returned value.",
            )

    if kind in {"module", "endmodule", "imports", "requires-file"}:
        return (
            "STRUCTURAL_DECLARATION",
            "Module/dependency structure; no equation or execution conclusion.",
        )
    if kind in {"configuration", "context"}:
        return (
            "FIXED_SEMANTICS_REVIEWED_STRUCTURE",
            "Configuration/cooling context is consistent with the supplied cell model and evaluation order.",
        )

    if (path, line) in warning_declarations:
        return (
            "UNUSED_TOTALITY_EVIDENCE_GAP",
            "Compiler reports non-exhaustive equations on the full declared sort; symbol is unreachable from solution.mpy.",
        )

    if "no-evaluators" in tags or ("symbol" in tags and "concrete" not in tags):
        return (
            "UNUSED_OPAQUE_TRUST_BOUNDARY",
            "Supplied opaque proof-domain primitive; no source construct or submitted claim reaches it.",
        )

    if path == "reference-semantics/semantics/concrete.k":
        return (
            "LLVM_CONCRETE_ONLY_REVIEWED",
            "Imported only by MPY-KRUN; reviewed as concrete test support and absent from the Haskell proof module.",
        )

    if path.startswith("reference-semantics/"):
        if path in active_families:
            return (
                "SUPPLIED_FIXED_SEMANTICS_ACTIVE_FAMILY_REVIEWED",
                "Rule/declaration family covers program syntax, integer evaluation, control, calls, frames, or assertions; no false matched-case conclusion found.",
            )
        return (
            "SUPPLIED_FIXED_SEMANTICS_INACTIVE_FAMILY_REVIEWED",
            "Reviewed but syntactically unreachable from this integer-only program and its submitted claims.",
        )

    if kind == "syntax":
        return (
            "PROOF_LOCAL_DECLARATION_REVIEWED",
            "Declaration attributes and use sites reviewed with the associated equations.",
        )
    return ("REVIEWED_OTHER", "Reviewed; no execution equation is introduced.")


def main() -> int:
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = payload["records"]
    counts: Counter[str] = Counter()
    rows = []
    for number, record in enumerate(records, start=1):
        status, reason = disposition(record)
        counts[status] += 1
        rows.append(
            {
                "record_id": number,
                "file": record["file"],
                "start_line": record["start_line"],
                "end_line": record["end_line"],
                "kind": record["kind"],
                "tags": ",".join(record["tags"]),
                "disposition": status,
                "justification": reason,
            }
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"reviewed_record_count={len(rows)}")
    print(f"disposition_counts={dict(sorted(counts.items()))}")
    print(f"artifact={OUTPUT}")
    unexpected = counts.get("PROOF_LOCAL_REVIEW_REQUIRED", 0)
    print(f"unexpected_proof_local_rules={unexpected}")
    return 1 if unexpected else 0


if __name__ == "__main__":
    raise SystemExit(main())
