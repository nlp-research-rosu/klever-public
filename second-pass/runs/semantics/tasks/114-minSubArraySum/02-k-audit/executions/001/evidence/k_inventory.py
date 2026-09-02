#!/usr/bin/env python3
"""Produce an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


TRUSTED_ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
OUTPUT_JSON = Path("/audit-output/evidence/k-inventory.json")
OUTPUT_SUMMARY = Path("/audit-output/evidence/k-inventory-summary.txt")

START = re.compile(
    r"^(?:(requires|module|endmodule)\b|"
    r"  (imports|configuration|syntax|rule|claim|context(?:\s+alias)?)\b)"
)
ATTRIBUTE_WORDS = (
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "concrete",
    "macro",
    "owise",
    "symbol",
    "hook",
)


def inventory_file(path: Path, origin: str) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            keyword = match.group(1) or match.group(2)
            starts.append((index, keyword.replace(" ", "_")))

    records: list[dict[str, object]] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).rstrip()
        attributes = [
            word
            for word in ATTRIBUTE_WORDS
            if re.search(rf"\b{re.escape(word)}\b", text)
        ]
        records.append(
            {
                "origin": origin,
                "file": str(path),
                "line_start": start + 1,
                "line_end": end,
                "kind": kind,
                "attributes": attributes,
                "text": text,
            }
        )
    return records


def main() -> None:
    records: list[dict[str, object]] = []
    trusted_files = sorted(TRUSTED_ROOT.rglob("*.k"))
    for path in trusted_files:
        records.extend(inventory_file(path, "trusted-supplied-semantics"))
    for path in CANDIDATE_FILES:
        records.extend(inventory_file(path, "candidate-proof-local"))

    OUTPUT_JSON.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    by_kind = Counter(str(record["kind"]) for record in records)
    by_origin = Counter(str(record["origin"]) for record in records)
    by_file = Counter(str(record["file"]) for record in records)
    by_attribute = Counter(
        attribute
        for record in records
        for attribute in record["attributes"]  # type: ignore[union-attr]
    )
    rule_classes = Counter()
    for record in records:
        if record["kind"] != "rule":
            continue
        attrs = set(record["attributes"])  # type: ignore[arg-type]
        if "simplification" in attrs:
            rule_classes["simplification_rule"] += 1
        elif "priority" in attrs:
            rule_classes["priority_rule"] += 1
        elif "macro" in attrs:
            rule_classes["macro_rule"] += 1
        else:
            rule_classes["ordinary_rule"] += 1

    summary_lines = [
        f"records={len(records)}",
        f"trusted_k_files={len(trusted_files)}",
        "by_origin=" + json.dumps(dict(sorted(by_origin.items())), sort_keys=True),
        "by_kind=" + json.dumps(dict(sorted(by_kind.items())), sort_keys=True),
        "by_attribute="
        + json.dumps(dict(sorted(by_attribute.items())), sort_keys=True),
        "rule_classes=" + json.dumps(dict(sorted(rule_classes.items())), sort_keys=True),
        "by_file:",
    ]
    summary_lines.extend(f"  {path}: {count}" for path, count in sorted(by_file.items()))
    OUTPUT_SUMMARY.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print("\n".join(summary_lines))
    print(f"inventory_json={OUTPUT_JSON}")


if __name__ == "__main__":
    main()
