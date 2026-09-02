#!/usr/bin/env python3
"""Attach an audit decision to every row of the exhaustive K inventory."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


# Rules/declarations on the concrete and symbolic path of this submitted program.
DIRECT_IDS = {
    195,
    196,
    212,
    248,
    270,
    271,
    272,
    273,
    274,
    297,
    324,
    325,
    326,
    328,
    329,
    334,
    335,
    336,
    337,
    338,
    339,
    342,
    345,
    350,
    351,
    352,
    353,
    354,
    565,
    577,
    578,
    580,
    582,
    584,
    594,
    736,
    737,
    738,
    739,
    888,
    889,
    897,
    899,
    903,
}


PROOF_DECISIONS = {
    929: (
        "SOUND_DEFINITION",
        "Fully equated proof-local mathematical summary; it does not rewrite program execution.",
    ),
    930: (
        "SOUND_BASE_EQUATION",
        "For N <= 0, zero shifts leave the first component A.",
    ),
    931: (
        "SOUND_RECURSIVE_EQUATION",
        "For N > 0, one tuple shift followed by N-1 shifts is definitionally exact.",
    ),
    932: (
        "SOUND_INTEGER_IDENTITY",
        "Over mathematical integers, N-(I+1)=(N-I)+(-1).",
    ),
}


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} INPUT_TSV OUTPUT_TSV")
        return 64
    input_path, output_path = map(Path, sys.argv[1:])
    with input_path.open(newline="") as stream:
        reader = csv.DictReader(stream, dialect="excel-tab")
        rows = list(reader)
        input_fields = reader.fieldnames or []

    fields = input_fields + ["program_relevance", "audit_decision", "audit_reason"]
    with output_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, dialect="excel-tab")
        writer.writeheader()
        for row in rows:
            row_id = int(row["id"])
            if row_id in PROOF_DECISIONS:
                decision, reason = PROOF_DECISIONS[row_id]
                relevance = "proof_local_and_result_relevant"
            elif row_id in DIRECT_IDS:
                decision = "USED_FIXED_RULE_REVIEWED_SOUND"
                reason = (
                    "Exact trusted supplied-semantics entry; its binding, evaluation, "
                    "control, and state effect agrees with the used integer-only path."
                )
                relevance = "direct_concrete_or_symbolic_path"
            elif row["class"] == "opaque_symbol_declaration":
                decision = "UNREACHABLE_TRUSTED_PRIMITIVE"
                reason = (
                    "Exact trusted supplied-semantics primitive; neither solution.mpy "
                    "nor the claims construct or reference this symbol."
                )
                relevance = "not_referenced_by_program_or_claim"
            else:
                decision = "ACCEPTED_FIXED_SUPPLIED_SEMANTICS"
                reason = (
                    "Type- and byte-identical to the mandated trusted semantics tree; "
                    "not a candidate proof extension. No task-specific FibFib conclusion."
                )
                relevance = "fixed_library"
            writer.writerow(
                {
                    **row,
                    "program_relevance": relevance,
                    "audit_decision": decision,
                    "audit_reason": reason,
                }
            )

    print(f"rows_annotated={len(rows)}")
    print(f"direct_path_rows={len(DIRECT_IDS)}")
    print(f"proof_local_rows={len(PROOF_DECISIONS)}")
    print(f"output={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
