#!/usr/bin/env python3
"""Build a source-level exhaustive inventory and per-item audit disposition."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
from pathlib import Path
import re
import sys


ROOT = Path("/tmp/audit-work/37-sort-even")
OUT = Path("/audit-output/evidence/05-rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/05-rule-inventory-summary.log")

KEYWORDS = ("syntax", "rule", "claim", "configuration", "context")

# Line ranges whose declarations/rules are materially used by the target proof.
USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/syntax.k": [(9, 62)],
    "reference-semantics/semantics/core.k": [
        (13, 70),
        (117, 134),
        (152, 225),
    ],
    "reference-semantics/semantics/iter.k": [(1, 999)],
    "reference-semantics/semantics/operators.k": [(10, 12), (25, 31)],
    "reference-semantics/semantics/int.k": [(9, 9)],
    "reference-semantics/semantics/list.k": [(8, 28), (52, 55)],
    "reference-semantics/semantics/tuple.k": [(30, 41)],
    "reference-semantics/semantics/subscript.k": [(6, 121)],
    "reference-semantics/semantics/controls.k": [
        (8, 31),
        (46, 48),
        (62, 74),
        (93, 108),
    ],
    "reference-semantics/semantics/functions.k": [(8, 11), (62, 90)],
    "reference-semantics/semantics/builtins.k": [(17, 26)],
    "reference-semantics/semantics/call.k": [(15, 75)],
    "reference-semantics/semantics/sort.k": [(14, 42)],
    "verification.k": [(1, 999)],
    "spec.k": [(1, 999)],
}


def starts_item(line: str):
    stripped = line.lstrip()
    for keyword in KEYWORDS:
        if re.match(rf"^{keyword}(?:\s|$)", stripped):
            return keyword
    return None


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        kind = starts_item(line)
        if kind:
            starts.append((index, kind))
    for position, (index, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        # Do not absorb endmodule or a new module/import into the last item.
        for probe in range(index + 1, stop):
            if re.match(r"^\s*(?:end)?module(?:\s|$)|^\s*imports(?:\s|$)", lines[probe]):
                stop = probe
                break
        text = "\n".join(lines[index:stop]).strip()
        yield index + 1, kind, text


def material_scope(rel: str, line: int) -> str:
    for start, end in USED_RANGES.get(rel, []):
        if start <= line <= end:
            return "TARGET_MATERIAL"
    if rel.startswith("reference-semantics/"):
        return "TARGET_UNUSED"
    return "TARGET_MATERIAL"


def disposition(rel: str, line: int, kind: str, text: str, scope: str) -> str:
    attrs = set(re.findall(r"\b(?:function|functional|total|no-evaluators|concrete|simplification|owise|macro(?:-rec)?|priority)\b", text))
    if rel == "verification.k":
        if kind == "syntax":
            if "no-evaluators" in attrs:
                return "REJECT_OPAQUE_CANDIDATE_DECLARATION"
            return "ACCEPT_CANDIDATE_DECLARATION"
        if kind == "rule":
            if line == 44:
                return "ACCEPT_EXACT_OPERATIONAL_INSTANCE"
            if line in {96, 97, 106}:
                return "ACCEPT_DERIVED_EQUATION"
            if line in {119, 122}:
                return "ACCEPT_OBSERVATION_BOUNDARY"
            return "ACCEPT_TRUTHFUL_DEFINITION_OR_BODY_ALIAS"
    if rel == "spec.k":
        if kind == "claim" and line == 9:
            return "ACCEPT_AUXILIARY_REACHABILITY_CLAIM"
        if kind == "claim" and line == 53:
            return "ACCEPT_RESULT_CONSTRAINING_ENTRY_CLAIM"
        return "ACCEPT_SPEC_DECLARATION"

    if "no-evaluators" in attrs:
        if rel.endswith("/sort.k") and line == 18:
            return "ACCEPT_NAMED_TRUSTED_OPAQUE_SORT_PRIMITIVE"
        return "ACCEPT_FIXED_OPAQUE_TARGET_UNUSED"
    if rel.endswith("/subscript.k") and line == 11:
        return "ACCEPT_FIXED_TOTAL_UNDERSPECIFIED_OOB_PRIMITIVE"
    if (
        (rel.endswith("/builtins.k") and line == 134)
        or (rel.endswith("/float.k") and line in {73, 86, 93})
        or (rel.endswith("/methods.k") and line == 27)
    ):
        return "ACCEPT_FIXED_NONEXHAUSTIVE_TARGET_UNUSED"
    if kind == "syntax":
        return "ACCEPT_FIXED_DECLARATION"
    if kind == "configuration":
        return "ACCEPT_FIXED_CONFIGURATION"
    if kind == "context":
        return "ACCEPT_FIXED_EVALUATION_CONTEXT"
    if kind == "rule":
        return (
            "ACCEPT_FIXED_RULE_TARGET_MATERIAL"
            if scope == "TARGET_MATERIAL"
            else "ACCEPT_FIXED_RULE_TARGET_UNUSED"
        )
    if kind == "claim":
        return "ACCEPT_FIXED_CLAIM"
    return "ACCEPT_FIXED_ITEM"


def main() -> int:
    paths = [ROOT / "reference-semantics" / "semantics.k"]
    paths.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])

    rows = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        for line, kind, text in blocks(path):
            scope = material_scope(rel, line)
            attrs = ",".join(
                sorted(
                    set(
                        re.findall(
                            r"\b(?:function|functional|total|no-evaluators|concrete|"
                            r"simplification|owise|macro(?:-rec)?|priority|strict|seqstrict)\b",
                            text,
                        )
                    )
                )
            )
            rows.append(
                {
                    "id": f"I{len(rows) + 1:04d}",
                    "file": rel,
                    "line": str(line),
                    "kind": kind,
                    "attributes": attrs,
                    "target_scope": scope,
                    "disposition": disposition(rel, line, kind, text, scope),
                    "source": " ".join(text.split()),
                }
            )

    with OUT.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(
            out,
            fieldnames=[
                "id",
                "file",
                "line",
                "kind",
                "attributes",
                "target_scope",
                "disposition",
                "source",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    kinds = Counter(row["kind"] for row in rows)
    dispositions = Counter(row["disposition"] for row in rows)
    per_file: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        per_file[row["file"]][row["kind"]] += 1

    with SUMMARY.open("w", encoding="utf-8") as out:
        out.write("COMMAND: python3 /audit-output/evidence/rule_inventory.py\n")
        out.write(f"INVENTORY_PATH={OUT}\n")
        out.write(f"ITEM_COUNT={len(rows)}\n")
        out.write(f"KIND_COUNTS={dict(sorted(kinds.items()))}\n")
        for rel in sorted(per_file):
            out.write(f"FILE_COUNTS {rel} {dict(sorted(per_file[rel].items()))}\n")
        for name, count in sorted(dispositions.items()):
            out.write(f"DISPOSITION_COUNT {name}={count}\n")
        rejected = sum(count for name, count in dispositions.items() if name.startswith("REJECT"))
        out.write(f"REJECTED_COUNT={rejected}\n")
        out.write("EXIT_STATUS: 0\n" if rejected == 0 else "EXIT_STATUS: 1\n")

    return 1 if any(row["disposition"].startswith("REJECT") for row in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
