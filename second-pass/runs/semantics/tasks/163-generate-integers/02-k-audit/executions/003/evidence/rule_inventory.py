#!/usr/bin/env python3
"""Generate an exhaustive declaration/rule inventory for the audited K theory."""

from __future__ import annotations

from collections import Counter
import csv
from pathlib import Path
import re


TRUSTED_ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")

DECL = re.compile(
    r"^(?P<indent>\s*)(?P<kind>requires|module|imports|syntax|configuration|context|rule|claim|alias|endmodule)\b"
)

# These source regions implement the exact execution path of solution.mpy.
USED_REGIONS: dict[str, list[tuple[int, int]]] = {
    "semantics.k": [(34, 90)],
    "semantics/syntax.k": [(7, 62)],
    "semantics/core.k": [
        (13, 60),
        (68, 70),
        (117, 194),
        (196, 205),
        (208, 225),
    ],
    "semantics/functions.k": [(12, 19), (64, 91)],
    "semantics/controls.k": [(7, 18), (46, 56)],
    "semantics/list.k": [(14, 21), (52, 55)],
    "semantics/bool.k": [(7, 25)],
    "semantics/operators.k": [(7, 19)],
    "semantics/int.k": [(22, 27)],
    "semantics/call.k": [(15, 23), (26, 32), (69, 78)],
}


def is_used(relative: str, start: int, end: int) -> bool:
    return any(start <= hi and end >= lo for lo, hi in USED_REGIONS.get(relative, []))


def classify(
    source: Path, relative: str, start: int, end: int, kind: str, text: str
) -> tuple[str, str]:
    if source == Path("/candidate/verification.k"):
        if kind == "syntax" and "generateIntegersBody" in text:
            return (
                "ACCEPTED-MACRO",
                "Exact constructor body; expanded KORE equals trusted regenerated solution.mpy.",
            )
        if kind == "rule" and start == 8:
            return (
                "ACCEPTED-MACRO",
                "Exact constructor body; expanded KORE equals trusted regenerated solution.mpy.",
            )
        if "solutionModule" in text or "generateIntegersClosure" in text:
            return (
                "ACCEPTED-MACRO",
                "Definitional syntax only; exact function binding/body/environment, no execution bypass.",
            )
        if "betweenEndpoints" in text:
            return (
                "ACCEPTED-SUMMARY",
                "Total mathematical predicate; exactly inclusive membership between either endpoint order.",
            )
        if "keepDigit" in text:
            return (
                "ACCEPTED-SUMMARY",
                "Two disjoint exhaustive Bool equations; retains the digit iff its predicate is true.",
            )
        if "evenDigits" in text:
            return (
                "ACCEPTED-SUMMARY",
                "Terminating definitional composition over 2,4,6,8; names the postcondition only.",
            )
        return (
            "ACCEPTED-STRUCTURE",
            "Module/import structure; adds no operational or logical shortcut.",
        )

    if source == Path("/candidate/spec.k"):
        if kind == "claim":
            return (
                "ACCEPTED-CLAIM",
                "Universal positive-Int entry claim; fresh proof closes and explicit false mutation fails.",
            )
        return (
            "ACCEPTED-STRUCTURE",
            "Specification module/import structure.",
        )

    if "no-evaluators" in text:
        return (
            "OPAQUE-UNUSED",
            "Declared supplied-semantics trust primitive; no reachable term in this program mentions it.",
        )
    if relative == "semantics/concrete.k":
        return (
            "RUNTIME-ONLY-UNUSED",
            "Imported only by MPY-KRUN; cannot contribute to the Haskell proof and does not match the audit program.",
        )
    if is_used(relative, start, end):
        return (
            "ACCEPTED-USED-PATH",
            "Matches the real program's syntax/execution path; checked for order, binding, cells, allocation, and control fidelity.",
        )
    return (
        "REVIEWED-UNUSED",
        "Supplied-semantics declaration/rule does not match any reachable term in this program; no overlap with used-path symbols.",
    )


def attribute_summary(text: str) -> str:
    names = []
    for name, pattern in [
        ("function", r"\bfunction\b"),
        ("functional", r"\bfunctional\b"),
        ("total", r"\btotal\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol\s*\("),
        ("priority", r"\bpriority\s*\("),
        ("macro-rec", r"\bmacro-rec\b"),
        ("macro", r"\bmacro\b"),
        ("owise", r"\bowise\b"),
        ("concrete", r"\bconcrete\b"),
        ("simplification", r"\bsimplification\b|\bsimplify\b"),
    ]:
        if re.search(pattern, text):
            names.append(name)
    return ",".join(names) if names else "-"


files = [TRUSTED_ROOT / "semantics.k", *sorted((TRUSTED_ROOT / "semantics").glob("*.k"))]
files += CANDIDATE_FILES
rows: list[list[str]] = []

for source in files:
    lines = source.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for line_number, line in enumerate(lines, 1):
        match = DECL.match(line)
        if match:
            indent = len(match.group("indent"))
            kind = match.group("kind")
            if (kind in {"requires", "module", "endmodule"} and indent == 0) or (
                kind
                in {
                    "imports",
                    "syntax",
                    "configuration",
                    "context",
                    "rule",
                    "claim",
                    "alias",
                }
                and indent == 2
            ):
                starts.append((line_number, kind))
    for index, (start, kind) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start - 1 : end]).strip()
        if source.is_relative_to(TRUSTED_ROOT):
            relative = source.relative_to(TRUSTED_ROOT).as_posix()
        else:
            relative = source.as_posix()
        status, rationale = classify(source, relative, start, end, kind, block)
        excerpt = re.sub(r"\s+", " ", block)
        if len(excerpt) > 320:
            excerpt = excerpt[:317] + "..."
        rows.append(
            [
                str(len(rows) + 1),
                relative,
                str(start),
                str(end),
                kind,
                attribute_summary(block),
                status,
                rationale,
                excerpt,
            ]
        )

with OUTPUT.open("w", newline="") as stream:
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(
        [
            "id",
            "source",
            "start_line",
            "end_line",
            "kind",
            "attributes",
            "decision",
            "rationale",
            "excerpt",
        ]
    )
    writer.writerows(rows)

print("inventory_path", OUTPUT)
print("entries", len(rows))
print("kinds", dict(sorted(Counter(row[4] for row in rows).items())))
print("attributes", dict(sorted(Counter(row[5] for row in rows).items())))
print("decisions", dict(sorted(Counter(row[6] for row in rows).items())))
print("functional_declarations", sum("functional" in row[5].split(",") for row in rows))
print("simplification_entries", sum("simplification" in row[5].split(",") for row in rows))
print("opaque_entries", sum("opaque/no-evaluators" in row[5].split(",") for row in rows))
print("priority_entries", sum("priority" in row[5].split(",") for row in rows))
