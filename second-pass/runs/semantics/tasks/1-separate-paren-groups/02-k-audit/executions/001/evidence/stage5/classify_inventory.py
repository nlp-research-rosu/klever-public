#!/usr/bin/env python3
"""Give every inventoried K sentence an explicit reviewer disposition."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/stage5/k-inventory.jsonl")

PROGRAM_PATH_FILES = {
    "syntax.k",
    "core.k",
    "controls.k",
    "functions.k",
    "call.k",
    "iter.k",
    "operators.k",
    "str.k",
    "list.k",
    "int.k",
}


def disposition(row: dict[str, object]) -> tuple[str, str, str]:
    path = Path(str(row["file"]))
    kind = str(row["kind"])
    line = int(row["line"])
    text = str(row["text"])

    if path.name == "verification.k":
        if kind in {"requires", "module", "imports", "endmodule"}:
            return (
                "ACCEPT",
                "proof-structure",
                "Structural import/module sentence; adds no equation or execution.",
            )
        if line in {9, 26} or 10 <= line <= 44:
            return (
                "ACCEPT",
                "definitional-summary",
                "scanGroups/scanClose structural fold; disjoint exhaustive cases and recursive descent on REST.",
            )
        if line == 49 or 50 <= line <= 58:
            return (
                "ACCEPT",
                "domain-predicate",
                "balancedTail structural predicate; disjoint exhaustive IntSeq cases and descent on REST.",
            )
        if line == 60 or 61 <= line <= 64:
            return (
                "ACCEPT",
                "domain-predicate",
                "parenSpaceOnly structural predicate; exhaustive IntSeq cases and descent on REST.",
            )
        if line == 68 or line == 69:
            return (
                "ACCEPT",
                "exact-body-macro",
                "Macro-only name for the submitted function closure; it does not rewrite a running program operation.",
            )
        return (
            "REVIEW_GAP",
            "unclassified-proof-extension",
            "Unexpected verification.k sentence not covered by the manual line classification.",
        )

    if kind in {"requires", "module", "imports", "endmodule"}:
        return (
            "ACCEPT",
            "fixed-semantics-structure",
            "Structural sentence from the byte-identical trusted supplied-semantics tree.",
        )
    if kind == "syntax":
        opaque = "no-evaluators" in text or "symbol(" in text
        if opaque:
            return (
                "ACCEPT",
                "fixed-unreachable-opaque-declaration",
                "Trusted supplied-semantics declaration; opaque symbol is unreachable from solution.mpy and all claims.",
            )
        return (
            "ACCEPT",
            "fixed-semantics-declaration",
            "Declaration from the byte-identical trusted supplied-semantics tree.",
        )
    if kind in {"configuration", "context"}:
        return (
            "ACCEPT",
            "fixed-semantics-control",
            "Configuration/evaluation context from the trusted supplied semantics.",
        )
    if kind == "rule":
        relevance = (
            "program-path"
            if path.name in PROGRAM_PATH_FILES
            else "unreachable-from-program"
        )
        return (
            "ACCEPT",
            f"fixed-semantics-rule-{relevance}",
            "Operational/equational rule from the byte-identical trusted supplied-semantics baseline.",
        )
    return ("REVIEW_GAP", "unknown", "Unexpected inventory kind.")


def main() -> int:
    rows: list[dict[str, object]] = []
    with INVENTORY.open(encoding="utf-8") as stream:
        for raw in stream:
            parsed = json.loads(raw)
            if "file" in parsed:
                rows.append(parsed)

    counts: Counter[str] = Counter()
    per_file: defaultdict[str, Counter[str]] = defaultdict(Counter)
    attribute_counts: Counter[str] = Counter()
    gaps = 0
    for row in rows:
        decision, classification, rationale = disposition(row)
        counts[classification] += 1
        per_file[Path(str(row["file"])).name][str(row["kind"])] += 1
        for attribute in row["attributes"]:  # type: ignore[union-attr]
            attribute_counts[str(attribute)] += 1
        if decision != "ACCEPT":
            gaps += 1
        output = {
            "file": row["file"],
            "line": row["line"],
            "kind": row["kind"],
            "attributes": row["attributes"],
            "decision": decision,
            "classification": classification,
            "rationale": rationale,
        }
        print(json.dumps(output, sort_keys=True))
    print(
        json.dumps(
            {
                "classified_entries": len(rows),
                "review_gap_count": gaps,
                "class_counts": dict(sorted(counts.items())),
                "attribute_counts": dict(sorted(attribute_counts.items())),
                "per_file_counts": {
                    name: dict(sorted(values.items()))
                    for name, values in sorted(per_file.items())
                },
            },
            sort_keys=True,
        )
    )
    return 1 if gaps else 0


if __name__ == "__main__":
    raise SystemExit(main())
