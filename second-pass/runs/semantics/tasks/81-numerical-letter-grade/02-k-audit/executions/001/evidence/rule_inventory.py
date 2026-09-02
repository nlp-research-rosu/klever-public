#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory for the supplied K tree and candidate proof."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


START = re.compile(
    r"^(requires)\b|^\s*(module|endmodule|imports|configuration|syntax|context(?:\s+alias)?|rule|claim)\b"
)


VERIFICATION_RULE_DECISIONS = {
    8: ("PINNING_GAP", "Macro duplicates the current branch body but is not linked to solution.mpy."),
    49: ("PINNING_GAP", "Macro duplicates the current function body but is not linked to solution.mpy."),
    59: ("SUBSTITUTED_PROGRAM_ENTRY", "Executes the duplicated macro body, not the submitted Module in solution.mpy."),
    66: ("ACCEPTED_DEFINITION", "String-to-code representation is a truthful local definition."),
    72: ("UNSOUND_OPERATIONAL_BRIDGE", "Preempts fixed Float equality with unconstrained gpaEqFour; no connection theorem."),
    76: ("ILLEGITIMATE_ORACLE_ALIAS", "Aliases eqFour to the same unconstrained result-bearing symbol used by execution."),
    77: ("ACCEPTED_TRUSTED_PRIMITIVE_ALIAS", "Aliases above to supplied-semantics gtF; conclusions remain conditional on gtF."),
    86: ("UNCONNECTED_ABSTRACT_ITERATION", "Defines iteration only for invented numericValues(.NumericGrades), with no concrete-list connection."),
    90: ("UNCONNECTED_ABSTRACT_ITERATION", "Defines Float-head iteration for invented numericValues input."),
    94: ("UNCONNECTED_ABSTRACT_ITERATION", "Defines Int-head iteration for invented numericValues input."),
    100: ("ORACLE_DEPENDENT_SUMMARY", "A+ branch mirrors duplicated code only under gpaEqFour's arbitrary interpretation."),
    102: ("ORACLE_DEPENDENT_SUMMARY", "A branch mirrors duplicated code only under gpaEqFour/gtF predicates."),
    105: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    109: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    114: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    120: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    127: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    135: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    144: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    154: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    165: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    177: ("ORACLE_DEPENDENT_SUMMARY", "Threshold summary is guard-disjoint but depends on the equality oracle."),
    190: ("ORACLE_DEPENDENT_SUMMARY", "Else summary is exhaustive only relative to the arbitrary predicates."),
    205: ("ACCEPTED_RECURSIVE_EQUATION", "Base case preserves the prefix."),
    206: ("ORACLE_DEPENDENT_RECURSION", "Structurally descends but appends oracle-dependent gradeOf(F)."),
    210: ("ORACLE_DEPENDENT_RECURSION", "Structurally descends after intToF but appends oracle-dependent gradeOf."),
    216: ("ACCEPTED_RECURSIVE_EQUATION", "Empty suffix preserves the prior loop variable."),
    217: ("ACCEPTED_RECURSIVE_EQUATION", "Structurally computes the last Float grade."),
    219: ("ACCEPTED_RECURSIVE_EQUATION", "Structurally computes the last Int grade after intToF."),
}

VERIFICATION_SYNTAX_DECISIONS = {
    7: ("PINNING_GAP", "Proof-local syntax for a copied branch body."),
    48: ("PINNING_GAP", "Proof-local syntax for a copied full function body."),
    58: ("SUBSTITUTED_PROGRAM_ENTRY", "Synthetic entry symbol used instead of loading solution.mpy."),
    65: ("ACCEPTED_DEFINITION", "Letter-string value constructor."),
    68: ("MIXED_TRUST", "eqFour is oracle-dependent; above delegates to supplied gtF."),
    70: ("ILLEGITIMATE_RESULT_ORACLE", "Opaque, total, no-evaluators Boolean controls execution and the postcondition."),
    82: ("UNCONNECTED_SYMBOLIC_INPUT", "Fresh grade-list datatype has no theorem connecting it to concrete ValSeq."),
    85: ("UNCONNECTED_SYMBOLIC_INPUT", "Fresh ValSeq wrapper consumed only by proof-local iterator bridges."),
    99: ("ORACLE_DEPENDENT_SUMMARY", "Result summary depends on gpaEqFour and opaque supplied comparisons."),
    204: ("ORACLE_DEPENDENT_SUMMARY", "Mathematical map is structurally total but inherits gradeOf's oracle."),
    215: ("ACCEPTED_DEFINITION", "Structurally total last-element summary."),
}

SPEC_CLAIM_DECISIONS = {
    6: ("TARGET_LIMITED", "Empty input is result-constraining but executes the duplicated body."),
    19: ("TARGET_ORACLE_DEPENDENT", "One-element A+ theorem assumes eqFour's unconstrained oracle."),
    37: ("TARGET_ORACLE_DEPENDENT", "One-element A theorem assumes oracle predicates."),
    56: ("TARGET_NOT_REAL_LIST_DOMAIN", "Universal theorem ranges over invented numericValues terms, not concrete ValSeq constructors."),
    75: ("AUXILIARY_NOT_REAL_LIST_DOMAIN", "Loop invariant ranges over invented numericValues terms and arbitrary continuation."),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kind_of(first_line: str) -> str:
    match = START.match(first_line)
    if not match:
        raise AssertionError(first_line)
    return (match.group(1) or match.group(2)).replace(" ", "_")


def flags_for(kind: str, block: str) -> list[str]:
    flags: list[str] = []
    for flag, needle in (
        ("function", "function"),
        ("total", "total"),
        ("functional", "functional"),
        ("symbol", "symbol("),
        ("no-evaluators", "no-evaluators"),
        ("priority", "priority("),
        ("simplification", "simplification"),
        ("concrete", "concrete"),
        ("owise", "owise"),
        ("macro", "macro"),
        ("strict", "strict"),
    ):
        if needle in block:
            flags.append(flag)
    if "symbol(" in block and "no-evaluators" in block:
        flags.append("opaque-symbol")
    if kind == "rule" and "simplification" not in flags and "macro" not in flags:
        flags.append("ordinary-rule")
    return flags


def verification_decision(kind: str, line: int) -> tuple[str, str]:
    if kind == "rule":
        return VERIFICATION_RULE_DECISIONS.get(
            line,
            ("UNMAPPED_CANDIDATE_RULE", "Inventory script requires an explicit reviewer decision."),
        )
    if kind == "syntax":
        return VERIFICATION_SYNTAX_DECISIONS.get(
            line,
            ("CANDIDATE_DECLARATION", "Proof-local declaration; see dependent rules."),
        )
    return ("CANDIDATE_STRUCTURE", "Module/import structure.")


def spec_decision(kind: str, line: int) -> tuple[str, str]:
    if kind == "claim":
        return SPEC_CLAIM_DECISIONS.get(
            line,
            ("UNMAPPED_CANDIDATE_CLAIM", "Inventory script requires an explicit reviewer decision."),
        )
    return ("CANDIDATE_STRUCTURE", "Module/import structure.")


def inventory_file(path: Path, root: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, text in enumerate(lines) if START.match(text)]
    records: list[dict[str, Any]] = []
    relative = path.relative_to(root).as_posix()
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        block = "\n".join(block_lines)
        kind = kind_of(lines[start])
        if relative.startswith("reference-semantics/"):
            decision = (
                "ACCEPTED_SELECTED_SUPPLIED_SEMANTICS",
                "Byte-identical to /reference/reference-semantics; fixed selected semantics boundary.",
            )
        elif relative == "verification.k":
            decision = verification_decision(kind, start + 1)
        elif relative == "spec.k":
            decision = spec_decision(kind, start + 1)
        else:
            decision = ("UNCLASSIFIED", "Unexpected K source.")
        records.append(
            {
                "source": relative,
                "source_sha256": sha256(path),
                "line_start": start + 1,
                "line_end": start + len(block_lines),
                "kind": kind,
                "flags": flags_for(kind, block),
                "summary": " ".join(part.strip() for part in block_lines[:2]),
                "decision": decision[0],
                "rationale": decision[1],
                "block": block,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted((args.root / "reference-semantics").rglob("*.k"))
    paths.extend([args.root / "verification.k", args.root / "spec.k"])
    records: list[dict[str, Any]] = []
    for path in paths:
        records.extend(inventory_file(path, args.root))

    args.json.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with args.csv.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "source",
                "source_sha256",
                "line_start",
                "line_end",
                "kind",
                "flags",
                "summary",
                "decision",
                "rationale",
            ],
        )
        writer.writeheader()
        for record in records:
            row = {key: record[key] for key in writer.fieldnames}
            row["flags"] = ";".join(record["flags"])
            writer.writerow(row)

    kinds = Counter(record["kind"] for record in records)
    decisions = Counter(record["decision"] for record in records)
    flags = Counter(flag for record in records for flag in record["flags"])
    print(f"file_count={len(paths)}")
    print(f"record_count={len(records)}")
    print(f"kinds={json.dumps(dict(sorted(kinds.items())), sort_keys=True)}")
    print(f"flags={json.dumps(dict(sorted(flags.items())), sort_keys=True)}")
    print(f"decisions={json.dumps(dict(sorted(decisions.items())), sort_keys=True)}")
    unmapped = [record for record in records if record["decision"].startswith("UNMAPPED")]
    print(f"unmapped_candidate_count={len(unmapped)}")
    for record in unmapped:
        print(f"UNMAPPED {record['source']}:{record['line_start']} {record['summary']}")
    return 1 if unmapped else 0


if __name__ == "__main__":
    raise SystemExit(main())
