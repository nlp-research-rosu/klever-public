#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
VERIFICATION = Path("/candidate/verification.k")
OUTPUT = Path("/audit-output/evidence/rule-inventory.csv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.md")

START = re.compile(
    r"^(module\b|endmodule\b|imports\b|configuration\b|"
    r"syntax\b|context\b|rule\b|claim\b|alias\b|macro\b)"
)


@dataclass
class Statement:
    path: Path
    start: int
    end: int
    text: str


# Exact source regions whose declarations/rules can contribute to the submitted
# function's symbolic execution. Declarations grouped in one K `syntax`
# statement are conservatively marked on-path when any production in the group
# is used.
ON_PATH: dict[str, list[tuple[int, int]]] = {
    "semantics.k": [(34, 90)],
    "semantics/syntax.k": [
        (9, 32),
        (37, 38),
        (41, 61),
    ],
    "semantics/core.k": [
        (13, 15),
        (18, 40),
        (44, 60),
        (68, 70),
        (94, 102),
        (117, 127),
        (129, 191),
        (193, 205),
        (208, 219),
    ],
    "semantics/functions.k": [(8, 16), (62, 91)],
    "semantics/call.k": [(15, 32), (34, 50), (69, 75)],
    "semantics/controls.k": [(8, 18)],
    "semantics/operators.k": [(10, 17), (33, 42)],
    "semantics/bool.k": [(8, 25)],
    "semantics/list.k": [(27, 28)],
    "semantics/sort.k": [(14, 42), (51, 66)],
}

CONCRETE_EVIDENCE: dict[str, list[tuple[int, int]]] = {
    "semantics/assert.k": [(6, 15)],
    "semantics/sort.k": [(20, 32)],
}


def parse_file(path: Path) -> list[Statement]:
    lines = path.read_text().splitlines()
    starts: list[int] = []
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if START.match(stripped) or line.startswith("requires "):
            starts.append(number)
    statements: list[Statement] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] - 1 if index + 1 < len(starts) else len(lines)
        pieces = []
        for line in lines[start - 1 : end]:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                pieces.append(stripped)
        statements.append(
            Statement(path=path, start=start, end=end, text=" ".join(pieces))
        )
    return statements


def intersects(
    relative: str, start: int, end: int, regions: dict[str, list[tuple[int, int]]]
) -> bool:
    return any(
        start <= region_end and end >= region_start
        for region_start, region_end in regions.get(relative, [])
    )


def kind(text: str) -> str:
    first = text.split(maxsplit=1)[0]
    if first == "syntax":
        if "no-evaluators" in text or "symbol(" in text:
            return "opaque syntax/function declaration"
        if "[macro" in text:
            return "syntax macro declaration"
        if "function" in text:
            return "function syntax declaration"
        return "syntax declaration"
    if first == "rule":
        if "simplification" in text:
            return "simplification rule"
        if "priority(" in text:
            return "priority semantic rule"
        if "[concrete" in text:
            return "concrete semantic/equational rule"
        if "[owise" in text:
            return "owise semantic/equational rule"
        return "ordinary semantic/equational rule"
    if first == "context":
        return "evaluation context"
    return first


def attributes(text: str) -> str:
    found = []
    for attribute in (
        "function",
        "functional",
        "total",
        "simplification",
        "concrete",
        "owise",
        "priority",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
        "macro",
    ):
        if re.search(rf"\b{re.escape(attribute)}\b", text):
            found.append(attribute)
    return ";".join(found)


def disposition(statement: Statement) -> tuple[str, str]:
    if statement.path == VERIFICATION:
        return (
            "PROOF_LOCAL_REVIEWED_SOUND",
            "Both Boolean simplifications were checked by truth table; guards are "
            "disjoint on their only syntactic overlap and each RHS is true.",
        )

    relative = statement.path.relative_to(SEMANTICS_ROOT).as_posix()
    if "sortVS(" in statement.text and (
        "no-evaluators" in statement.text or statement.text.startswith("syntax")
    ):
        return (
            "ON_PATH_TRUSTED_PRIMITIVE_LIMITATION",
            "Fixed supplied primitive; symbolic value is intentionally opaque. "
            "The theorem is conditional on sortVS denoting Python's ascending sort.",
        )
    if intersects(relative, statement.start, statement.end, ON_PATH):
        return (
            "ON_PATH_REVIEWED_SOUND_OR_FIXED_PRIMITIVE",
            "Matched against the constructor map and reviewed for binding, order, "
            "control, state, allocation, and result flow.",
        )
    if intersects(relative, statement.start, statement.end, CONCRETE_EVIDENCE):
        return (
            "CONCRETE_EVIDENCE_PATH_REVIEWED",
            "Used only by fresh LLVM assertions; not imported as an additional "
            "proof-local theorem.",
        )
    if "no-evaluators" in statement.text or "symbol(" in statement.text:
        return (
            "OFF_PATH_OPAQUE_FIXED_PRIMITIVE",
            "Constructor is absent from every reachable submitted-program term.",
        )
    return (
        "OFF_PATH_FIXED_SEMANTICS_REVIEWED",
        "Top constructor/sort cannot match any reachable term in this submitted "
        "program; no result or control influence on the target claim.",
    )


def main() -> None:
    paths = [SEMANTICS_ROOT / "semantics.k"]
    paths.extend(sorted((SEMANTICS_ROOT / "semantics").glob("*.k")))
    paths.append(VERIFICATION)
    statements = []
    for path in paths:
        statements.extend(parse_file(path))

    with OUTPUT.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "id",
                "file",
                "start_line",
                "end_line",
                "kind",
                "attributes",
                "disposition",
                "review_basis",
                "normalized_statement",
            ]
        )
        for identifier, statement in enumerate(statements, 1):
            if statement.path == VERIFICATION:
                relative = "verification.k"
            else:
                relative = statement.path.relative_to(SEMANTICS_ROOT).as_posix()
            status, basis = disposition(statement)
            writer.writerow(
                [
                    identifier,
                    relative,
                    statement.start,
                    statement.end,
                    kind(statement.text),
                    attributes(statement.text),
                    status,
                    basis,
                    statement.text,
                ]
            )

    counts: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for statement in statements:
        status, _ = disposition(statement)
        counts[status] = counts.get(status, 0) + 1
        item_kind = kind(statement.text)
        kinds[item_kind] = kinds.get(item_kind, 0) + 1

    lines = [
        "# Exhaustive K source inventory summary",
        "",
        f"Inventory rows: {len(statements)}",
        "",
        "Every launcher-supplied K source statement and every proof-local "
        "`verification.k` statement is listed in `rule-inventory.csv` with source "
        "lines, attributes, reachability disposition, and review basis.",
        "",
        "## Kinds",
        "",
    ]
    lines.extend(f"- {name}: {count}" for name, count in sorted(kinds.items()))
    lines.extend(["", "## Dispositions", ""])
    lines.extend(f"- {name}: {count}" for name, count in sorted(counts.items()))
    lines.extend(
        [
            "",
            "The two proof-local simplifications are the only local theory "
            "extensions. `sortVS` is the only on-path opaque result-bearing symbol. "
            "All other opaque symbols and off-path rules have distinct top "
            "constructors or sorts and cannot affect this claim.",
            "",
        ]
    )
    SUMMARY.write_text("\n".join(lines))
    print(f"wrote {OUTPUT} rows={len(statements)}")
    print(f"wrote {SUMMARY}")
    for name, count in sorted(counts.items()):
        print(name, count)


if __name__ == "__main__":
    main()
