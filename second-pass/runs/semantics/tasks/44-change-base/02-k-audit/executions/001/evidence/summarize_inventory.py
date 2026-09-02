#!/usr/bin/env python3
"""Summarize and sanity-check the exhaustive K inventory."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


def main() -> int:
    path = Path("/audit-output/evidence/rule-inventory.tsv")
    rows = []
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(
            (line for line in stream if not line.startswith("#")), delimiter="\t"
        )
        rows.extend(reader)

    print(f"ITEM_COUNT={len(rows)}")
    print(f"KINDS={dict(sorted(Counter(row['kind'] for row in rows).items()))}")
    print(
        "DISPOSITIONS="
        + repr(
            dict(
                sorted(
                    Counter(
                        row["disposition"].split("|", 1)[0] for row in rows
                    ).items()
                )
            )
        )
    )
    attribute_counter = Counter()
    for row in rows:
        if row["attributes"] != "-":
            attribute_counter.update(row["attributes"].split(","))
    print(f"ATTRIBUTES={dict(sorted(attribute_counter.items()))}")
    print("PROOF_LOCAL_ITEMS")
    for row in rows:
        if row["file"] == "verification.k":
            print(
                f"  {row['line_start']}: {row['kind']} "
                f"[{row['attributes']}] {row['disposition']} :: {row['statement']}"
            )
    return 0 if len(rows) == 943 else 1


if __name__ == "__main__":
    raise SystemExit(main())
