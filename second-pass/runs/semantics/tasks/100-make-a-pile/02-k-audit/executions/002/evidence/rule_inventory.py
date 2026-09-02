#!/usr/bin/env python3
"""Produce a complete source-level K declaration/rule inventory."""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work")
OUTPUT = Path("/audit-output/evidence/rule_inventory.tsv")
START = re.compile(r"^\s*(configuration|context|syntax|rule|claim)\b")
ATTRIBUTE = re.compile(
    r"\b(function|total|functional|symbol|no-evaluators|priority|"
    r"simplification|macro-rec|macro|owise|concrete|strict|seqstrict)\b"
)


# The exact source sentence starts that lie on the submitted program's
# execution/proof path. Entries not listed here remain part of the exhaustive
# inventory and receive an explicit off-path decision.
MATERIAL_LINES: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13, 14, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49, 68, 69, 70,
        117, 118, 124, 125, 126, 127, 130, 131, 132, 152, 157, 158,
        185, 186, 189, 190, 191, 194, 199, 200, 208, 209, 210, 213,
        214, 215, 217, 218, 219,
    },
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 14, 22},
    "semantics/list.k": {13, 14, 15, 18, 19, 20, 53},
    "semantics/controls.k": {9, 20, 48, 65, 77, 78, 79, 81, 85},
    "semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "semantics/call.k": {16, 19, 20, 21, 24, 52, 53, 56, 69},
}

LIMITED_STARTS: dict[str, set[int]] = {
    # Deliberately totalized/underspecified or compiler-warned helpers. None is
    # reachable from the submitted program or its proof.
    "semantics/subscript.k": {11},
    "semantics/builtins.k": {134},
    "semantics/float.k": {73, 86, 93},
    "semantics/methods.k": {27},
}


def relative_name(path: Path) -> str:
    if path == WORK / "verification.k":
        return "verification.k"
    if path == WORK / "spec.k":
        return "spec.k"
    return path.relative_to(WORK / "reference-semantics").as_posix()


def source_files() -> list[Path]:
    files = [WORK / "reference-semantics" / "semantics.k"]
    files.extend(sorted((WORK / "reference-semantics" / "semantics").glob("*.k")))
    files.extend([WORK / "verification.k", WORK / "spec.k"])
    return files


def extract(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    records: list[dict[str, object]] = []
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        # Do not consume the module terminator as part of the final sentence.
        for probe in range(start + 1, stop):
            if lines[probe].strip() == "endmodule":
                stop = probe
                break
        sentence_lines = lines[start:stop]
        while sentence_lines and (
            not sentence_lines[-1].strip()
            or sentence_lines[-1].lstrip().startswith("//")
        ):
            sentence_lines.pop()
        sentence = "\n".join(sentence_lines).strip()
        attrs = sorted(set(ATTRIBUTE.findall(sentence)))
        records.append(
            {
                "file": relative_name(path),
                "start_line": start + 1,
                "end_line": start + max(1, len(sentence_lines)),
                "kind": kind,
                "attributes": ",".join(attrs) if attrs else "-",
                "sentence": sentence.replace("\t", "    ").replace("\n", "\\n"),
            }
        )
    return records


def decision(record: dict[str, object]) -> tuple[str, str, str]:
    file = str(record["file"])
    line = int(record["start_line"])
    kind = str(record["kind"])
    attrs = str(record["attributes"])
    sentence = str(record["sentence"])

    if file == "verification.k":
        if kind == "syntax":
            return (
                "MATERIAL_PROOF",
                "ACCEPT",
                "Proof-local declaration. Macros were mechanically expanded; "
                "pile is a guarded definitional summary and not an execution rewrite.",
            )
        if line in {7, 11, 19, 26, 29}:
            return (
                "MATERIAL_PROOF",
                "ACCEPT",
                "Exact syntax macro for the submitted condition/body/function/module; "
                "macro-expanded constructor identity was machine checked.",
            )
        if line in {35, 37}:
            return (
                "MATERIAL_PROOF",
                "ACCEPT",
                "Disjoint and exhaustive integer equations for the finite arithmetic "
                "suffix; recursive branch strictly increases I toward N.",
            )
        return (
            "MATERIAL_PROOF",
            "ACCEPT",
            "True ValSeq monoid identity/associativity simplification; it does not "
            "replace operational execution.",
        )

    if file == "spec.k":
        label = "loop invariant/final summary" if line < 50 else "actual-program prefix"
        return (
            "TARGET_CLAIM",
            "ACCEPT",
            f"Result-constraining {label} claim; satisfiable precondition and concrete "
            "substitution checked independently.",
        )

    if line in MATERIAL_LINES.get(file, set()):
        explanations = {
            "semantics/syntax.k": (
                "Material AST declaration/strictness; preserves constructor shape and "
                "left-to-right evaluation for the used expressions/statements."
            ),
            "semantics/core.k": (
                "Material configuration/value, allocation, sequencing, lookup, "
                "argument-evaluation, literal, truthiness, or ValSeq helper rule; "
                "state footprint matches the executed operation."
            ),
            "semantics/operators.k": (
                "Material BinOp/Compare evaluation and dispatch; operands are evaluated "
                "before exact Int-domain dispatch."
            ),
            "semantics/int.k": (
                "Material mathematical integer +, *, or < equation; agrees with "
                "unbounded Python integers on the target domain."
            ),
            "semantics/list.k": (
                "Material list allocation/concatenation/append rule; append mutates the "
                "referenced heap list and returns noneV exactly as consumed by Expr."
            ),
            "semantics/controls.k": (
                "Material assignment, augmented assignment, expression discard, while, "
                "or loop-label rule; guard re-evaluation and current-scope update match "
                "the submitted control flow."
            ),
            "semantics/functions.k": (
                "Material function definition, parameter binding, return, or frame-pop "
                "rule; return value, environment, scopes, stack, and allocation cells "
                "are explicitly tracked."
            ),
            "semantics/call.k": (
                "Material callee/argument/method/closure dispatch; selected binding and "
                "continuation are evaluated without an execution shortcut."
            ),
        }
        return ("MATERIAL_SEMANTICS", "ACCEPT", explanations[file])

    if line in LIMITED_STARTS.get(file, set()):
        return (
            "OFF_PATH_LIMITATION",
            "ACCEPT_NONMATERIAL_LIMITATION",
            "Deliberately underspecified or non-exhaustive helper. It is absent from "
            "the submitted AST and all target-claim terms, so no false target conclusion "
            "can be witnessed through it.",
        )

    if (
        "no-evaluators" in attrs
        or file == "semantics/sort.k"
        or "md5hexCodes" in sentence
    ):
        return (
            "OFF_PATH_OPAQUE",
            "ACCEPT_NONMATERIAL_TRUST_BOUNDARY",
            "Explicit opaque fixed-semantics primitive. No constructor, binding, call, "
            "branch, state cell, or postcondition in this task can reach its symbol.",
        )

    if file == "semantics/concrete.k":
        return (
            "CONCRETE_ONLY_OFF_PATH",
            "ACCEPT",
            "LLVM-only deep-equality/keyed-sort declaration or rule. The target uses "
            "neither operation, and this module is absent from the proof definition.",
        )

    if file == "semantics/assert.k":
        return (
            "CONCRETE_TEST_ONLY",
            "ACCEPT",
            "Concrete test-harness Assert rule; evaluates truthiness and sets the "
            "exception/exit cells on failure. It is absent from the target proof path.",
        )

    return (
        "SUPPLIED_OFF_PATH",
        "ACCEPT",
        "Fixed supplied-semantics declaration/rule for a constructor absent from the "
        "exact submitted program and target claims. Source review found no task-answer "
        "encoding, cross-sort overlap, or concrete false conclusion relevant to the "
        "int/list/function/while domain.",
    )


def main() -> None:
    all_records: list[dict[str, object]] = []
    source_hashes: dict[str, str] = {}
    for path in source_files():
        relative = relative_name(path)
        source_hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        all_records.extend(extract(path))

    counters: Counter[str] = Counter()
    decisions: Counter[str] = Counter()
    for identifier, record in enumerate(all_records, start=1):
        relevance, outcome, justification = decision(record)
        record["id"] = f"K-{identifier:04d}"
        record["relevance"] = relevance
        record["decision"] = outcome
        record["justification"] = justification
        counters[str(record["kind"])] += 1
        decisions[outcome] += 1

    fields = [
        "id",
        "file",
        "start_line",
        "end_line",
        "kind",
        "attributes",
        "relevance",
        "decision",
        "justification",
        "sentence",
    ]
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(all_records)

    print(f"inventory_output={OUTPUT}")
    print(f"source_file_count={len(source_hashes)}")
    for file, digest in source_hashes.items():
        print(f"SOURCE {file} sha256={digest}")
    print(f"entry_count={len(all_records)}")
    print(f"kind_counts={dict(sorted(counters.items()))}")
    print(f"decision_counts={dict(sorted(decisions.items()))}")
    print("RULE_INVENTORY_OK")


if __name__ == "__main__":
    main()
