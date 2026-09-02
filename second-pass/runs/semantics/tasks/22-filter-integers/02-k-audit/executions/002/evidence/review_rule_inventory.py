#!/usr/bin/env python3
"""Attach target-specific audit dispositions to every inventory sentence."""

from __future__ import annotations

import csv
from pathlib import Path


inventory = Path("/audit-output/evidence/rule-inventory.tsv")

# Sentences that are on the actual FILTER-PROGRAM execution path for at least
# one positive claim. Line numbers are sentence start lines in the source.
used = {
    "reference-semantics/semantics/core.k": {
        49, 117, 118, 124, 125, 126, 127, 130, 131, 132, 152, 157, 158,
        185, 186, 189, 190, 191, 199, 200, 213, 214, 217, 218,
    },
    "reference-semantics/semantics/str.k": {13, 14, 15, 16},
    "reference-semantics/semantics/list.k": {
        9, 10, 13, 14, 15, 18, 19, 20, 53,
    },
    "reference-semantics/semantics/tuple.k": {31, 32},
    "reference-semantics/semantics/controls.k": {
        9, 35, 36, 48, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85,
    },
    "reference-semantics/semantics/functions.k": {
        8, 14, 63, 64, 78, 85,
    },
    "reference-semantics/semantics/call.k": {
        16, 19, 20, 21, 31, 52, 53, 69,
    },
    "reference-semantics/semantics/builtins.k": {
        17, 291, 293, 294, 295,
    },
}

with inventory.open(newline="") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))

writer = csv.writer(__import__("sys").stdout, delimiter="\t", lineterminator="\n")
writer.writerow(
    ["file", "line", "kind", "attributes", "disposition", "rationale", "text"]
)

for row in rows:
    file = row["file"]
    line = int(row["line"])
    kind = row["kind"]
    attrs = row["attributes"]

    if file == "reference-semantics/semantics/builtins.k" and line == 295:
        disposition = "UNSOUND_ON_INTENDED_DOMAIN_AND_USED"
        rationale = (
            "For the satisfiable Bool witness false, owise concludes isIntV(false)=false; "
            "CPython and trusted canonical conclude isinstance(False,int)=True, changing "
            "filter_integers([False]) from [False] to []."
        )
    elif file == "reference-semantics/semantics/builtins.k" and line in {291, 293}:
        disposition = "USED_MODEL_GAP_DEPENDENCY"
        rationale = (
            "Routes isinstance(...,int) through isIntV; structurally faithful, but its "
            "observable result inherits the Bool-subclass defect at line 295."
        )
    elif file == "reference-semantics/semantics/builtins.k" and line == 294:
        disposition = "USED_SOUND_FOR_DIRECT_INT_VALUES"
        rationale = "Direct K Int values are correctly classified as Python ints."
    elif file == "verification.k":
        disposition = "EXACT_PROGRAM_MACRO_OR_STRUCTURE"
        rationale = (
            "Only syntax macros/import structure; no semantic/proof rewrite. Independent "
            "macro expansion matched trusted-regenerated solution.mpy byte-for-byte as JSON KAST."
        )
    elif file == "spec.k" and kind == "claim":
        disposition = "SOUND_FIXED_SHAPE_BUT_MATERIALLY_LIMITED"
        rationale = (
            "Result-constraining finite-shape entry claim; no arbitrary-length/heterogeneous "
            "ValSeq theorem."
        )
        if line == 90:
            rationale += " This Bool-shaped claim additionally inherits the isIntV model gap."
    elif line in used.get(file, set()):
        disposition = "USED_SOUND_ON_REPRESENTED_NONBOOL_CASES"
        rationale = (
            "Matches the submitted control/data path and preserves relevant cells; no false "
            "conclusion witness found apart from the separately identified Bool type-test rule."
        )
    elif "no-evaluators" in attrs:
        disposition = "OPAQUE_TRUST_BOUNDARY_INERT_FOR_TARGET"
        rationale = (
            "Opaque proof-domain primitive, but the submitted program and all target claims "
            "neither invoke it nor mention its result."
        )
    elif "concrete" in attrs:
        disposition = "CONCRETE_ONLY_INERT_FOR_SYMBOLIC_TARGET"
        rationale = (
            "Concrete evaluator rule excluded from the MPY proof module or inactive on the "
            "target path; no target conclusion depends on it."
        )
    elif kind.startswith("rule"):
        disposition = "OUT_OF_TARGET_PATH_NO_FALSE_WITNESS"
        rationale = (
            "Reviewed for overlaps/guards/priority; not reachable from FILTER-PROGRAM on any "
            "submitted entry shape, and no concrete or symbolic false-conclusion witness was found."
        )
    elif kind.startswith("syntax") or kind in {
        "configuration", "context", "module", "endmodule", "import", "requires"
    }:
        disposition = "STRUCTURAL_DECLARATION"
        rationale = "Declaration/import/evaluation-context structure; not a correctness axiom."
    else:
        disposition = "STRUCTURAL"
        rationale = "Non-rule structure."

    writer.writerow(
        [file, line, kind, attrs, disposition, rationale, row["text"]]
    )
