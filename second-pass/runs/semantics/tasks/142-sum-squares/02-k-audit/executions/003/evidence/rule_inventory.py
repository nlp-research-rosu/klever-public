#!/usr/bin/env python3
"""Generate an exhaustive declaration/rule inventory from audited K sources."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path("/tmp/audit-work/reconstruction")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")

START_RE = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias)\b"
)
MODULE_RE = re.compile(r"^\s*module\s+(\S+)")
END_MODULE_RE = re.compile(r"^\s*endmodule\b")


REACHABLE_LINES: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {
        9,
        15,
        28,
        30,
        32,
        37,
        41,
        44,
        45,
        49,
        50,
        53,
        56,
        57,
        60,
        61,
    },
    "reference-semantics/semantics/core.k": {
        13,
        14,
        18,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        126,
        127,
        130,
        131,
        132,
        152,
        185,
        186,
        189,
        190,
        191,
        194,
        199,
        200,
        208,
        209,
        210,
        213,
        214,
        215,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/list.k": {9, 10},
    "reference-semantics/semantics/operators.k": {
        12,
        15,
        16,
        17,
    },
    "reference-semantics/semantics/int.k": {
        9,
        14,
        15,
        19,
        20,
        26,
    },
    "reference-semantics/semantics/controls.k": {
        9,
        20,
        51,
        52,
        53,
        54,
        65,
        69,
        71,
        72,
        73,
        85,
    },
    "reference-semantics/semantics/tuple.k": {
        31,
        32,
    },
    "reference-semantics/semantics/functions.k": {
        8,
        63,
        64,
        78,
        80,
        85,
    },
    "reference-semantics/semantics/call.k": {
        19,
        20,
        21,
        69,
    },
}


def source_files() -> list[Path]:
    files = sorted(SEMANTICS.rglob("*.k"))
    files.extend([ROOT / "verification.k", ROOT / "spec.k"])
    return files


def relpath(path: Path) -> str:
    return str(path.relative_to(ROOT))


def clean_record(lines: list[str]) -> list[str]:
    # Comments and blank lines that introduce the following declaration are
    # not part of the current record.
    while lines and (not lines[-1].strip() or lines[-1].lstrip().startswith("//")):
        lines.pop()
    return lines


def records(path: Path) -> Iterable[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    module = "<outside-module>"
    starts: list[tuple[int, str, str]] = []
    module_at_line: dict[int, str] = {}
    for number, line in enumerate(lines, 1):
        module_match = MODULE_RE.match(line)
        if module_match:
            module = module_match.group(1)
        module_at_line[number] = module
        if END_MODULE_RE.match(line):
            module = "<outside-module>"
        start_match = START_RE.match(line)
        if start_match:
            starts.append((number, start_match.group(1), module_at_line[number]))

    boundaries = [number for number, _, _ in starts]
    for index, (number, kind, record_module) in enumerate(starts):
        next_number = boundaries[index + 1] if index + 1 < len(boundaries) else len(lines) + 1
        # Stop at endmodule if it occurs before the next declaration.
        end = next_number
        for candidate in range(number + 1, next_number):
            if END_MODULE_RE.match(lines[candidate - 1]):
                end = candidate
                break
        body_lines = clean_record(lines[number - 1 : end - 1])
        text = "\n".join(line.rstrip() for line in body_lines).strip()
        yield {
            "file": relpath(path),
            "line": number,
            "module": record_module,
            "kind": kind,
            "text": text,
        }


def classify(record: dict[str, object]) -> tuple[str, str, str, str]:
    kind = str(record["kind"])
    text = str(record["text"])
    file = str(record["file"])
    line = int(record["line"])

    attributes = sorted(
        set(
            re.findall(
                r"\b(functional|function|total|macro-rec|macro|priority|"
                r"owise|simplification|anywhere|symbol|hook|no-evaluators|"
                r"strict|seqstrict)\b",
                text,
            )
        )
    )

    if kind == "configuration":
        classification = "configuration"
    elif kind == "context":
        classification = "evaluation-context"
    elif kind == "claim":
        classification = "reachability-claim"
    elif kind == "syntax":
        if "macro" in attributes or "macro-rec" in attributes:
            classification = "macro-declaration"
        elif "no-evaluators" in attributes or "symbol" in attributes:
            classification = "opaque/symbol-declaration"
        elif "function" in attributes or "functional" in attributes:
            classification = "equational-symbol-declaration"
        else:
            classification = "constructor/control-syntax"
    elif kind == "rule":
        if "<k>" in text or re.search(r"<[A-Za-z-]+>", text):
            classification = "operational-rule"
        else:
            classification = "equational-or-macro-rule"
        if "priority" in attributes:
            classification += "+priority"
        if "owise" in attributes:
            classification += "+owise"
        if "simplification" in attributes:
            classification += "+simplification"
    else:
        classification = kind

    if file in ("verification.k", "spec.k"):
        scope = "candidate-proof"
    else:
        scope = "launcher-trusted-supplied-semantics"

    if file == "verification.k":
        if kind == "rule" and line in {15, 17}:
            decision = (
                "ACCEPT_WITH_LIMITATION: exact structural iterator definition "
                "for proof-local intVals; disjoint from fixed vCons/.ValSeq "
                "rules and preserves continuation/cells, but its equivalence "
                "to fixed concrete list representation is informal"
            )
        elif kind == "rule" and line in {24, 26, 28}:
            decision = (
                "ACCEPT: truthful integer contribution equations; guards are "
                "pairwise disjoint and exhaustive for divisors 3 and 4"
            )
        elif kind == "rule" and line in {33, 34, 39, 40, 44, 45}:
            decision = (
                "ACCEPT: constructor-complete structural recursion with strict "
                "descent; equations match accumulator/index/last-value updates"
            )
        elif kind == "rule" and line in {49, 78}:
            decision = (
                "ACCEPT: macro expansion; constructor identity to translated "
                "loop/function body checked independently"
            )
        elif kind == "syntax":
            decision = (
                "ACCEPT: proof-local constructor or symbol declaration; "
                "equations/uses are inventoried separately"
            )
        else:
            decision = "ACCEPT: candidate proof record; reviewed separately"
        reachability = "proof-critical"
    elif file == "spec.k":
        decision = "CLAIM: adequacy and closure reviewed separately"
        reachability = "target-claim"
    else:
        is_reachable = line in REACHABLE_LINES.get(file, set())
        reachability = "reachable-proof-slice" if is_reachable else "unused-by-target"
        if is_reachable:
            decision = (
                "ACCEPT_FIXED_REACHABLE: intact supplied rule/declaration; "
                "manual control/evaluation/state review found no mismatch on "
                "the target's integer-list execution slice"
            )
        else:
            decision = (
                "ACCEPT_FIXED_UNUSED: intact launcher-trusted supplied "
                "semantics and unreachable from all target claims; no "
                "candidate extension or identified false-conclusion witness"
            )

    return classification, ",".join(attributes), scope, f"{reachability}; {decision}"


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    all_records: list[dict[str, object]] = []
    for path in source_files():
        all_records.extend(records(path))

    fieldnames = [
        "id",
        "scope",
        "file",
        "line",
        "module",
        "kind",
        "classification",
        "attributes",
        "assessment",
        "text",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for record in all_records:
            classification, attributes, scope, assessment = classify(record)
            writer.writerow(
                {
                    "id": f"{record['file']}:{record['line']}",
                    "scope": scope,
                    "file": record["file"],
                    "line": record["line"],
                    "module": record["module"],
                    "kind": record["kind"],
                    "classification": classification,
                    "attributes": attributes,
                    "assessment": assessment,
                    "text": one_line(str(record["text"])),
                }
            )

    by_kind: dict[str, int] = {}
    by_scope: dict[str, int] = {}
    by_class: dict[str, int] = {}
    for record in all_records:
        classification, _, scope, _ = classify(record)
        by_kind[str(record["kind"])] = by_kind.get(str(record["kind"]), 0) + 1
        by_scope[scope] = by_scope.get(scope, 0) + 1
        by_class[classification] = by_class.get(classification, 0) + 1

    raw_text = "\n".join(str(record["text"]) for record in all_records)
    print(f"source_file_count={len(source_files())}")
    print(f"inventory_record_count={len(all_records)}")
    print(f"kind_counts={dict(sorted(by_kind.items()))}")
    print(f"scope_counts={dict(sorted(by_scope.items()))}")
    print(f"classification_counts={dict(sorted(by_class.items()))}")
    functional_count = len(re.findall(r"\bfunctional\b", raw_text))
    simplification_count = len(re.findall(r"\bsimplification\b", raw_text))
    opaque_count = len(re.findall(r"\bno-evaluators\b", raw_text))
    print(f"functional_attribute_count={functional_count}")
    print(f"simplification_attribute_count={simplification_count}")
    print(f"opaque_no_evaluators_count={opaque_count}")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
