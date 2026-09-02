#!/usr/bin/env python3
"""Produce a source-located exhaustive declaration/rule inventory for K files."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^(?:"
    r"(?P<header_kind>module|endmodule|requires)\b"
    r"|[ \t]+(?P<body_kind>syntax|rule|claim|configuration|context|imports)\b"
    r")"
)
ATTR_NAMES = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "strict",
    "seqstrict",
    "macro",
    "symbol",
    "no-evaluators",
)


def normalize(lines: list[str]) -> str:
    return " ".join(" ".join(line.strip().split()) for line in lines).strip()


def records(path: Path, root: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("header_kind") or match.group("body_kind")))
    result: list[dict[str, object]] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        text = normalize(block)
        attrs = [name for name in ATTR_NAMES if re.search(rf"\b{re.escape(name)}\b", text)]
        assessment = (
            "selected supplied-semantics baseline; no candidate modification"
            if "reference-semantics/" in path.as_posix()
            else "candidate-local; manual assessment required"
        )
        result.append(
            {
                "file": path.relative_to(root).as_posix(),
                "line": start + 1,
                "kind": kind,
                "attributes": ",".join(attrs),
                "assessment_class": assessment,
                "declaration_or_rule": text,
            }
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--tsv", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted((args.root / "reference-semantics").rglob("*.k"))
    paths.extend([args.root / "verification.k", args.root / "spec.k"])
    all_records = [record for path in paths for record in records(path, args.root)]

    with args.tsv.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            delimiter="\t",
            fieldnames=[
                "file",
                "line",
                "kind",
                "attributes",
                "assessment_class",
                "declaration_or_rule",
            ],
        )
        writer.writeheader()
        writer.writerows(all_records)

    kinds = Counter(str(record["kind"]) for record in all_records)
    attrs = Counter(
        attr
        for record in all_records
        for attr in str(record["attributes"]).split(",")
        if attr
    )
    by_file: dict[str, Counter[str]] = {}
    for record in all_records:
        by_file.setdefault(str(record["file"]), Counter())[str(record["kind"])] += 1
    summary = {
        "files": len(paths),
        "records": len(all_records),
        "by_kind": dict(sorted(kinds.items())),
        "attribute_bearing_records": dict(sorted(attrs.items())),
        "by_file": {
            name: dict(sorted(counts.items()))
            for name, counts in sorted(by_file.items())
        },
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
