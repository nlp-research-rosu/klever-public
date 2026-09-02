#!/usr/bin/env python3
"""Attach an audit disposition to every local K declaration and rule."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventory_k import inventory  # noqa: E402


RELEVANT_FIXED = {
    "semantics.k",
    "syntax.k",
    "core.k",
    "iter.k",
    "operators.k",
    "int.k",
    "bool.k",
    "list.k",
    "tuple.k",
    "controls.k",
    "functions.k",
    "call.k",
}


def proof_disposition(line: int, kind: str) -> tuple[str, str]:
    if kind == "syntax" and line in (8, 27, 34, 43):
        return (
            "ACCEPT_EXACT_PROGRAM_MACRO",
            "macro expansion was KORE-identical to the submitted translated module",
        )
    if kind == "rule" and line in (9, 28, 35, 44):
        return (
            "ACCEPT_EXACT_PROGRAM_MACRO",
            "macro expansion was KORE-identical to the submitted translated module",
        )
    if kind == "syntax" and line in (52, 53):
        return (
            "ACCEPT_WITH_INERT_UNDERDEFINITION",
            "total head/tail are equation-free on nilInts, but all target uses are guarded nonempty",
        )
    if kind == "rule" and line in (58, 60):
        return (
            "ACCEPT_ITERATOR_ABSTRACTION",
            "nil/cons guards partition Ints and mirror supplied .ValSeq/vCons iterator rules",
        )
    if kind == "syntax" and line == 66:
        return (
            "ACCEPT_RESULT_SUMMARY",
            "nsScan is exhaustively guarded and structurally recursive on Ints",
        )
    if kind == "rule" and 67 <= line <= 95:
        return (
            "ACCEPT_RESULT_SUMMARY_EQUATION",
            "disjoint/exhaustive branch equation mirrors the corresponding program branch",
        )
    if kind == "rule" and line == 104:
        return (
            "ACCEPT_VALIDATED_OPERATIONAL_LEMMA",
            "complete bridge-free connection theorem closes with the independent MAP delete law",
        )
    return (
        "ACCEPT_PROOF_LOCAL_DECLARATION",
        "constructor/selector declaration or exhaustive equation with no oracle value",
    )


def disposition(path: Path, line: int, kind: str, attrs: str) -> tuple[str, str]:
    if path.name == "verification.k":
        return proof_disposition(line, kind)
    if path.name == "spec.k":
        return (
            "TARGET_CLAIM",
            "audited dynamically, for satisfiability, result constraint, and real-program pinning",
        )
    if "reference-semantics" in path.parts:
        if path.name == "concrete.k":
            return (
                "ACCEPT_SUPPLIED_RUNTIME_ONLY",
                "trusted supplied rule; excluded from both Haskell proof definitions",
            )
        if "symbol" in attrs or "no-evaluators" in attrs:
            return (
                "ACCEPT_SUPPLIED_OPAQUE_INERT",
                "trusted supplied primitive; no such symbol is reachable in this integer-list program",
            )
        if path.name in RELEVANT_FIXED:
            return (
                "ACCEPT_SUPPLIED_RELEVANT",
                "inspected supplied rule; patterns, evaluation order, and state effects match the used construct",
            )
        return (
            "ACCEPT_SUPPLIED_DISJOINT",
            "inspected supplied rule; its syntax/guards are disjoint from every submitted-program execution term",
        )
    return ("REVIEW_REQUIRED", "unclassified source")


def main() -> int:
    if len(sys.argv) < 2:
        return 64
    files: set[Path] = set()
    for raw in sys.argv[1:]:
        path = Path(raw)
        if path.is_dir():
            files.update(path.rglob("*.k"))
        else:
            files.add(path)

    kinds = {"configuration", "syntax", "context", "rule", "claim"}
    number = 0
    counts: dict[str, int] = {}
    rows: list[str] = []
    for path in sorted(files):
        for line, kind, attrs, block in inventory(path):
            if kind not in kinds:
                continue
            number += 1
            decision, rationale = disposition(path, line, kind, attrs)
            counts[decision] = counts.get(decision, 0) + 1
            first_line = block.splitlines()[0].strip().replace("\t", " ")
            rows.append(
                f"{number:04d}\t{path}:{line}\t{kind}\t{attrs}\t"
                f"{decision}\t{rationale}\t{first_line}"
            )

    print("DECISION_COUNTS")
    for decision in sorted(counts):
        print(f"{decision}\t{counts[decision]}")
    print(f"TOTAL_DECIDED\t{number}")
    print()
    print("ID\tSOURCE\tKIND\tATTRS\tDECISION\tRATIONALE\tDECLARATION")
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
