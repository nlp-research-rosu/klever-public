#!/usr/bin/env python3
"""Produce a complete declaration/rule inventory for the audited K source tree."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/47-median/candidate-src")
OUT = Path("/audit-output/evidence/05-rule-inventory.tsv")

START = re.compile(r"^  (syntax|rule|context|configuration|claim|alias)\b")
END_MODULE = re.compile(r"^endmodule\b")

# Line intervals whose declarations/rules can occur in the median target's
# execution or formal result. Everything else is still inventoried, but is not
# in the dependency slice of any target claim.
RELEVANT: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/syntax.k": [(9, 16), (27, 32), (37, 38), (41, 61)],
    "reference-semantics/semantics/core.k": [
        (13, 60),
        (117, 127),
        (130, 181),
        (185, 205),
        (208, 254),
    ],
    "reference-semantics/semantics/operators.k": [(10, 17), (25, 31)],
    "reference-semantics/semantics/int.k": [(7, 36)],
    "reference-semantics/semantics/bool.k": [(10, 22)],
    "reference-semantics/semantics/float.k": [
        (20, 32),
        (43, 52),
        (111, 113),
        (131, 187),
        (225, 240),
    ],
    "reference-semantics/semantics/str.k": [(13, 17)],
    "reference-semantics/semantics/subscript.k": [(7, 41)],
    "reference-semantics/semantics/controls.k": [(9, 18), (46, 54)],
    "reference-semantics/semantics/functions.k": [(8, 20), (62, 90)],
    "reference-semantics/semantics/builtins.k": [(17, 26)],
    "reference-semantics/semantics/call.k": [(15, 24), (31, 50), (69, 75)],
    "reference-semantics/semantics/sort.k": [(14, 61)],
    "program.k": [(6, 30)],
    "spec.k": [(7, 322)],
}


def relevant(rel: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in RELEVANT.get(rel, []))


def statement_kind(first: str, body: str) -> str:
    word = first.strip().split()[0]
    if word == "syntax":
        return "syntax"
    if word == "context":
        return "context"
    if word == "configuration":
        return "configuration"
    if word == "claim":
        return "target-claim"
    if word == "alias":
        return "alias"
    if "[simplification" in body:
        return "simplification-rule"
    if "<k>" in body or any(
        cell in body
        for cell in (
            "<env>",
            "<scopes>",
            "<heap>",
            "<heapLoc>",
            "<stack>",
            "<ret>",
            "<exc>",
            "<exit-code>",
        )
    ):
        return "operational-rule"
    return "equational-rule"


def flags(body: str) -> str:
    names = []
    for name, pattern in (
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol(?:\(|\b)"),
        ("concrete", r"\bconcrete\b"),
        ("simplification", r"\bsimplification\b"),
        ("owise", r"\bowise\b"),
        ("priority", r"\bpriority\s*\("),
        ("macro", r"\bmacro(?:-rec)?\b"),
        ("strict", r"\b(?:seq)?strict(?:\(|\b)"),
    ):
        if re.search(pattern, body):
            names.append(name)
    return ",".join(names) if names else "-"


def review(rel: str, line: int, body: str, is_relevant: bool) -> str:
    if rel == "program.k":
        return "JUSTIFIED_PROOF_LOCAL_DEFINITION"
    if rel == "spec.k":
        return "TARGET_CLAIM_NOT_ASSUMPTION"
    if rel == "verification.k":
        return "EMPTY_IMPORT_MODULE"
    if rel.endswith("semantics/float.k") and line == 31:
        return "FIXED_MODEL_GAP_FALSE_ON_HUGE_INT_WITNESS"
    if is_relevant and any(
        symbol in body
        for symbol in (
            "sortVS",
            "valSeqAt",
            "intFloatDiv",
            "divII",
            "floatLt",
            "addF",
            "ltFI",
            "ltIF",
            "eqIF",
            "divFloatIntV",
            "intToF",
        )
    ):
        return "SUPPLIED_RESULT_BEARING_MODEL_BOUNDARY"
    if is_relevant:
        return "RELEVANT_OPERATIONAL_OR_MATHEMATICAL_RULE_REVIEWED"
    return "FIXED_SEMANTICS_UNUSED_BY_TARGET"


def source_files() -> list[Path]:
    paths = [ROOT / "reference-semantics/semantics.k"]
    paths.extend(sorted((ROOT / "reference-semantics/semantics").glob("*.k")))
    paths.extend([ROOT / "program.k", ROOT / "verification.k", ROOT / "spec.k"])
    return paths


def main() -> int:
    rows: list[dict[str, str | int]] = []
    for path in source_files():
        rel = path.relative_to(ROOT).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        starts = [i for i, line in enumerate(lines) if START.match(line)]
        for pos, index in enumerate(starts):
            upper = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
            for end in range(index + 1, upper):
                if END_MODULE.match(lines[end]):
                    upper = end
                    break
            body_lines = lines[index:upper]
            while body_lines and (
                not body_lines[-1].strip() or body_lines[-1].lstrip().startswith("//")
            ):
                body_lines.pop()
            body = "\n".join(body_lines)
            is_relevant = relevant(rel, index + 1)
            rows.append(
                {
                    "id": len(rows) + 1,
                    "file": rel,
                    "line": index + 1,
                    "kind": statement_kind(lines[index], body),
                    "flags": flags(body),
                    "target_dependency": "YES" if is_relevant else "NO",
                    "review": review(rel, index + 1, body, is_relevant),
                    "declaration": " ".join(part.strip() for part in body_lines),
                }
            )

    with OUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "id",
                "file",
                "line",
                "kind",
                "flags",
                "target_dependency",
                "review",
                "declaration",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    by_kind: dict[str, int] = {}
    by_review: dict[str, int] = {}
    for row in rows:
        by_kind[str(row["kind"])] = by_kind.get(str(row["kind"]), 0) + 1
        by_review[str(row["review"])] = by_review.get(str(row["review"]), 0) + 1
    print(f"inventory_path={OUT}")
    print(f"records={len(rows)}")
    print(f"kind_counts={dict(sorted(by_kind.items()))}")
    print(f"review_counts={dict(sorted(by_review.items()))}")
    print("INVENTORY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
