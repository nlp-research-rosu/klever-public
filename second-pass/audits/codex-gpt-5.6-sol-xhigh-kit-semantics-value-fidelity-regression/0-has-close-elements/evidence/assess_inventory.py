#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventoried K sentence."""

from __future__ import annotations

import csv
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")


def verification_assessment(line: int) -> tuple[str, str]:
    if line in {7, 11, 12}:
        return (
            "ACCEPTED_DEFINITIONAL",
            "Exhaustive structural datatype/summary declaration over FloatSeq.",
        )
    if line == 9:
        return (
            "FAIL_RUNTIME_REPRESENTATION_EXTENSION",
            "Adds floatVals as a new ValSeq constructor; runtime ValSeq values are .ValSeq/vCons. "
            "The target uses this proof-only constructor, and inherited total functions become "
            "non-exhaustive on it.",
        )
    if 23 <= line <= 48:
        return (
            "LOCALLY_VALID_BUT_UNCONNECTED_ENCODING",
            "Truthful structural encoding/simplification at its stated pattern, but it does not "
            "connect list(floatVals(FS)) to a fixed-semantics runtime list in active context.",
        )
    if 55 <= line <= 86:
        return (
            "ACCEPTED_DEFINITIONAL",
            "Exhaustive, disjoint, structurally decreasing length/fold equation; matches the "
            "program's accumulator and index update.",
        )
    if line in {101, 105}:
        return (
            "FAIL_OPERATIONAL_BRIDGE",
            "Turns a fixed-semantics stuck proof-only list representation into iterator progress. "
            "Ground empty/cons bridge-free probes are stuck; the extension proves them.",
        )
    return ("REVIEW_REQUIRED", "Unexpected verification sentence.")


def spec_assessment(line: int) -> tuple[str, str]:
    if line in {6, 53}:
        return (
            "BRIDGE_DEPENDENT_CIRCULARITY",
            "Loop body, scope, accumulator, and control shape match the source, but closure depends "
            "on the unconnected iterator bridges and proof-only list representation.",
        )
    if line == 108:
        return (
            "FAIL_REAL_PROGRAM_PINNING",
            "Loads the submitted body, but invokes it on list(floatVals(INPUT)), not the fixed "
            "runtime list constructors. The bridge-free ground empty instance gets stuck.",
        )
    return ("REVIEW_REQUIRED", "Unexpected specification claim.")


def main() -> int:
    inventory_path = EVIDENCE / "rule-inventory.tsv"
    assessment_path = EVIDENCE / "rule-assessment.tsv"
    with inventory_path.open(newline="") as stream:
        records = list(csv.DictReader(stream, delimiter="\t"))

    for record in records:
        file = record["file"]
        line = int(record["line"])
        if file.startswith("reference-semantics/"):
            if "no-evaluators" in record["tags"]:
                disposition = "ACCEPTED_SUPPLIED_OPAQUE_BOUNDARY"
                rationale = (
                    "Exact trusted supplied-semantics symbol. Its interpretation is fixed by "
                    "concrete rules but opaque to kprove; only floatLt/absF/subF affect this target."
                )
            else:
                disposition = "ACCEPTED_SUPPLIED_FIXED_SEMANTICS"
                rationale = (
                    "Exact trusted supplied-semantics sentence, accepted as the selected fixed "
                    "language model; used-path rules are mapped separately."
                )
        elif file == "verification.k":
            disposition, rationale = verification_assessment(line)
        elif file == "spec.k":
            disposition, rationale = spec_assessment(line)
        else:
            disposition, rationale = "REVIEW_REQUIRED", "Unexpected source file."
        record["disposition"] = disposition
        record["rationale"] = rationale

    fieldnames = list(records[0]) if records else []
    with assessment_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(records)

    counts: dict[str, int] = {}
    for record in records:
        key = record["disposition"]
        counts[key] = counts.get(key, 0) + 1
    print(f"assessed_records={len(records)}")
    print(f"disposition_counts={dict(sorted(counts.items()))}")
    print(f"assessment={assessment_path} bytes={assessment_path.stat().st_size}")
    return 0 if "REVIEW_REQUIRED" not in counts else 1


if __name__ == "__main__":
    raise SystemExit(main())
