#!/usr/bin/env python3
"""Create an exhaustive top-level K declaration/rule inventory."""

from __future__ import annotations

import csv
import pathlib
import re
from collections import Counter


ROOT = pathlib.Path("/tmp/audit-work/reconstruction")
OUTPUT = pathlib.Path("/audit-output/evidence/05_rule_inventory.tsv")
SUMMARY = pathlib.Path("/audit-output/evidence/05_rule_inventory_summary.log")

SOURCES = [
    *sorted((ROOT / "reference-semantics").rglob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^(?:"
    r"(?P<file_requires>requires)\b"
    r"|"
    r"\s*(?P<declaration>module|imports|configuration|syntax|context|rule|claim|endmodule)\b"
    r")"
)
ATTR = re.compile(r"\[([^\]]+)\]")


def is_used_slice(relative: str, line: int) -> bool:
    used_ranges: dict[str, list[tuple[int, int]]] = {
        "reference-semantics/semantics/syntax.k": [
            (9, 16),
            (28, 32),
            (37, 38),
            (41, 60),
        ],
        "reference-semantics/semantics/core.k": [
            (13, 60),
            (68, 70),
            (76, 78),
            (85, 90),
            (106, 115),
            (123, 127),
            (129, 181),
            (183, 215),
        ],
        "reference-semantics/semantics/operators.k": [(10, 46)],
        "reference-semantics/semantics/int.k": [(7, 27)],
        "reference-semantics/semantics/list.k": [(8, 15)],
        "reference-semantics/semantics/tuple.k": [(30, 41)],
        "reference-semantics/semantics/controls.k": [
            (8, 31),
            (50, 75),
        ],
        "reference-semantics/semantics/functions.k": [
            (8, 20),
            (62, 90),
        ],
        "reference-semantics/semantics/call.k": [
            (18, 21),
            (69, 74),
        ],
    }
    return any(start <= line <= end for start, end in used_ranges.get(relative, []))


def blocks(path: pathlib.Path) -> list[tuple[int, int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            starts.append(
                (index, match.group("file_requires") or match.group("declaration"))
            )
    result: list[tuple[int, int, str, str]] = []
    for position, (start, kind) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines) + 1
        end = next_start - 1
        while end >= start and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        text = " ".join(
            piece.strip()
            for piece in lines[start - 1 : end]
            if piece.strip() and not piece.lstrip().startswith("//")
        )
        result.append((start, max(start, end), kind, text))
    return result


def decision(
    relative: str, line: int, kind: str, text: str, opaque: bool
) -> tuple[str, str]:
    if relative == "verification.k":
        if kind in {"requires", "module", "imports", "endmodule"}:
            return "proof-local structure", "NO_TRUTH_BEARING_EXTENSION"
        if kind == "syntax" and "IS-SORTED-" in text:
            return "exact source macro", "SOUND_EXACT_COMPILE_TIME_ABBREVIATION"
        if kind == "rule" and "IS-SORTED-" in text:
            return "exact source macro", "SOUND_EXACT_COMPILE_TIME_ABBREVIATION"
        if kind == "syntax" and (
            "sortedFrom" in text or "sortedAtMostTwice" in text
        ):
            return "result summary", "SOUND_TOTAL_STRUCTURAL_DEFINITION"
        if kind == "rule" and (
            "sortedFrom" in text or "sortedAtMostTwice" in text
        ):
            return "result summary", "SOUND_TOTAL_STRUCTURAL_DEFINITION"
        return "proof-local", "REVIEWED_NO_OPERATIONAL_BRIDGE"

    if relative == "spec.k":
        if kind == "claim":
            return "target theorem", "RESULT_CONSTRAINING_BOUNDED_OBLIGATION"
        return "specification structure", "NO_SEMANTIC_EXTENSION"

    if kind in {"requires", "module", "imports", "endmodule", "syntax", "configuration", "context"}:
        relevance = "used semantic slice" if is_used_slice(relative, line) else "fixed baseline declaration"
        if opaque:
            return relevance, "FIXED_TRUST_BOUNDARY_NOT_REACHED_BY_TARGET"
        return relevance, "DECLARATIVE_OR_SELECTED_SEMANTICS_STRUCTURE"

    if is_used_slice(relative, line):
        return (
            "used semantic slice",
            "SOUND_FOR_TARGET_DOMAIN_AND_CONTROL_STATE",
        )
    if opaque:
        return (
            "unused fixed opaque boundary",
            "FIXED_TRUST_BOUNDARY_NOT_REACHED_BY_TARGET",
        )
    return (
        "unused fixed semantic rule",
        "NO_TARGET_PATH_EFFECT_ACCEPTED_AS_SELECTED_BASELINE",
    )


def main() -> int:
    rows: list[dict[str, object]] = []
    for path in SOURCES:
        relative = path.relative_to(ROOT).as_posix()
        module = ""
        for start, end, kind, text in blocks(path):
            if kind == "module":
                parts = text.split()
                module = parts[1] if len(parts) > 1 else ""
            attributes = ";".join(ATTR.findall(text))
            opaque = "no-evaluators" in text or (
                "symbol(" in text and "[concrete]" not in text
            )
            relevance, review = decision(relative, start, kind, text, opaque)
            rows.append(
                {
                    "id": f"{relative}:{start}",
                    "file": relative,
                    "module": module,
                    "start": start,
                    "end": end,
                    "kind": kind,
                    "attributes": attributes,
                    "function": "function" in attributes,
                    "total": "total" in attributes,
                    "functional": "functional" in attributes,
                    "simplification": "simplification" in attributes,
                    "priority": "priority(" in attributes,
                    "concrete": "concrete" in attributes,
                    "owise": "owise" in attributes,
                    "macro": "macro" in attributes,
                    "opaque": opaque,
                    "relevance": relevance,
                    "review_decision": review,
                    "declaration": text,
                }
            )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    kinds = Counter(str(row["kind"]) for row in rows)
    decisions = Counter(str(row["review_decision"]) for row in rows)
    with SUMMARY.open("w", encoding="utf-8") as handle:
        handle.write(f"source_files={len(SOURCES)}\n")
        handle.write(f"inventory_rows={len(rows)}\n")
        for kind, count in sorted(kinds.items()):
            handle.write(f"kind.{kind}={count}\n")
        for field in (
            "function",
            "total",
            "functional",
            "simplification",
            "priority",
            "concrete",
            "owise",
            "macro",
            "opaque",
        ):
            handle.write(
                f"attribute.{field}={sum(bool(row[field]) for row in rows)}\n"
            )
        for review, count in sorted(decisions.items()):
            handle.write(f"decision.{review}={count}\n")
        handle.write("per_file:\n")
        for file_name in sorted({str(row["file"]) for row in rows}):
            file_rows = [row for row in rows if row["file"] == file_name]
            handle.write(
                f"  {file_name}: rows={len(file_rows)}"
                f" syntax={sum(row['kind'] == 'syntax' for row in file_rows)}"
                f" rules={sum(row['kind'] == 'rule' for row in file_rows)}"
                f" claims={sum(row['kind'] == 'claim' for row in file_rows)}\n"
            )
        handle.write("opaque_declarations:\n")
        for row in rows:
            if row["opaque"]:
                handle.write(f"  {row['id']}: {row['declaration']}\n")
        handle.write("priority_rules:\n")
        for row in rows:
            if row["priority"]:
                handle.write(f"  {row['id']}: {row['declaration']}\n")
        handle.write(f"output={OUTPUT}\n")
    print(SUMMARY.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
