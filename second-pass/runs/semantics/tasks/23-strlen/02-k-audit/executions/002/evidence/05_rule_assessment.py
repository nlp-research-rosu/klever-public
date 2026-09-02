#!/usr/bin/env python3
"""Attach a target-reachability and soundness disposition to every inventory row."""

from __future__ import annotations

import csv
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/05_rule_inventory.tsv")

# Declaration/rule starts in the exact fixed-semantics slice exercised by the
# target claim. A multi-alternative syntax declaration is represented by its
# first line, as in 05_rule_inventory.tsv.
REACHABLE: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {9, 41, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        13,
        15,
        25,
        36,
        37,
        38,
        39,
        40,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        213,
        214,
        215,
        227,
        228,
        229,
    },
    "reference-semantics/semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "reference-semantics/semantics/builtins.k": {17, 20, 21, 24},
    "reference-semantics/semantics/call.k": {19, 20, 21, 31, 69},
}

REASONS: dict[tuple[str, int], str] = {
    ("reference-semantics/semantics/core.k", 49): "initial cells match the claim pre-state",
    ("reference-semantics/semantics/core.k", 125): "loads the exact Module statement sequence",
    ("reference-semantics/semantics/core.k", 126): "sequences the function definition before the call",
    ("reference-semantics/semantics/core.k", 127): "eliminates the empty statement suffix",
    ("reference-semantics/semantics/core.k", 131): "starts lexical name lookup from current env",
    ("reference-semantics/semantics/core.k", 132): "returns the local strlen/string or builtin len binding",
    ("reference-semantics/semantics/core.k", 152): "falls through from the call frame to module/builtins",
    ("reference-semantics/semantics/core.k", 158): "defines the standard builtin len binding",
    ("reference-semantics/semantics/core.k", 189): "evaluates the sole argument left-to-right",
    ("reference-semantics/semantics/core.k", 190): "accumulates the evaluated string argument",
    ("reference-semantics/semantics/core.k", 191): "dispatches the completed argument list",
    ("reference-semantics/semantics/core.k", 214): "appends the sole argument",
    ("reference-semantics/semantics/core.k", 215): "structural append recursion (unused tail case but same helper)",
    ("reference-semantics/semantics/core.k", 228): "isLen empty base case is 0",
    ("reference-semantics/semantics/core.k", 229): "isLen counts one cons and recurses structurally",
    ("reference-semantics/semantics/functions.k", 14): "binds the submitted function body as a closure",
    ("reference-semantics/semantics/functions.k", 63): "finishes one-parameter binding",
    ("reference-semantics/semantics/functions.k", 64): "binds string to the supplied str value",
    ("reference-semantics/semantics/functions.k", 78): "returns the computed value and initiates frame pop",
    ("reference-semantics/semantics/functions.k", 85): "restores caller env/stack and removes the call frame",
    ("reference-semantics/semantics/builtins.k", 21): "routes the resolved len builtin to seqLen",
    ("reference-semantics/semantics/builtins.k", 24): "defines string len as structural IntSeq length",
    ("reference-semantics/semantics/call.k", 20): "evaluates the actual callee; no priority interceptor matches",
    ("reference-semantics/semantics/call.k", 21): "evaluates arguments after binding resolution",
    ("reference-semantics/semantics/call.k", 31): "dispatches builtinV(\"len\") without an oracle",
    ("reference-semantics/semantics/call.k", 69): "enters and executes the exact user closure body",
}

text = INVENTORY.read_text(encoding="utf-8")
records_text = text.split("RECORDS\n", 1)[1]
reader = csv.DictReader(records_text.splitlines(), delimiter="\t")

writer = csv.writer(__import__("sys").stdout, delimiter="\t", lineterminator="\n")
writer.writerow(
    [
        "file",
        "line",
        "kind",
        "attributes",
        "disposition",
        "assessment",
        "declaration",
    ]
)

for row in reader:
    path = row["file"]
    line = int(row["line"])
    attrs = row["attributes"]
    if path == "verification.k":
        if line == 7:
            disposition = "CANDIDATE-VALID-DEFINITIONAL-MACRO"
            assessment = "compile-time name for the mechanically identical submitted Module term"
        elif line == 8:
            disposition = "CANDIDATE-VALID-DEFINITIONAL-MACRO"
            assessment = "RHS is constructor-identical to regenerated solution.mpy"
        elif line == 18:
            disposition = "CANDIDATE-VALID-ENTRY-DECLARATION"
            assessment = "fresh entry symbol; carries no value equation"
        else:
            disposition = "CANDIDATE-VALID-EXECUTION-WRAPPER"
            assessment = "prepends exact module load and ordinary call while preserving continuation and all cells"
    elif path == "spec.k":
        disposition = "TARGET-CLAIM"
        assessment = "universal str(IntSeq) result is constrained to isLen of the same sequence"
    elif line in REACHABLE.get(path, set()):
        disposition = "FIXED-REACHABLE-VALID"
        assessment = REASONS.get(
            (path, line),
            "declaration/helper in the exact fixed-semantics execution slice; no opaque result",
        )
    elif "no-evaluators" in attrs:
        disposition = "FIXED-OPAQUE-UNREACHABLE"
        assessment = "supplied baseline opaque primitive; syntactically unreachable from this target claim"
    else:
        disposition = "FIXED-UNREACHABLE"
        assessment = "supplied baseline declaration/rule; its head cannot occur on the target execution slice"
    writer.writerow(
        [
            path,
            line,
            row["kind"],
            attrs,
            disposition,
            assessment,
            row["declaration"],
        ]
    )
