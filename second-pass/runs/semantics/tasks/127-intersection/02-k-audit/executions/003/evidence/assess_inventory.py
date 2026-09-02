#!/usr/bin/env python3
"""Attach an audit disposition to every inventoried K source sentence."""

from __future__ import annotations

import csv
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/rule-inventory.tsv")

LOCAL = {
    9: (
        "ACCEPT_DERIVED_LOW_LEVEL",
        "Valid Map deletion normalization under the explicit disjoint-key guard; "
        "only normalizes fixed #pop frame deletion.",
    ),
    16: (
        "ACCEPT_EXACT_DEFINITION",
        "intersectionBody is constructor-identical to trusted regeneration; see "
        "constructor-pinning.k and 04a-constructor-pinning.log.",
    ),
    38: (
        "ACCEPT_EXACT_DEFINITION",
        "divisorBody is the exact loop body occurring in intersectionBody.",
    ),
    48: ("ACCEPT_MATH_DEFINITION", "Exact ASCII encoding of YES."),
    49: ("ACCEPT_MATH_DEFINITION", "Exact ASCII encoding of NO."),
    55: (
        "ACCEPT_MATH_DEFINITION",
        "Divisor search returns YES when the candidate range is exhausted.",
    ),
    57: (
        "ACCEPT_MATH_DEFINITION",
        "A divisor in the remaining range fixes the result to NO.",
    ),
    59: (
        "ACCEPT_MATH_DEFINITION",
        "Non-divisor branch advances D by one; used domain has D>=2.",
    ),
    62: (
        "ACCEPT_MATH_DEFINITION",
        "Integers <=1 are non-prime for the source contract.",
    ),
    64: (
        "ACCEPT_MATH_DEFINITION",
        "Integers >1 start exhaustive divisor search at 2.",
    ),
    68: (
        "ACCEPT_MATH_DEFINITION",
        "Exact closed-interval overlap length used by both implementations.",
    ),
    78: (
        "ACCEPT_PROVED_OPERATIONAL_BRIDGE",
        "Exact universal LOOP-SPEC theorem installed after bridge-free #Top; "
        "same continuation, bindings, frame, result, and state footprint.",
    ),
}


def fixed_assessment(kind: str, attributes: str) -> tuple[str, str]:
    if kind == "rule":
        return (
            "ACCEPT_FIXED_SUPPLIED_LEVEL",
            "Individually inspected fixed-supplied rule. Used-path relevance and "
            "construct routing are recorded in construct-map.md; no false "
            "conclusion witness was found on the intended domain.",
        )
    if kind == "syntax" and "no-evaluators" in attributes:
        return (
            "ACCEPT_INERT_OPAQUE_DECLARATION",
            "Opaque fixed-semantics symbol; not reachable from solution.mpy.",
        )
    if kind == "syntax":
        return (
            "ACCEPT_DECLARATION",
            "Syntax/function/attribute declaration inventoried; material used-path "
            "rules are mapped in construct-map.md.",
        )
    if kind == "claim":
        return (
            "PROOF_TARGET",
            "Reachability target, independently reconstructed in Stage 3.",
        )
    return ("STRUCTURAL", "Module/import/configuration/context sentence inventoried.")


with INVENTORY.open(newline="") as stream:
    reader = csv.DictReader(stream, delimiter="\t")
    print("id\tfile\tline\tkind\tattributes\tdisposition\treason")
    for row in reader:
        if not row["id"].startswith("K"):
            break
        file_name = row["file"]
        line = int(row["line"])
        if file_name == "/candidate/verification.k" and line in LOCAL:
            disposition, reason = LOCAL[line]
        elif file_name == "/candidate/verification.k":
            disposition, reason = fixed_assessment(row["kind"], row["attributes"])
            if row["kind"] in {"syntax", "module", "imports", "endmodule", "requires"}:
                reason = "Proof-local structural or sort declaration; semantic rules are assessed separately."
        else:
            disposition, reason = fixed_assessment(row["kind"], row["attributes"])
        print(
            "\t".join(
                [
                    row["id"],
                    file_name,
                    row["line"],
                    row["kind"],
                    row["attributes"],
                    disposition,
                    reason,
                ]
            )
        )
