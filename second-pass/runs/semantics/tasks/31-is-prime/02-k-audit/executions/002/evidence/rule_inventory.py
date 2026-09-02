#!/usr/bin/env python3
"""Create a source-level declaration/rule inventory for the audited K theory."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/31-is-prime-audit")
OUT = Path("/audit-output/evidence")
START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(module|endmodule|imports)\b|^\s*requires\s+\""
)


def source_files() -> list[Path]:
    semantics = [WORK / "reference-semantics" / "semantics.k"]
    semantics.extend(sorted((WORK / "reference-semantics" / "semantics").glob("*.k")))
    return semantics + [WORK / "verification.k", WORK / "spec.k"]


def used_fragment(path: Path, line: int, kind: str) -> str:
    rel = path.relative_to(WORK).as_posix()
    if rel == "verification.k":
        return "PROOF_LOCAL"
    if rel == "spec.k":
        return "CLAIM"
    if rel == "reference-semantics/semantics/syntax.k":
        if line in {9, 32, 41, 56, 57, 60, 61}:
            return "USED_OR_IDENTITY"
    if rel == "reference-semantics/semantics/core.k":
        if (
            line in {49, 124, 125, 126, 127, 130, 131, 132, 152, 194, 195, 199, 200, 208, 209, 210}
            or 44 <= line <= 60
        ):
            return "USED_OR_IDENTITY"
    if rel == "reference-semantics/semantics/operators.k":
        if line in {12, 15, 16, 17}:
            return "USED"
    if rel == "reference-semantics/semantics/int.k":
        if line in {9, 14, 15, 19, 20, 22, 23, 26}:
            return "USED"
    if rel == "reference-semantics/semantics/controls.k":
        if line in {9, 20, 51, 52, 53, 54, 65, 77, 78, 79, 81, 85}:
            return "USED"
    if rel == "reference-semantics/semantics/functions.k":
        if line in {8, 78, 80, 85}:
            return "USED"
    return "UNUSED_BY_FORMAL_CLAIMS"


def disposition(path: Path, line: int, kind: str, text: str) -> str:
    rel = path.relative_to(WORK).as_posix()
    if rel.startswith("reference-semantics/"):
        if used_fragment(path, line, kind).startswith("USED"):
            return "SUPPLIED_BASELINE_RELEVANT_MANUALLY_CHECKED"
        return "SUPPLIED_BASELINE_UNMODIFIED_NOT_REACHED"
    if rel == "verification.k":
        if line in {9, 11}:
            return "SOUND_FINITE_MAP_DELETE_IDENTITY"
        if line in {16, 17, 22, 23, 31, 32}:
            return "SOUND_SYNTAX_ABBREVIATION"
        if line in {44, 45, 47, 49}:
            return "SOUND_GUARDED_RECURSIVE_DEFINITION_ON_USED_D_GE_2"
        if line in {52, 53, 54}:
            return "SOUND_DISJOINT_INT_CASE_DEFINITION"
        return "PROOF_LOCAL_DECLARATION"
    if rel == "spec.k":
        if line == 9:
            return "PROVED_RESULT_CONSTRAINING_LOOP_LEMMA"
        if line == 52:
            return "PROVED_RESULT_CONSTRAINING_SMALL_ENTRY_CASE"
        if line == 97:
            return "PROVED_PREFIX_ONLY_NOT_TARGET_POSTCONDITION"
    return "REVIEWED"


def attributes(text: str, kind: str) -> str:
    tags: list[str] = []
    for tag in [
        "function",
        "total",
        "functional",
        "simplification",
        "priority",
        "owise",
        "macro-rec",
        "macro",
        "concrete",
        "anywhere",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ]:
        if re.search(rf"\b{re.escape(tag)}\b", text):
            tags.append(tag)
    if kind == "rule":
        tags.append("operational" if "<k>" in text else "equational")
    if "symbol" in tags and "no-evaluators" in tags:
        tags.append("opaque-symbol")
    return ",".join(tags)


def records_for(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts = [
        (index, START.match(line).group(1))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    records: list[dict[str, object]] = []
    for start_index, kind in starts:
        end_index = start_index + 1
        while end_index < len(lines):
            line = lines[end_index]
            if START.match(line) or BOUNDARY.match(line):
                break
            end_index += 1
        body_lines = lines[start_index:end_index]
        while body_lines and (
            not body_lines[-1].strip() or body_lines[-1].lstrip().startswith("//")
        ):
            body_lines.pop()
        text = " ".join(line.strip() for line in body_lines)
        text = re.sub(r"\s+", " ", text)
        records.append(
            {
                "file": path.relative_to(WORK).as_posix(),
                "line": start_index + 1,
                "kind": kind,
                "attributes": attributes(text, kind),
                "formal_relevance": used_fragment(path, start_index + 1, kind),
                "review_disposition": disposition(
                    path, start_index + 1, kind, text
                ),
                "text": text,
            }
        )
    return records


def main() -> int:
    records: list[dict[str, object]] = []
    for path in source_files():
        records.extend(records_for(path))

    tsv_path = OUT / "rule_inventory.tsv"
    with tsv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "file",
                "line",
                "kind",
                "attributes",
                "formal_relevance",
                "review_disposition",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(records)

    by_kind = Counter(str(record["kind"]) for record in records)
    by_attr: Counter[str] = Counter()
    by_disposition = Counter(str(record["review_disposition"]) for record in records)
    by_file = Counter(str(record["file"]) for record in records)
    for record in records:
        for attr in str(record["attributes"]).split(","):
            if attr:
                by_attr[attr] += 1
    summary = {
        "record_count": len(records),
        "by_kind": dict(sorted(by_kind.items())),
        "by_attribute": dict(sorted(by_attr.items())),
        "by_disposition": dict(sorted(by_disposition.items())),
        "by_file": dict(sorted(by_file.items())),
        "inventory_sha256": __import__("hashlib").sha256(
            tsv_path.read_bytes()
        ).hexdigest(),
    }
    (OUT / "rule_inventory_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"inventory={tsv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
