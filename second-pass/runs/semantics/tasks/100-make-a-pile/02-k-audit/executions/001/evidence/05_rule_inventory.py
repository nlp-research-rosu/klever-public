#!/usr/bin/env python3
"""Enumerate every local K directive and soundness-sensitive attribute."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|alias)\b"
)
ATTRIBUTE_WORDS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "concrete",
    "anywhere",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


records: list[dict[str, str | int]] = []
REACHABLE_BASELINE_FILES = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/list.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/call.k",
}
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for ordinal, start in enumerate(starts):
        stop = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        block_lines = []
        for line in lines[start:stop]:
            if line.strip() == "endmodule":
                break
            if line.lstrip().startswith("//"):
                continue
            if line.strip().startswith(("module ", "imports ")):
                continue
            if line.strip():
                block_lines.append(line.strip())
        statement = " ".join(block_lines)
        kind = START.match(lines[start]).group(1)  # type: ignore[union-attr]
        attrs = [
            word
            for word in ATTRIBUTE_WORDS
            if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(word)}(?![A-Za-z0-9_-])", statement)
        ]
        records.append(
            {
                "id": len(records) + 1,
                "file": rel(path),
                "line": start + 1,
                "kind": kind,
                "attributes": ",".join(attrs) if attrs else "-",
                "statement": statement,
            }
        )

for record in records:
    file_name = str(record["file"])
    line = int(record["line"])
    if file_name.startswith("reference-semantics/"):
        record["decision"] = "FOLLOWS_SELECTED_SUPPLIED_SEMANTICS"
        record["program_use"] = (
            "REACHABLE_MODULE_REVIEWED"
            if file_name in REACHABLE_BASELINE_FILES
            else "TERM_DISJOINT_FROM_SUBMITTED_PROGRAM"
        )
    elif file_name == "spec.k":
        record["decision"] = "CLAIM_ADEQUACY_REVIEWED"
        record["program_use"] = "POSITIVE_TARGET"
    elif file_name == "verification.k" and line in {6, 7, 10, 11, 18, 19, 25, 26, 28, 29}:
        record["decision"] = "SOUND_EXACT_ABBREVIATION"
        record["program_use"] = "PROGRAM_PINNING"
    elif file_name == "verification.k" and line == 34:
        record["decision"] = "SOUND_DEFINITIONAL_SUMMARY_DECLARATION"
        record["program_use"] = "RESULT_SUMMARY"
    elif file_name == "verification.k" and line in {35, 37}:
        record["decision"] = "SOUND_TRUE_GUARDED_EQUATION"
        record["program_use"] = "RESULT_SUMMARY"
    elif file_name == "verification.k" and line in {43, 44}:
        record["decision"] = "SOUND_LIST_MONOID_EQUATION"
        record["program_use"] = "SYMBOLIC_NORMALIZATION"
    else:
        raise AssertionError(f"unclassified directive: {file_name}:{line}")

counts = collections.Counter(record["kind"] for record in records)
source_counts = collections.Counter(
    "candidate-proof"
    if str(record["file"]) in {"verification.k", "spec.k"}
    else "trusted-supplied-semantics"
    for record in records
)
attribute_counts = collections.Counter()
for record in records:
    if record["attributes"] != "-":
        attribute_counts.update(str(record["attributes"]).split(","))

print("# Inventory summary")
print(f"files={len(FILES)}")
print(f"directives={len(records)}")
print("directive_counts=" + repr(dict(sorted(counts.items()))))
print("source_counts=" + repr(dict(sorted(source_counts.items()))))
print("attribute_counts=" + repr(dict(sorted(attribute_counts.items()))))
print()
print("id\tfile\tline\tkind\tattributes\tprogram_use\tdecision\tstatement")
for record in records:
    statement = str(record["statement"]).replace("\t", " ").replace("\n", " ")
    print(
        f"{record['id']}\t{record['file']}\t{record['line']}\t"
        f"{record['kind']}\t{record['attributes']}\t"
        f"{record['program_use']}\t{record['decision']}\t{statement}"
    )
