#!/usr/bin/env python3
"""Produce an exhaustive source-level inventory of K declarations."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|alias)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "concrete",
    "symbol",
    "trusted",
)


def declaration_records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, match.group(1))
        for index, line in enumerate(lines)
        if (match := START.match(line))
    ]
    for ordinal, (start, kind) in enumerate(starts, 1):
        end = starts[ordinal][0] if ordinal < len(starts) else len(lines)
        while end > start and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        text = "\n".join(lines[start:end]).rstrip()
        normalized = " ".join(
            part.strip()
            for part in text.splitlines()
            if part.strip() and not part.lstrip().startswith("//")
        )
        attributes = [
            attr
            for attr in ATTRS
            if re.search(rf"\b{re.escape(attr)}\b", text)
        ]
        yield {
            "file": str(path),
            "line": start + 1,
            "kind": kind,
            "attributes": attributes,
            "text": text,
            "normalized": normalized,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--tsv", type=Path, required=True)
    args = parser.parse_args()

    files = sorted(args.root.joinpath("reference-semantics").rglob("*.k"))
    files.extend(
        path
        for name in ("verification.k", "spec.k")
        if (path := args.root / name).is_file()
    )
    records = []
    for path in files:
        origin = (
            "CANDIDATE_LOCAL"
            if path.name in {"verification.k", "spec.k"}
            else "SUPPLIED_SEMANTICS"
        )
        for record in declaration_records(path):
            record["id"] = len(records) + 1
            record["origin"] = origin
            record["review_disposition"] = (
                "candidate-local: requires individual review"
                if origin == "CANDIDATE_LOCAL"
                else "fixed supplied semantics: integrity-verified; inspect relevance"
            )
            records.append(record)

    args.json.write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with args.tsv.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(
            [
                "id",
                "origin",
                "file",
                "line",
                "kind",
                "attributes",
                "review_disposition",
                "normalized",
            ]
        )
        for record in records:
            writer.writerow(
                [
                    record["id"],
                    record["origin"],
                    record["file"],
                    record["line"],
                    record["kind"],
                    ",".join(record["attributes"]),
                    record["review_disposition"],
                    record["normalized"],
                ]
            )

    kinds = Counter(record["kind"] for record in records)
    attrs = Counter(
        attr for record in records for attr in record["attributes"]
    )
    origins = Counter(record["origin"] for record in records)
    summary = {
        "files": len(files),
        "records": len(records),
        "by_origin": dict(sorted(origins.items())),
        "by_kind": dict(sorted(kinds.items())),
        "by_attribute": dict(sorted(attrs.items())),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
