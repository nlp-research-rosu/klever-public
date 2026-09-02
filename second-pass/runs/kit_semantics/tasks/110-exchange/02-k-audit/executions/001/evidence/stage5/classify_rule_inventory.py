#!/usr/bin/env python3
"""Attach an explicit audit decision to every inventoried K declaration."""

from __future__ import annotations

import csv
from pathlib import Path


INPUT = Path("/audit-output/evidence/stage5/rule-inventory.tsv")
OUTPUT = Path("/audit-output/evidence/stage5/rule-review.tsv")


def proof_local_decision(line: int, kind: str) -> tuple[str, str]:
    if kind in {"requires", "module", "endmodule", "imports"}:
        return (
            "STRUCTURAL",
            "Module/include structure only; it imports the byte-identical supplied semantics.",
        )
    if line in {8, 15, 30}:
        return (
            "SOUND_DECLARATION",
            "Macro syntax only; the associated expansion is reviewed separately.",
        )
    if line in {9, 16, 31}:
        return (
            "SOUND_EXACT_MACRO",
            "Expanded constructor term was mechanically compared with regenerated solution.mpy.",
        )
    if line in {40, 41, 60, 61, 80, 81}:
        return (
            "SOUND_SORT_PREDICATE",
            "Defines the corresponding generated subsort predicate and adds no operational effect.",
        )
    if 43 <= line <= 97:
        return (
            "SOUND_GUARDED_TOTALIZER",
            "Partial-cast definedness/orientation is guarded by the exact sort predicate; "
            "off-sort total values occur only below a false Boolean conjunct.",
        )
    if 102 <= line <= 104:
        return (
            "SOUND_BOOL_COERCION",
            "Exhaustive Python Bool-to-int mapping false->0 and true->1.",
        )
    if 106 <= line <= 108:
        return (
            "TRUSTED_NUMERIC_PRIMITIVE_BRIDGE",
            "Adds the previously missing Bool/Float promotion cases used by the source; "
            "it is result-bearing and supported by reviewer LLVM/Python tests, while "
            "Float value meaning remains conditional on supplied floatMod/eqF primitives.",
        )
    if 110 <= line <= 120:
        return (
            "SOUND_DOMAIN_DEFINITION",
            "Exact Int/Bool/Float union and structurally descending finite-sequence predicate.",
        )
    if 125 <= line <= 126:
        return (
            "SOUND_CONDITIONAL_PARITY",
            "Exhaustive sort-disjoint parity formula, conditional only on the named numeric primitives.",
        )
    if 137 <= line <= 142:
        return (
            "SOUND_STRUCTURAL_COUNT",
            "Base/step recursion descends on ValSeq; complementary guards cover every total Bool result.",
        )
    if 148 <= line <= 151:
        return (
            "SOUND_RESULT_DEFINITION",
            "Complementary >=/< integer guards select exactly one literal result.",
        )
    if line == 161:
        return (
            "SOUND_DERIVED_PURE_BRIDGE",
            "Pure post-evaluation composition; all six bridge-free connection claims close and "
            "the rule touches no state/control cells.",
        )
    if line == 164:
        return (
            "SOUND_DEFINEDNESS_LEMMA",
            "Modulo by fixed nonzero 2 is defined for every value admitted by isNumberVal "
            "under the modeled total numeric primitives.",
        )
    if kind == "syntax":
        return ("SOUND_DECLARATION", "Pure syntax/function declaration reviewed with its equations.")
    return ("REVIEWED_NO_DEFECT", "No separate operational or logical effect beyond reviewed equations.")


def main() -> None:
    with INPUT.open() as stream:
        records = list(csv.DictReader(stream, delimiter="\t"))
    fieldnames = list(records[0]) + ["decision", "audit_rationale"]
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for record in records:
            provenance = record["provenance"]
            if provenance == "SUPPLIED_FIXED":
                if record["opaque_no_evaluators"] == "True":
                    decision = "FIXED_OPAQUE_TRUST_BOUNDARY"
                    rationale = (
                        "Byte-identical launcher-selected semantics; opaque value is accepted "
                        "only at the supplied-semantics trust boundary and is accounted for separately."
                    )
                else:
                    decision = "FIXED_SELECTED_SEMANTICS"
                    rationale = (
                        "Byte-identical launcher-selected semantics, not a candidate proof extension."
                    )
            elif provenance == "PROOF_LOCAL":
                decision, rationale = proof_local_decision(
                    int(record["line"]), record["kind"]
                )
            elif provenance == "PROOF_CLAIM":
                decision = "CHECKED_CONNECTION_CLAIM"
                rationale = (
                    "Claim/module declaration; all six selected connection claims exited 0 with #Top."
                )
            elif provenance == "TARGET_CLAIM":
                decision = "CHECKED_TARGET_CLAIM"
                rationale = (
                    "Claim/module declaration; count-loop closes individually and the complete "
                    "target suite exits 0 with #Top."
                )
            else:
                raise AssertionError(provenance)
            writer.writerow(
                {
                    **record,
                    "decision": decision,
                    "audit_rationale": rationale,
                }
            )

    counts: dict[str, int] = {}
    with OUTPUT.open() as stream:
        for record in csv.DictReader(stream, delimiter="\t"):
            counts[record["decision"]] = counts.get(record["decision"], 0) + 1
    print(f"input={INPUT}")
    print(f"output={OUTPUT}")
    print(f"reviewed_declarations={len(records)}")
    for decision, count in sorted(counts.items()):
        print(f"{decision}={count}")


if __name__ == "__main__":
    main()
