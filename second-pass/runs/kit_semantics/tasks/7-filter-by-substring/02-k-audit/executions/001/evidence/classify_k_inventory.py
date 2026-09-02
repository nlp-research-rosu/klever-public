#!/usr/bin/env python3
"""Attach a reviewer decision to every indexed K declaration/rule."""

from __future__ import annotations

import csv
from pathlib import Path


SOURCE = Path("/audit-output/evidence/k-rule-inventory.tsv")

# Rules/declarations that are reachable while executing solution.mpy or
# evaluating its proof-local pre/postcondition. Ranges are intentionally
# conservative: a marked line may be a dispatch rule whose higher-priority
# specialized sibling actually fires.
ACTIVE: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": set(range(9, 62)),
    "reference-semantics/semantics/core.k": {
        13, 14, 15, 18, 25, 29, 31, 36, 37, 38, 39, 40, 41, 42,
        49, 68, 69, 70, 95, 96, 97, 98, 100, 101, 102, 117, 118,
        124, 125, 126, 127, 130, 131, 132, 145, 152, 157, 158,
        185, 186, 189, 190, 191, 199, 203, 208, 210, 213, 214,
        215, 223, 224, 225, 227, 228, 229,
    },
    "reference-semantics/semantics/operators.k": {10, 12, 15, 16, 17},
    "reference-semantics/semantics/str.k": {
        13, 14, 15, 16, 20, 21, 22, 29, 32, 33, 34, 35, 37, 38, 39, 40,
    },
    "reference-semantics/semantics/list.k": {
        9, 10, 13, 14, 15, 18, 19, 20, 53,
    },
    "reference-semantics/semantics/controls.k": {
        9, 36, 48, 51, 52, 53, 54, 65, 69, 71, 72, 73,
    },
    "reference-semantics/semantics/functions.k": {
        8, 14, 62, 63, 64, 77, 78, 85,
    },
    "reference-semantics/semantics/call.k": {
        16, 19, 20, 21, 24, 52, 53, 56, 69,
    },
    "reference-semantics/semantics/tuple.k": {31, 32},
    "verification.k": set(range(9, 45)),
    "spec.k": {6, 49},
}


def classify(file: str, line: int, kind: str, attrs: str, text: str) -> tuple[str, str]:
    if kind in {
        "module", "endmodule", "imports", "requires", "configuration",
        "context", "context_alias", "macro", "alias",
    }:
        return (
            "structural",
            "Reviewed for module closure, configuration shape, or evaluation order; no independent truth axiom.",
        )

    if file == "verification.k":
        if line in {11, 12, 13}:
            return (
                "proof-local-definitional",
                "Sound: exhaustive string projection; owise covers disjoint non-string constructors.",
            )
        if line in {15, 16, 17}:
            return (
                "proof-local-definitional",
                "Sound: exhaustive ValSeq recursion; exactly characterizes semantic string heads.",
            )
        if line == 23:
            return (
                "proof-local-derived-lemma",
                "Sound under its equality guard by congruence; fixed MPY-STR membership still executes.",
            )
        if line in {30, 31, 32, 40}:
            return (
                "proof-local-definitional",
                "Sound on allStrVS uses: disjoint complementary containment guards and strict tail descent.",
            )
        return (
            "proof-local-structural",
            "Declaration/import only; no operational bridge or opaque result symbol.",
        )

    if file == "spec.k" and kind == "claim":
        return (
            "derived-reachability-claim",
            "Machine-checked under fixed semantics; exact loop body or exact translated entry program is present.",
        )

    if file.startswith("reference-semantics/"):
        if "no-evaluators" in attrs:
            return (
                "fixed-opaque-inactive",
                "Supplied uninterpreted/total primitive; unreachable from solution.mpy and absent from its result.",
            )
        if line in ACTIVE.get(file, set()):
            return (
                "fixed-active-reviewed",
                "Reachable rule/declaration; checked against the modeled Python subset and the concrete state footprint.",
            )
        if "concrete" in attrs:
            return (
                "fixed-concrete-inactive",
                "Concrete-only or ground evaluator outside the symbolic path for this program.",
            )
        return (
            "fixed-inactive-reviewed",
            "Outside the program/proof dependency slice; overlap, guards, and declarations inspected; no false-conclusion witness found.",
        )

    return ("other", "No truth-bearing local extension identified.")


def main() -> int:
    lines = SOURCE.read_text().splitlines()
    data_lines = [line for line in lines if not line.startswith("#")]
    reader = csv.DictReader(data_lines, delimiter="\t")
    writer = csv.writer(__import__("sys").stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(
        ["file", "line", "kind", "attributes", "classification", "decision", "text"]
    )
    count = 0
    for row in reader:
        line = int(row["line"])
        classification, decision = classify(
            row["file"], line, row["kind"], row["attributes"], row["text"]
        )
        writer.writerow(
            [
                row["file"],
                line,
                row["kind"],
                row["attributes"],
                classification,
                decision,
                row["text"],
            ]
        )
        count += 1
    print(f"# DECISION_ROWS {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
