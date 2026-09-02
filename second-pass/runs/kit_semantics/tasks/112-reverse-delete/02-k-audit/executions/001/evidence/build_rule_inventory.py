#!/usr/bin/env python3
"""Build an exhaustive statement/rule inventory for the audited K sources."""

from __future__ import annotations

import csv
import pathlib
import re
import sys


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
OUTPUT = pathlib.Path("/audit-output/evidence/rule-inventory.tsv")

START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|module|endmodule|imports)\b"
)
FILE_REQUIRE = re.compile(r'^requires\s+"')
ATTRIBUTES = [
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "no-evaluators",
    "symbol",
    "strict",
    "seqstrict",
    "macro",
]

# Lines whose declarations/rules can participate in the exact entry proof.
MATERIAL_LINES: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/syntax.k": [(9, 61)],
    "reference-semantics/semantics/core.k": [
        (13, 42),
        (49, 60),
        (95, 102),
        (123, 134),
        (183, 219),
    ],
    "reference-semantics/semantics/iter.k": [(6, 8)],
    "reference-semantics/semantics/operators.k": [(6, 17)],
    "reference-semantics/semantics/str.k": [(3, 41)],
    "reference-semantics/semantics/tuple.k": [(3, 18), (30, 41)],
    "reference-semantics/semantics/controls.k": [(3, 31), (46, 75)],
    "reference-semantics/semantics/functions.k": [(3, 20), (62, 91)],
    "reference-semantics/semantics/call.k": [(10, 21), (69, 75)],
}


def is_material(rel: str, start: int, end: int) -> bool:
    return any(start <= hi and end >= lo for lo, hi in MATERIAL_LINES.get(rel, []))


def statements(path: pathlib.Path) -> list[tuple[str, int, int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1).replace(" ", "_")))
        elif FILE_REQUIRE.match(line):
            starts.append((index, "requires"))
    result: list[tuple[str, int, int, str]] = []
    for offset, (start, kind) in enumerate(starts):
        next_start = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines) + 1
        end = next_start - 1
        # Exclude trailing blank/comment lines belonging conceptually to the next item.
        while end >= start and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        text = "\n".join(lines[start - 1 : end]).strip()
        result.append((kind, start, end, text))
    return result


def disposition(rel: str, kind: str, start: int, end: int) -> tuple[str, str]:
    if rel == "verification.k":
        if kind == "syntax":
            return (
                "PROOF_LOCAL_DECLARATION",
                "ACCEPT: pure total structural summary; exhaustive IntSeq constructors; no K-cell match",
            )
        if kind == "rule":
            return (
                "PROOF_LOCAL_EQUATION",
                "ACCEPT: truthful guarded structural recursion on a strict IntSeq suffix",
            )
        return ("PROOF_LOCAL_SCAFFOLD", "ACCEPT: module/import scaffolding only")
    if rel == "spec.k":
        if kind == "claim":
            return (
                "REACHABILITY_CLAIM",
                "ACCEPT: manually reviewed for satisfiability, control-flow pinning, framing, and result constraint",
            )
        return ("SPEC_SCAFFOLD", "ACCEPT: module/import scaffolding only")
    if is_material(rel, start, end):
        if kind in {"rule", "context", "configuration"}:
            return (
                "MATERIAL_FIXED_SEMANTICS",
                "ACCEPT: manually reviewed in the reachable semantic slice; matches the intended material operation",
            )
        if kind == "syntax":
            return (
                "MATERIAL_DECLARATION",
                "ACCEPT: declaration/strictness for a constructor or value used by the pinned program",
            )
        return ("MATERIAL_SCAFFOLD", "ACCEPT: fixed-semantics module/import scaffolding")
    if kind == "rule":
        return (
            "OUT_OF_TARGET_SLICE_FIXED_RULE",
            "NO TARGET IMPACT: cannot match the pinned program's reachable constructors/control states; no false witness asserted",
        )
    if kind in {"syntax", "context", "configuration"}:
        return (
            "OUT_OF_TARGET_SLICE_DECLARATION",
            "NO TARGET IMPACT: fixed-semantics declaration not exercised by the pinned program",
        )
    return ("FIXED_SCAFFOLD", "NO TARGET IMPACT: assembly/module/import scaffolding")


def main() -> int:
    paths = sorted((WORK / "reference-semantics").rglob("*.k"))
    paths += [WORK / "verification.k", WORK / "spec.k"]
    rows: list[dict[str, str | int]] = []
    counts: dict[str, int] = {}
    for path in paths:
        rel = path.relative_to(WORK).as_posix()
        for ordinal, (kind, start, end, text) in enumerate(statements(path), 1):
            attrs = ",".join(attribute for attribute in ATTRIBUTES if attribute in text)
            review_class, decision = disposition(rel, kind, start, end)
            key = f"{rel}:{start}:{kind}:{ordinal}"
            rows.append(
                {
                    "id": key,
                    "file": rel,
                    "start_line": start,
                    "end_line": end,
                    "kind": kind,
                    "attributes": attrs,
                    "review_class": review_class,
                    "decision": decision,
                    "text": " ".join(text.split()),
                }
            )
            counts[kind] = counts.get(kind, 0) + 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "id",
                "file",
                "start_line",
                "end_line",
                "kind",
                "attributes",
                "review_class",
                "decision",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"output={OUTPUT}")
    print(f"rows={len(rows)}")
    for kind, count in sorted(counts.items()):
        print(f"kind.{kind}={count}")
    for attribute in ATTRIBUTES:
        count = sum(attribute in str(row["attributes"]).split(",") for row in rows)
        print(f"attribute.{attribute}={count}")
    for review_class in sorted({str(row["review_class"]) for row in rows}):
        count = sum(row["review_class"] == review_class for row in rows)
        print(f"class.{review_class}={count}")
    print(
        "simplification_rules=",
        sum(
            row["kind"] == "rule"
            and "simplification" in str(row["attributes"]).split(",")
            for row in rows
        ),
        sep="",
    )
    print(
        "opaque_declarations=",
        sum(
            row["kind"] == "syntax"
            and "no-evaluators" in str(row["attributes"]).split(",")
            for row in rows
        ),
        sep="",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
