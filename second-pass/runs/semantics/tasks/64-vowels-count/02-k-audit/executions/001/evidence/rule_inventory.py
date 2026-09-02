#!/usr/bin/env python3
"""Emit an exhaustive source-sentence inventory for the supplied K proof."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path("/tmp/audit-work/fresh")
START = re.compile(r"^\s*(syntax|rule|claim|configuration|context)\b")
MODULE = re.compile(r"^\s*(?:module|endmodule)\b")
ATTR = re.compile(
    r"\b(function|total|functional|macro|macro-rec|concrete|simplification|"
    r"no-evaluators|owise)\b|priority\([^)]*\)|symbol\([^)]*\)"
)

# Source rules/declarations that participate in parsing or executing solution.mpy.
USED_LINES: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        13, 15, 25, 31, 34, 36, 37, 38, 39, 40, 41, 42, 49,
        68, 124, 125, 126, 127, 130, 131, 132, 145, 152, 157,
        158, 185, 186, 189, 190, 191, 194, 195, 199, 200,
        208, 209, 210, 213, 214, 215,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/operators.k": {12, 15, 16, 17},
    "reference-semantics/semantics/int.k": {9, 11},
    "reference-semantics/semantics/str.k": {
        8, 9, 13, 14, 15, 16, 20, 21, 22, 29, 32, 33, 34, 35,
        37, 38, 39, 40,
    },
    "reference-semantics/semantics/methods.k": {
        10, 19, 112, 113, 115, 116, 140, 142, 143, 154, 155, 156,
    },
    "reference-semantics/semantics/controls.k": {
        9, 20, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85,
    },
    "reference-semantics/semantics/functions.k": {
        8, 14, 63, 64, 78, 80, 85,
    },
    "reference-semantics/semantics/call.k": {
        16, 19, 20, 21, 24, 69,
    },
    "reference-semantics/semantics/tuple.k": {31, 32},
}


def sentences(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) or MODULE.match(line)
    ]
    starts.append(len(lines))
    for position, start in enumerate(starts[:-1]):
        match = START.match(lines[start])
        if not match:
            continue
        end = starts[position + 1]
        body_lines = [
            line.strip()
            for line in lines[start:end]
            if line.strip() and not line.lstrip().startswith("//")
        ]
        yield start + 1, match.group(1), " ".join(body_lines)


def decision(relative: str, line: int, kind: str, body: str) -> tuple[str, str]:
    if relative == "verification.k":
        if kind == "rule" and line == 78:
            return (
                "REJECT_UNSOUND_OPERATIONAL_BRIDGE",
                "omits env and other theorem-fixed cells; ground env=0 witness proves false frame-1 update",
            )
        if kind == "rule" and line in {8, 12, 13, 24, 25, 34, 35, 39}:
            return (
                "ACCEPT_MATHEMATICAL_DEFINITION",
                "truthful structural equation with disjoint constructor coverage and descent",
            )
        if kind == "rule" and line in {45, 58, 68}:
            return (
                "ACCEPT_EXACT_MACRO",
                "macro expansion mechanically matches submitted solution syntax",
            )
        return (
            "ACCEPT_CANDIDATE_DECLARATION",
            "declaration is conservative; its associated rules are separately inventoried",
        )

    if relative == "spec.k":
        if kind == "claim" and line == 6:
            return (
                "ACCEPT_PROVED_AUXILIARY_CLAIM",
                "fresh bridge-free proof closes; exact loop body and env=1 state",
            )
        if kind == "claim" and line == 46:
            return (
                "TARGET_CLAIM_CONTAMINATED_BY_REJECTED_BRIDGE",
                "result-constraining target closes only in theory containing rejected bridge",
            )

    if relative.startswith("reference-semantics/"):
        attributes = set(ATTR.findall(body))
        if "no-evaluators" in body or (
            "symbol(" in body and "concrete" in body
        ):
            return (
                "ACCEPT_FIXED_OPAQUE_OFF_PATH",
                "supplied primitive is not reachable from solution.mpy",
            )
        if relative == "reference-semantics/semantics/str.k" and line in {
            13, 14, 15, 16
        }:
            return (
                "ACCEPT_FIXED_ASCII_MODEL_LIMITATION",
                "literal conversion is explicitly ASCII-only; all program literals are ASCII",
            )
        if relative == "reference-semantics/semantics/methods.k" and line in {
            19, 140, 142, 143, 154, 155, 156
        }:
            return (
                "ACCEPT_FIXED_ASCII_MODEL_LIMITATION",
                "lower() is ASCII code mapping, causing a documented CPython Unicode bridge gap",
            )
        if line in USED_LINES.get(relative, set()):
            return (
                "ACCEPT_FIXED_USED_PATH",
                "fixed supplied rule/declaration implements the used construct without task-specific conclusion",
            )
        return (
            "ACCEPT_FIXED_OFF_PATH",
            "byte-identical supplied-semantics sentence; construct is unreachable from solution.mpy",
        )

    return ("REVIEW_GAP", "unclassified source sentence")


def main() -> int:
    paths = [ROOT / "reference-semantics" / "semantics.k"]
    paths.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])

    writer = csv.writer(sys.stdout, dialect="excel-tab", lineterminator="\n")
    writer.writerow(
        ["source", "line", "kind", "attributes", "decision", "reason", "sentence"]
    )
    counts: dict[str, int] = {}
    total = 0
    for path in paths:
        relative = str(path.relative_to(ROOT))
        for line, kind, body in sentences(path):
            attributes = sorted(set(match.group(0) for match in ATTR.finditer(body)))
            verdict, reason = decision(relative, line, kind, body)
            writer.writerow(
                [
                    relative,
                    line,
                    kind,
                    ",".join(attributes) or "-",
                    verdict,
                    reason,
                    body,
                ]
            )
            counts[kind] = counts.get(kind, 0) + 1
            total += 1

    print(
        "# counts "
        + " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
        + f" total={total}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
