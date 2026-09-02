#!/usr/bin/env python3
"""Build a line-addressable inventory of K declarations and rules."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/128-prod-signs.HMXf22")
EVIDENCE = Path("/audit-output/evidence")
START = re.compile(
    r"^(?:(requires|module)\b|  "
    r"(imports|configuration|syntax|context|rule|claim)\b)"
)
ATTR = re.compile(
    r"\b(functional|function|total|simplification|concrete|"
    r"priority|owise|macro-rec|macro|strict|seqstrict|symbol|opaque|"
    r"no-evaluators)\b"
)
BRACKET_ATTRIBUTE_BLOCK = re.compile(r"\[\s*([A-Za-z][^\]]*)\]")


def chunks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    current = None
    for number, line in enumerate(lines, start=1):
        match = START.match(line)
        if match:
            if current is not None:
                yield current
            kind = match.group(1) or match.group(2)
            current = {
                "file": str(path.relative_to(SCRATCH)),
                "line": number,
                "kind": kind,
                "lines": [line],
            }
        elif current is not None:
            stripped = line.strip()
            if stripped == "endmodule":
                yield current
                current = None
            else:
                current["lines"].append(line)
    if current is not None:
        yield current


def main() -> int:
    paths = [SCRATCH / "reference-semantics" / "semantics.k"]
    paths.extend(
        sorted((SCRATCH / "reference-semantics" / "semantics").glob("*.k"))
    )
    paths.append(SCRATCH / "verification.k")
    records = []
    for path in paths:
        for chunk in chunks(path):
            text = " ".join(
                part.strip()
                for part in chunk.pop("lines")
                if part.strip() and not part.strip().startswith("//")
            )
            attrs = sorted(
                {
                    attribute
                    for block in BRACKET_ATTRIBUTE_BLOCK.findall(text)
                    for attribute in ATTR.findall(block)
                }
            )
            source_class = (
                "candidate-proof-extension"
                if chunk["file"] == "verification.k"
                else "trusted-supplied-semantics"
            )
            records.append(
                {
                    **chunk,
                    "source_class": source_class,
                    "attributes": ",".join(attrs),
                    "text": text,
                }
            )

    with (EVIDENCE / "rule-inventory.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as output:
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "file",
                "line",
                "kind",
                "source_class",
                "attributes",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(records)

    by_kind = Counter(record["kind"] for record in records)
    by_source = Counter(record["source_class"] for record in records)
    by_attribute = Counter()
    for record in records:
        by_attribute.update(
            item for item in record["attributes"].split(",") if item
        )
    summary = {
        "files": len(paths),
        "records": len(records),
        "by_kind": dict(sorted(by_kind.items())),
        "by_source_class": dict(sorted(by_source.items())),
        "by_attribute": dict(sorted(by_attribute.items())),
        "inventory": "rule-inventory.tsv",
    }
    (EVIDENCE / "rule-inventory-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
