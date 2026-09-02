#!/usr/bin/env python3
"""Produce a line-addressed exhaustive inventory of local K declarations."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|alias|"
    r"module|endmodule|imports|requires)\b"
)

USED_MARKERS = {
    "#alloc",
    "#applyK",
    "#bindP",
    "#bindTgt",
    "#branch",
    "#callee",
    "#dictAcc",
    "#dset",
    "#endcall",
    "#evalArgs",
    "#iter",
    "#loadAll",
    "#look",
    "#loop",
    "#pop",
    "appendVal",
    "applyBin",
    "applyCmp",
    "applyIndexD",
    "Assert",
    "Assign",
    "Attribute",
    "BinOp",
    "Call",
    "Compare",
    "DictExpr",
    "dictSet",
    "dGet",
    "dHasKey",
    "dPut",
    "For",
    "flushTok",
    "FuncDef",
    "If",
    "Int(",
    "Name",
    "Return",
    "splitWS",
    "Str(",
    "Subscript",
    "truthy",
    "valSeqConcat",
    "vsLen",
}


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        match = START.match(lines[start])
        assert match is not None
        end_limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
        end = end_limit
        # A module boundary can occur before the next declaration.
        for candidate in range(start + 1, end_limit):
            if BOUNDARY.match(lines[candidate]) and not START.match(lines[candidate]):
                end = candidate
                break
        body_lines = []
        for line in lines[start:end]:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue
            body_lines.append(stripped)
        yield match.group(1).replace(" ", "_"), start + 1, " ".join(body_lines)


def tags(text: str) -> list[str]:
    available = [
        "function",
        "total",
        "functional",
        "macro",
        "macro-rec",
        "constructor",
        "simplification",
        "concrete",
        "owise",
        "priority",
        "no-evaluators",
        "symbol",
        "strict",
        "seqstrict",
    ]
    return [tag for tag in available if tag in text]


def decision(path: Path, kind: str, text: str) -> str:
    if path.name == "verification.k":
        if "tokenText" in text and kind == "syntax":
            return "CANDIDATE_NOVEL_SYNTHETIC_INTSEQ_CONSTRUCTOR"
        if text.startswith("rule splitWS(tokenText"):
            return "CANDIDATE_SYNTHETIC_SPLIT_EQUATION_REQUIRES_DENOTATION_BRIDGE"
        if "histogramCheck" in text and kind == "syntax":
            return "CANDIDATE_MACRO_DECLARATION"
        if text.startswith("rule histogramCheck"):
            return "CANDIDATE_EXACT_AST_CLONE_PLUS_RESULT_ASSERTION"
        return "CANDIDATE_EXTENSION_REVIEW_REQUIRED"
    if path.name in {"spec.k", "spec-labeled.k"}:
        return "TARGET_REACHABILITY_CLAIM"
    relevant = any(marker in text for marker in USED_MARKERS)
    if relevant:
        return "ACCEPTED_FIXED_SUPPLIED_SEMANTICS_ON_PROOF_PATH"
    return "ACCEPTED_FIXED_SUPPLIED_SEMANTICS_OFF_PROOF_PATH"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--semantics-root", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted(args.semantics_root.rglob("*.k"))
    paths.extend([args.verification, args.spec])
    rows = []
    counts = Counter()
    attribute_counts = Counter()
    for path in paths:
        if path.is_relative_to(args.semantics_root):
            display = "reference-semantics/" + path.relative_to(
                args.semantics_root
            ).as_posix()
        else:
            display = path.name
        for kind, line, text in blocks(path):
            item_tags = tags(text)
            item_decision = decision(path, kind, text)
            rows.append(
                (
                    display,
                    line,
                    kind,
                    ",".join(item_tags) if item_tags else "-",
                    item_decision,
                    text,
                )
            )
            counts[kind] += 1
            attribute_counts.update(item_tags)

    with args.output.open("w", encoding="utf-8") as handle:
        handle.write("file\tline\tkind\tattributes\taudit_classification\tdeclaration\n")
        for row in rows:
            handle.write("\t".join(str(value).replace("\t", " ") for value in row) + "\n")

    print(f"files_inventoried={len(paths)}")
    print(f"inventory_rows={len(rows)}")
    print("kind_counts=" + repr(dict(sorted(counts.items()))))
    print("attribute_counts=" + repr(dict(sorted(attribute_counts.items()))))
    per_file = Counter(row[0] for row in rows)
    for path, count in sorted(per_file.items()):
        print(f"file_count path={path} rows={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
