#!/usr/bin/env python3
"""Produce an exhaustive declaration/rule inventory for the audited K sources.

The parser is intentionally lexical: it treats every top-level K declaration
marker as an item boundary, preserves the full normalized text and source
location, and emits a SHA-256 for later integrity checks.
"""

from __future__ import annotations

import collections
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
OUT_TSV = Path("/audit-output/evidence/stage5/rule-inventory.tsv")
OUT_SUMMARY = Path("/audit-output/evidence/stage5/rule-inventory-summary.txt")

MARKER = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|alias|priority)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "simplification",
    "priority",
    "macro",
    "strict",
    "seqstrict",
    "anywhere",
    "owise",
    "concrete",
)
USED_PATTERNS = (
    "#loadAll",
    "Module(",
    "FuncDef(",
    "Params(",
    "closureVal",
    "Call(",
    "#call",
    "call(",
    "Name(",
    "lookup",
    "Assign(",
    "ListExpr",
    "list(",
    "For(",
    "#loop",
    "If(",
    "#if",
    "Compare(",
    "CmpOp(",
    "applyCmp",
    "Attribute(",
    "append",
    "applyMethod",
    "Expr(",
    "Return(",
    "#return",
    "strToCodes",
    "valSeqConcat",
    "vCons",
    "Float(",
    "intToF",
    "eqF",
    "gtF",
    "grade",
)


@dataclass(frozen=True)
class Item:
    path: Path
    line: int
    kind: str
    text: str


def source_paths() -> list[Path]:
    paths = [ROOT / "reference-semantics" / "semantics.k"]
    paths.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    return paths


def parse(path: Path) -> list[Item]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = MARKER.match(line)
        if match:
            starts.append((index, match.group(1)))
    items: list[Item] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).rstrip()
        items.append(Item(path=path, line=start + 1, kind=kind, text=text))
    return items


def classify(item: Item) -> str:
    text = re.sub(r"//[^\n]*", " ", item.text)
    if item.kind == "syntax":
        tags = [attribute for attribute in ATTRIBUTES if attribute in text]
        return "syntax" + (":" + ",".join(tags) if tags else "")
    if item.kind == "rule":
        if "simplification" in text:
            return "rule:simplification"
        if "priority" in text:
            return "rule:priority"
        if "macro" in text or item.path.name == "verification.k" and item.line in {9, 49}:
            return "rule:macro"
        return "rule:ordinary"
    return item.kind


def local_disposition(item: Item, relevance: str) -> str:
    relative = item.path.relative_to(ROOT).as_posix()
    if relative.startswith("reference-semantics/"):
        return (
            "ACCEPT_FIXED_BASELINE_USED"
            if relevance == "potentially-used"
            else "ACCEPT_FIXED_BASELINE_UNUSED"
        )
    if relative == "verification.k":
        if item.kind == "syntax" and item.line in {8, 48}:
            return "ACCEPT_EXACT_AST_MACRO_DECL"
        if item.kind == "rule" and item.line in {9, 49}:
            return "ACCEPT_EXACT_AST_MACRO_EXPANSION"
        if item.kind == "syntax" and item.line in {60, 63, 71, 77, 95, 137}:
            return "ACCEPT_DEFINITIONAL_FUNCTION_DECL"
        if item.kind == "rule" and item.line in {
            61,
            64,
            65,
            72,
            73,
            74,
            78,
            79,
            80,
            96,
            138,
            139,
        }:
            return "ACCEPT_TRUTHFUL_DEFINITIONAL_EQUATION"
        if item.kind == "rule" and item.line in {84, 88}:
            return "ACCEPT_DERIVED_FIXED_COMPARISON_LEMMA"
        return "MANUAL_REVIEW_REQUIRED"
    if relative == "spec.k":
        if item.kind == "claim" and item.line == 6:
            return "ACCEPT_LOOP_CIRCULARITY"
        if item.kind == "claim" and item.line == 31:
            return "ACCEPT_ENTRY_THEOREM"
        return "MANUAL_REVIEW_REQUIRED"
    return "MANUAL_REVIEW_REQUIRED"


def compact(text: str) -> str:
    text = re.sub(r"//[^\n]*", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    items: list[Item] = []
    for path in source_paths():
        items.extend(parse(path))

    rows: list[list[str]] = []
    classifications: collections.Counter[str] = collections.Counter()
    dispositions: collections.Counter[str] = collections.Counter()
    files: collections.Counter[str] = collections.Counter()
    for index, item in enumerate(items, 1):
        relative = item.path.relative_to(ROOT).as_posix()
        classification = classify(item)
        relevance = (
            "potentially-used"
            if any(pattern in item.text for pattern in USED_PATTERNS)
            else "unused-by-submitted-program"
        )
        disposition = local_disposition(item, relevance)
        normalized = compact(item.text)
        digest = hashlib.sha256(item.text.encode()).hexdigest()
        rows.append(
            [
                str(index),
                relative,
                str(item.line),
                item.kind,
                classification,
                relevance,
                disposition,
                digest,
                normalized,
            ]
        )
        classifications[classification] += 1
        dispositions[disposition] += 1
        files[relative] += 1

    header = [
        "id",
        "file",
        "line",
        "kind",
        "classification",
        "program_relevance",
        "review_disposition",
        "sha256",
        "normalized_text",
    ]
    with OUT_TSV.open("w", encoding="utf-8") as stream:
        stream.write("\t".join(header) + "\n")
        for row in rows:
            stream.write("\t".join(value.replace("\t", " ") for value in row) + "\n")

    with OUT_SUMMARY.open("w", encoding="utf-8") as stream:
        stream.write(f"TOTAL_ITEMS {len(rows)}\n")
        stream.write("CLASSIFICATIONS\n")
        for key, count in sorted(classifications.items()):
            stream.write(f"{key}\t{count}\n")
        stream.write("DISPOSITIONS\n")
        for key, count in sorted(dispositions.items()):
            stream.write(f"{key}\t{count}\n")
        stream.write("FILES\n")
        for key, count in sorted(files.items()):
            stream.write(f"{key}\t{count}\n")
        stream.write(f"INVENTORY_SHA256 {hashlib.sha256(OUT_TSV.read_bytes()).hexdigest()}\n")

    manual = [row for row in rows if row[6] == "MANUAL_REVIEW_REQUIRED"]
    print(f"inventory={OUT_TSV} items={len(rows)} manual={len(manual)}")
    print(OUT_SUMMARY.read_text(encoding="utf-8"), end="")
    if manual:
        print("MANUAL_ROWS")
        for row in manual:
            print("\t".join(row[:7]))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
