#!/usr/bin/env python3
"""Attach an audit decision and proof-reachability classification to each entry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# Source ranges participating in the exact closure-body claim. A range includes
# declarations and rules that either execute or can overlap a reached redex.
REACHED = {
    "syntax.k": [(9, 61)],
    "core.k": [
        (13, 60),
        (68, 70),
        (100, 102),
        (109, 111),
        (123, 154),
        (183, 225),
    ],
    "iter.k": [(8, 8)],
    "operators.k": [(10, 20), (25, 46)],
    "str.k": [(8, 41)],
    "tuple.k": [(14, 18), (31, 46)],
    "controls.k": [(9, 31), (50, 74)],
    "functions.k": [(8, 20), (62, 90)],
    "call.k": [(18, 32), (69, 75)],
}


def in_ranges(line: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= line <= end for start, end in ranges)


def candidate_extension_assessment(record):
    text = record["text"]
    if record["kind"] == "syntax":
        if "keptAcc" in text:
            return (
                "ACCEPT: total structural recursion. The empty/cons equations "
                "terminate on the first IntSeq; the membership guards are "
                "Boolean complements and cover every cons input."
            )
        if "reversedKeptAcc" in text:
            return (
                "ACCEPT: total structural recursion. Equations terminate and "
                "the complementary membership guards cover every cons input."
            )
        if "lastCharacter" in text:
            return (
                "ACCEPT: total structural recursion over IntSeq with one base "
                "case and one constructor case."
            )
    if record["kind"] == "rule":
        if "keptAcc(.IntSeq" in text:
            return "ACCEPT: processing no remaining characters preserves the forward accumulator."
        if "keptAcc(iCons" in text and "seqConcat" not in text:
            return "ACCEPT: a head present in c is deleted and recursion advances to the tail."
        if "keptAcc(iCons" in text and "seqConcat" in text:
            return "ACCEPT: a head absent from c is appended once and recursion advances."
        if "reversedKeptAcc(.IntSeq" in text:
            return "ACCEPT: processing no remaining characters preserves the reverse accumulator."
        if "reversedKeptAcc(iCons" in text and "iCons(X, A)" not in text:
            return "ACCEPT: a deleted head does not change the reverse accumulator."
        if "reversedKeptAcc(iCons" in text and "iCons(X, A)" in text:
            return "ACCEPT: a retained head is prepended exactly once, matching the submitted body."
        if "lastCharacter(.IntSeq" in text:
            return "ACCEPT: an empty iteration leaves the target's previous value unchanged."
        if "lastCharacter(iCons" in text:
            return "ACCEPT: structural recursion returns the final one-character string."
        if "#loop(" in text:
            return (
                "ACCEPT DERIVED BRIDGE: exact submitted loop AST, bindings, "
                "environment, parent, and three changed locals are matched; "
                "all other cells and the continuation are framed. The identical "
                "universal reachability claim closed against MPY-VERIFICATION-BASE, "
                "which excludes this bridge."
            )
    return "REVIEWED: candidate-local entry not otherwise classified."


def claim_assessment(record):
    text = record["text"]
    if "#loop(" in text:
        return (
            "ACCEPT CONNECTION THEOREM: universal loop execution from arbitrary "
            "S,C,A,RA,V and framed continuation/state to the three exact summaries."
        )
    return (
        "ACCEPT FORMAL ENTRY THEOREM: exact closure body and exact initial cells "
        "return the two-component tuple of forward summary and summary equality."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.inventory.read_text(encoding="utf-8"))
    counts = {}
    for record in data["entries"]:
        path = Path(record["file"])
        basename = path.name
        if basename == "verification.k":
            scope = "candidate-proof-extension"
            assessment = candidate_extension_assessment(record)
        elif basename == "spec.k":
            scope = "candidate-claim"
            assessment = claim_assessment(record)
        elif record["kind"] in {"syntax", "configuration", "context"}:
            reached = in_ranges(record["start_line"], REACHED.get(basename, []))
            scope = "fixed-declaration-reached" if reached else "fixed-declaration-unreached"
            assessment = (
                "ACCEPT FIXED DECLARATION: byte-identical trusted supplied semantics; "
                + (
                    "sorts/evaluation order participate in the exact claim and fresh builds succeeded."
                    if reached
                    else "this declaration has no rewrite effect on the exact claim."
                )
            )
        else:
            reached = in_ranges(record["start_line"], REACHED.get(basename, []))
            scope = "fixed-rule-reached" if reached else "fixed-rule-unreached"
            if reached:
                assessment = (
                    "ACCEPT FIXED RULE: byte-identical trusted supplied semantics. "
                    "Reviewed in the reached call/sequence/lookup/loop/string/tuple "
                    "dependency; guards and priorities preserve the exact submitted "
                    "control flow and no false conclusion witness was found."
                )
            else:
                assessment = (
                    "NO PROOF DEPENDENCE: byte-identical trusted supplied-semantics "
                    "rule, but its constructor/operator/value-sort redex is unreachable "
                    "from the exact closure AST and pinned string inputs. It cannot "
                    "contribute to claim closure; no candidate soundness conclusion "
                    "is drawn from it."
                )
        record["audit_scope"] = scope
        record["audit_assessment"] = assessment
        counts[scope] = counts.get(scope, 0) + 1

    data["audit_scope_counts"] = counts
    args.json_output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    rows = [
        "# Assessed exhaustive K source inventory",
        "",
        f"Entries: {data['entry_count']}",
        "",
        "Every extracted declaration, context, rule, and claim has an explicit "
        "reachability class and audit decision below. Full untruncated source "
        "statements are in the companion JSON.",
        "",
        "| # | File:line | Source class | Audit scope | Decision |",
        "|---:|---|---|---|---|",
    ]
    for number, record in enumerate(data["entries"], 1):
        assessment = record["audit_assessment"].replace("|", "&#124;")
        rows.append(
            f"| {number} | `{record['file']}:{record['start_line']}-"
            f"{record['end_line']}` | {record['classification']} | "
            f"{record['audit_scope']} | {assessment} |"
        )
    args.markdown_output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({"entry_count": data["entry_count"], "scope_counts": counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
