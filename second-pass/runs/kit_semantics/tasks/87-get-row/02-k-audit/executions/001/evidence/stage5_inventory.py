#!/usr/bin/env python3
"""Exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/src")
SUPPLIED = ROOT / "reference-semantics"
LOCAL_FILES = [
    ROOT / "row-model.k",
    ROOT / "verification.k",
    ROOT / "shape-connection.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^  (syntax|rule|claim|configuration|context|context alias|macro|alias)\b"
)
MODULE = re.compile(r"^module\s+([A-Za-z0-9-]+)")

USED_MARKERS = (
    "Module",
    "FuncDef",
    "Params",
    "Return",
    "UnaryOp",
    "Subscript",
    "Name",
    "Int(",
    "Assign",
    "ListExpr",
    "NoneVal",
    "For(",
    "#loop",
    "#iter",
    "If(",
    "Compare",
    "CmpOp",
    "TupleExpr",
    "tuple(",
    "Expr(",
    "Call(",
    "#call",
    "#apply",
    "Attribute",
    "append",
    "AugAssign",
    "applyBin",
    "applyCmp",
    "sorted",
    "sortKeyVS",
    "#alloc",
    "#lookup",
    "#bind",
    "closureVal",
    "rowContents",
    "listRows",
    "advanceIndex",
    "scanAppend",
    "rowsAppend",
    "valSeqConcat",
    "list(",
    "vCons",
)


def files() -> list[Path]:
    return sorted(
        [SUPPLIED / "semantics.k", *(SUPPLIED / "semantics").glob("*.k")]
    ) + LOCAL_FILES


def blocks(path: Path):
    lines = path.read_text().splitlines()
    module = "(outside-module)"
    index = 0
    while index < len(lines):
        module_match = MODULE.match(lines[index])
        if module_match:
            module = module_match.group(1)
        start_match = START.match(lines[index])
        if not start_match:
            index += 1
            continue
        start = index
        kind = start_match.group(1)
        index += 1
        while index < len(lines):
            if START.match(lines[index]) or MODULE.match(lines[index]):
                break
            if lines[index].startswith("endmodule"):
                break
            index += 1
        text = "\n".join(lines[start:index]).strip()
        yield module, kind, start + 1, index, text


def normalize(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if "//" in stripped:
            stripped = stripped.split("//", 1)[0].rstrip()
        kept.append(stripped)
    return " ".join(kept).replace("\t", " ")


def main() -> None:
    rows = []
    for path in files():
        origin = (
            "SUPPLIED_FIXED"
            if path.is_relative_to(SUPPLIED)
            else "CANDIDATE_LOCAL"
        )
        for module, kind, start, end, text in blocks(path):
            flat = normalize(text)
            attributes = ",".join(
                attribute
                for attribute in (
                    "function",
                    "functional",
                    "total",
                    "macro",
                    "simplification",
                    "concrete",
                    "owise",
                    "no-evaluators",
                    "priority",
                )
                if re.search(rf"\b{re.escape(attribute)}\b", flat)
            )
            relevance = (
                "MAPPED_USED_OR_SUPPORT"
                if any(marker in flat for marker in USED_MARKERS)
                else "NOT_MAPPED_TO_SUBMITTED_PROGRAM"
            )
            if origin == "SUPPLIED_FIXED":
                decision = "ACCEPTED_SELECTED_FIXED_SEMANTICS_BOUNDARY"
            elif kind == "claim":
                decision = "POSITIVE_PROOF_TARGET_REVIEWED"
            else:
                decision = "LOCAL_EXTENSION_REVIEWED_SEPARATELY"
            rel = path.relative_to(ROOT).as_posix()
            rows.append(
                (
                    rel,
                    module,
                    kind,
                    f"{start}-{end}",
                    attributes or "-",
                    relevance,
                    decision,
                    flat,
                )
            )

    print(
        "file\tmodule\tkind\tlines\tattributes\trelevance\tdecision\tnormalized_source"
    )
    for row in rows:
        print("\t".join(row))
    print(f"INVENTORY_COUNT={len(rows)}")
    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row[0], row[2])
        counts[key] = counts.get(key, 0) + 1
    for (path, kind), count in sorted(counts.items()):
        print(f"COUNT\t{path}\t{kind}\t{count}")


if __name__ == "__main__":
    main()
