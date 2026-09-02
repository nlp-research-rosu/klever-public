#!/usr/bin/env python3
"""Attach an audit disposition to every sentence in the lexical inventory."""

from __future__ import annotations

import json
from pathlib import Path


SOURCE = Path("/audit-output/evidence/stage5/rule-inventory.json")
OUTPUT = Path("/audit-output/evidence/stage5/annotated-inventory.md")

# Fixed-semantics lines materially exercised by the submitted program/proof.
USED_FIXED_RANGES = {
    "reference-semantics/semantics.k": [(34, 90)],
    "reference-semantics/semantics/syntax.k": [(3, 62)],
    "reference-semantics/semantics/core.k": [
        (25, 60),
        (68, 70),
        (100, 111),
        (123, 127),
        (129, 181),
        (183, 225),
    ],
    "reference-semantics/semantics/list.k": [(8, 10)],
    "reference-semantics/semantics/tuple.k": [(30, 41)],
    "reference-semantics/semantics/controls.k": [
        (8, 31),
        (50, 85),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 20),
        (62, 90),
    ],
    "reference-semantics/semantics/call.k": [(18, 31), (69, 75)],
    "reference-semantics/semantics/operators.k": [(10, 20)],
    "reference-semantics/semantics/int.k": [(7, 28)],
    "reference-semantics/semantics/bool.k": [(8, 25)],
}

PROOF_RULES = {
    7: ("ACCEPT", "Map deletion normalization; exact for the explicit key plus disjoint rest."),
    10: ("ACCEPT", "Fresh-key Map update normalization; exact insertion."),
    18: ("ACCEPT", "Two fixed Name/#look steps in a non-cell frame."),
    24: ("ACCEPT", "Concrete Map-split form of the same non-cell Name lookup."),
    31: ("ACCEPT", "Guarded specialization of fixed Assign; identical state update."),
    40: ("ACCEPT", "Integer literal cooling only; no state or control effect."),
    43: ("ACCEPT", "Boolean literal cooling only; no state or control effect."),
    46: ("ACCEPT", "Existing-key normal form of the fixed Assign update."),
    55: ("ACCEPT", "Guarded fixed AugAssign for a non-reference local."),
    65: ("ACCEPT", "Map-split normal form of the same non-reference AugAssign."),
    75: ("ACCEPT", "Guarded specialization of fixed #bindTgt."),
    81: ("ACCEPT", "Existing-key normal form of fixed #bindTgt."),
    91: ("ACCEPT", "Side-effect-free left-to-right lookup of two distinct local Names."),
    103: ("ACCEPT", "Side-effect-free local Name plus integer literal comparison."),
    111: ("ACCEPT", "Side-effect-free Name lookup followed by fixed If truthiness."),
    119: ("ACCEPT", "Side-effect-free RHS Name lookup before fixed assignment."),
    127: ("ACCEPT", "Side-effect-free Name lookup before fixed Return control."),
    134: (
        "CONCERN",
        "Exact for the theorem's unboxed list value, but over-broad for ref-valued locals; "
        "the fixed semantics dereferences a ref before #loop while this rule can leave #loop(ref,...).",
    ),
    142: ("ACCEPT", "Finite Call/Name/callee/argument normalization with the exact closure binding."),
    166: ("ACCEPT", "Finite local lookup, literal cooling, and integer >= comparison."),
    186: ("ACCEPT", "Empty symbolic IntList iterator case."),
    188: ("ACCEPT", "Nonempty symbolic IntList iterator case; exposes exactly one head."),
    195: ("ACCEPT", "trialPrime false-state base case."),
    196: ("ACCEPT", "trialPrime loop-exit case."),
    198: ("ACCEPT", "trialPrime divisible branch, disjoint from loop exit."),
    201: ("ACCEPT", "trialPrime non-divisible recursive branch; divisor increases."),
    209: ("ACCEPT", "trialDivisor false-state base case."),
    210: ("ACCEPT", "trialDivisor loop-exit case."),
    212: ("ACCEPT", "trialDivisor divisible iteration increments once before exit."),
    215: ("ACCEPT", "trialDivisor non-divisible recursion; divisor increases."),
    222: ("ACCEPT", "isPrime names trial division from 2 with n>=2 initialization."),
    225: ("ACCEPT", "largestPrime empty-list base case."),
    226: ("ACCEPT", "largestPrime update branch."),
    230: ("ACCEPT", "largestPrime keep-current branch; complementary to update."),
    237: ("ACCEPT", "digitAcc loop-exit case."),
    240: ("ACCEPT", "digitAcc decimal step; positive N strictly decreases."),
    248: ("ACCEPT", "digitSum initializes digitAcc at zero."),
    252: ("ACCEPT", "Macro equals the submitted primality-loop condition AST."),
    260: ("ACCEPT", "Macro equals the submitted primality-loop body AST."),
    269: ("ACCEPT", "Macro equals the submitted scan-loop body AST."),
    282: ("ACCEPT", "Macro equals the submitted digit-loop condition AST."),
    286: ("ACCEPT", "Macro equals the submitted digit-loop body AST."),
    294: ("ACCEPT", "Macro equals the complete submitted function body AST."),
    307: (
        "ACCEPT_WITH_EVIDENCE_GAP",
        "Exact bounded call/frame/bind/initialization/For-prefix composition on its complete "
        "match; the bridge-free machine proof was separately attempted and recorded.",
    ),
    342: ("ACCEPT", "Module macro KAST is byte-identical to parsed submitted solution.mpy KAST."),
}

CLAIMS = {
    7: ("ACCEPT", "Trial-division loop invariant; exact final prime/divisor state."),
    42: ("ACCEPT", "Digit loop invariant; exact final accumulator and zeroed largest."),
    73: ("ACCEPT", "List scan plus fixed suffix and frame pop; returns the result summary."),
    118: ("ACCEPT", "Function invocation theorem, dependent on the proved scan claim."),
    138: (
        "ACCEPT_WITH_INTENT_LIMIT",
        "End-to-end submitted-program execution to exact result summary; interpreting the "
        "summary as standard primality remains an informal mathematics bridge.",
    ),
}


def in_used_range(file: str, line: int) -> bool:
    return any(start <= line <= end for start, end in USED_FIXED_RANGES.get(file, []))


def disposition(record: dict) -> tuple[str, str]:
    file = record["file"]
    line = record["line"]
    text = record["text"]
    if file.startswith("reference-semantics/"):
        if record["kind"] == "syntax" and (
            "no-evaluators" in text
            or ("symbol(" in text and "[concrete]" not in text)
        ):
            return (
                "FIXED_OPAQUE_UNUSED",
                "Supplied fixed-semantics opaque/trusted primitive; unreachable from this integer-only program.",
            )
        if in_used_range(file, line):
            return (
                "FIXED_USED",
                "Selected supplied-semantics sentence in the reachable execution slice; checked against the mapped construct.",
            )
        return (
            "FIXED_UNUSED",
            "Selected supplied-semantics sentence; no syntax or proof term in this task reaches it.",
        )
    if file == "verification.k":
        if record["kind"] == "rule":
            return PROOF_RULES[line]
        if record["kind"] == "syntax":
            return (
                "ACCEPT_DECLARATION",
                "Proof-local constructor, total function, or exact AST macro declaration; its rules are separately inventoried.",
            )
        return ("STRUCTURE", "Proof module/import structure.")
    if file == "spec.k" and record["kind"] == "claim":
        return CLAIMS[line]
    if file == "spec.k":
        return ("STRUCTURE", "Specification module/import structure.")
    raise AssertionError((file, line, record["kind"]))


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = [
        "# Annotated exhaustive inventory",
        "",
        "Every lexical sentence from `rule-inventory.json` has an audit disposition.",
        "",
        "| # | File:line | Kind/tags | Disposition | Reason |",
        "|---:|---|---|---|---|",
    ]
    for index, record in enumerate(payload["records"], start=1):
        decision, reason = disposition(record)
        kind = record["kind"]
        if record["tags"]:
            kind += " (" + ", ".join(record["tags"]) + ")"
        escaped_reason = reason.replace("|", "\\|")
        rows.append(
            f"| {index} | `{record['file']}:{record['line']}` | {kind} | "
            f"{decision} | {escaped_reason} |"
        )
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"annotated_records={len(payload['records'])}")
    print(OUTPUT)


if __name__ == "__main__":
    main()
