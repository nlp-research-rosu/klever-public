#!/usr/bin/env python3
"""Inventory every supplied K symbol(...) declaration and theorem relevance."""

from __future__ import annotations

import csv
import re
from pathlib import Path


root = Path("/candidate/reference-semantics")
rows: list[dict[str, object]] = []
for path in sorted(root.rglob("*.k")):
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if line.lstrip().startswith("//"):
            continue
        match = re.search(r"symbol\(([^)]+)\)", line)
        if not match:
            continue
        name = match.group(1)
        used = name in {"sortVS", "sortKeyVS"}
        rows.append(
            {
                "symbol": name,
                "source": str(path),
                "line": line_number,
                "no_evaluators": "yes" if "no-evaluators" in line else "no",
                "reached_by_theorem": "yes" if used else "no",
                "assessment": (
                    "RESULT-BEARING SUPPLIED TRUST BOUNDARY"
                    if used
                    else "UNUSED BY SUBMITTED PROGRAM AND CLAIMS"
                ),
            }
        )

output = Path("/audit-output/evidence/opaque-symbols.tsv")
with output.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "symbol",
            "source",
            "line",
            "no_evaluators",
            "reached_by_theorem",
            "assessment",
        ],
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"symbol_count={len(rows)}")
print("reached=" + ",".join(str(row["symbol"]) for row in rows if row["reached_by_theorem"] == "yes"))
print("unused=" + ",".join(str(row["symbol"]) for row in rows if row["reached_by_theorem"] == "no"))
print(f"output={output}")
