#!/usr/bin/env python3
"""Emit a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.json")

START = re.compile(r"^  (syntax|configuration|rule|context|claim)\b")
BOUNDARY = re.compile(
    r"^(?:module\b|endmodule\b|requires\b|  imports\b|  (?:syntax|configuration|rule|context|claim)\b)"
)
ATTR = re.compile(r"\[([^\]]+)\]", re.DOTALL)


def sources() -> list[Path]:
    semantics = ROOT / "reference-semantics"
    files = [semantics / "semantics.k"]
    files.extend(sorted((semantics / "semantics").glob("*.k")))
    files.extend((ROOT / "verification.k", ROOT / "spec.k"))
    return files


def trim_trailing(lines: list[str]) -> list[str]:
    result = list(lines)
    while result and (not result[-1].strip() or result[-1].lstrip().startswith("//")):
        result.pop()
    return result


def inventory_file(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    records: list[dict[str, object]] = []
    for ordinal, start in enumerate(starts, 1):
        match = START.match(lines[start])
        assert match is not None
        end = len(lines)
        for probe in range(start + 1, len(lines)):
            if BOUNDARY.match(lines[probe]):
                end = probe
                break
        block = trim_trailing(lines[start:end])
        if not block:
            continue
        text = "\n".join(block)
        attributes = ",".join(
            attribute.strip().replace("\n", " ")
            for attribute in ATTR.findall(text)
        )
        kind = match.group(1)
        flags = {
            name: bool(re.search(rf"\b{re.escape(name)}\b", attributes))
            for name in (
                "function",
                "functional",
                "total",
                "symbol",
                "no-evaluators",
                "priority",
                "simplification",
                "concrete",
                "owise",
                "macro",
                "strict",
                "seqstrict",
            )
        }
        if kind == "rule":
            semantic_class = "operational-rule" if "<k>" in text else "equational-rule"
        elif kind == "syntax":
            semantic_class = "syntax-declaration"
        else:
            semantic_class = kind
        rel = path.relative_to(ROOT).as_posix()
        records.append(
            {
                "file": rel,
                "ordinal": ordinal,
                "start_line": start + 1,
                "end_line": start + len(block),
                "kind": kind,
                "semantic_class": semantic_class,
                "attributes": attributes,
                **flags,
                "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "source": text.replace("\t", "\\t").replace("\n", "\\n"),
            }
        )
    return records


def main() -> int:
    records = [record for path in sources() for record in inventory_file(path)]
    fields = [
        "file",
        "ordinal",
        "start_line",
        "end_line",
        "kind",
        "semantic_class",
        "attributes",
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "concrete",
        "owise",
        "macro",
        "strict",
        "seqstrict",
        "source_sha256",
        "source",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(records)

    by_file: dict[str, Counter[str]] = defaultdict(Counter)
    totals = Counter()
    for record in records:
        file_name = str(record["file"])
        kind = str(record["kind"])
        semantic_class = str(record["semantic_class"])
        by_file[file_name][kind] += 1
        if semantic_class != kind:
            by_file[file_name][semantic_class] += 1
        totals[kind] += 1
        if semantic_class != kind:
            totals[semantic_class] += 1
        for flag in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "macro",
            "strict",
            "seqstrict",
        ):
            if record[flag]:
                by_file[file_name][flag] += 1
                totals[flag] += 1
    summary = {
        "source_root": str(ROOT),
        "record_count": len(records),
        "inventory_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "totals": dict(sorted(totals.items())),
        "by_file": {name: dict(sorted(counts.items())) for name, counts in sorted(by_file.items())},
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
