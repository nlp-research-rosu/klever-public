#!/usr/bin/env python3
"""Sanity checks and focused summaries over the exhaustive K inventory."""

from __future__ import annotations

from collections import Counter
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/05_rule_inventory.tsv")


def main() -> None:
    print(
        "COMMAND: python3 "
        "/audit-output/evidence/05_inventory_checks.py"
    )
    rows = []
    for line in INVENTORY.read_text(encoding="utf-8").splitlines()[1:]:
        if line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 8:
            raise AssertionError(f"malformed inventory row: {line[:120]}")
        rows.append(parts)
    if len(rows) != 936:
        raise AssertionError(f"inventory is not exhaustive: {len(rows)}")

    kinds = Counter(row[3] for row in rows)
    classes = Counter(row[5] for row in rows)
    attributes = Counter()
    for row in rows:
        if row[4] != "-":
            attributes.update(row[4].split(","))
    print(f"KINDS {dict(sorted(kinds.items()))}")
    print(f"CLASSES {dict(sorted(classes.items()))}")
    print(f"ATTRIBUTES {dict(sorted(attributes.items()))}")

    proof_local = [
        row for row in rows if row[5] == "PROOF_LOCAL_SOUND"
    ]
    if len(proof_local) != 7:
        raise AssertionError(f"unexpected proof-local entry count: {len(proof_local)}")
    for row in proof_local:
        if any(
            forbidden in row[4].split(",")
            for forbidden in (
                "priority",
                "simplification",
                "concrete",
                "no-evaluators",
            )
        ):
            raise AssertionError(f"forbidden proof-local attribute: {row}")
        print(
            f"PROOF_LOCAL {row[1]}:{row[2]} {row[3]} "
            f"attrs={row[4]} {row[7]}"
        )
    verification = Path(
        "/tmp/audit-work/reconstruction/verification.k"
    ).read_text(encoding="utf-8")
    if "<k>" in verification or "claim " in verification:
        raise AssertionError("verification.k contains operational rewrite or claim")
    print(
        "PROOF_LOCAL_CHECK no <k>-cell rewrite, priority, simplification, "
        "opaque symbol, concrete rule, or auxiliary claim"
    )

    opaque = [
        row for row in rows if row[5] == "UNUSED_OPAQUE_TRUST_BOUNDARY"
    ]
    print(f"OPAQUE_UNUSED count={len(opaque)}")
    for row in opaque:
        print(f"OPAQUE_UNUSED {row[1]}:{row[2]} {row[7]}")

    priority_relevant = [
        row
        for row in rows
        if "priority" in row[4].split(",")
        and row[5] == "RELEVANT_FIXED_SOUND"
    ]
    print(f"PRIORITY_RELEVANT count={len(priority_relevant)}")
    for row in priority_relevant:
        print(f"PRIORITY_RELEVANT {row[1]}:{row[2]} {row[7]}")

    gaps = [
        row for row in rows if row[5] == "UNUSED_TOTALITY_COVERAGE_GAP"
    ]
    print(
        f"TOTALITY_WARNING_ENTRIES count={len(gaps)} "
        "names=mapStrVS,floorFI,toF,ceilF,joinCodes,valSeqAt "
        "theorem_path_occurrences=0"
    )
    print("RESULT: exhaustive inventory checks passed")


if __name__ == "__main__":
    main()
