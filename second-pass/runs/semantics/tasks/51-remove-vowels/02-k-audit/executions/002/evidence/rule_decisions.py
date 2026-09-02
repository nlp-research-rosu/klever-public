#!/usr/bin/env python3
"""Attach an explicit audit decision to every inventoried K declaration."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


inventory_path = Path("/audit-output/evidence/stage5-k-inventory.json")
output_path = Path("/audit-output/evidence/stage5-rule-decisions.json")
inventory = json.loads(inventory_path.read_text())

used_lines: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {
        9,
        32,
        37,
        41,
        56,
        57,
        60,
        61,
    },
    "reference-semantics/semantics/core.k": {
        13,
        14,
        15,
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
        125,
        126,
        127,
        130,
        131,
        132,
        145,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        199,
        200,
        208,
        209,
        210,
        213,
        214,
        215,
    },
    "reference-semantics/semantics/str.k": {
        8,
        9,
        13,
        14,
        15,
        16,
        20,
        21,
        22,
        24,
        29,
        30,
        32,
        33,
        34,
        35,
        37,
        38,
        39,
        40,
        48,
    },
    "reference-semantics/semantics/operators.k": {15, 16, 17},
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
    },
    "reference-semantics/semantics/functions.k": {
        8,
        14,
        63,
        64,
        78,
        80,
        85,
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "reference-semantics/semantics/tuple.k": {31, 32},
}

file_assessment = {
    "assert.k": "assertion and exception rules; unused by solution",
    "bool.k": "Boolean dispatch/short-circuit rules; only fixed Bool truth is reached indirectly",
    "builtins.k": "builtin registry operations and folds; unused by solution",
    "call.k": "uniform call routing; material closure-call rules preserve evaluation, binding, and frame state",
    "comprehension.k": "comprehension macros; unused by solution",
    "concrete.k": "LLVM-only deep equality/keyed sorting; absent from proof definition",
    "controls.k": "assignment, branch, and loop control; material rules follow the submitted control flow",
    "core.k": "configuration, scope, sequencing, lookup, and pure helpers; material rules preserve all modeled cells",
    "dict.k": "dictionary operations; unused by solution",
    "float.k": "fixed opaque/concrete float boundary; all float symbols unused by solution",
    "functions.k": "function binding, return, and frame lifecycle; material rules match the exact one-call execution",
    "int.k": "integer operator rules; only ordinary code equality is used inside proof summaries",
    "iter.k": "iterator protocol declaration used by the string loop",
    "list.k": "list operations; unused by solution",
    "methods.k": "string/list method operations; unused by solution",
    "operators.k": "operator evaluation/dispatch; material Compare path is left-to-right and structure-preserving",
    "range.k": "range operations; unused by solution",
    "set.k": "set operations; unused by solution",
    "sort.k": "fixed opaque sort boundary; unused by solution",
    "str.k": "string iteration, literals, concatenation, and membership; material rules match the code-sequence model",
    "subscript.k": "index/slice operations; unused by solution",
    "syntax.k": "AST declarations and strictness; material declarations enforce the required evaluation order",
    "tuple.k": "tuple operations plus target binding; only ordinary name-target binding is used",
}

decisions: list[dict[str, object]] = []
for entry in inventory["entries"]:
    filename = str(entry["file"])
    line = int(entry["start_line"])
    if filename == "verification.k":
        if line == 21:
            status = "SOUND_OPERATIONAL_BRIDGE"
            justification = (
                "Exact pure specialization of one-character strContains over "
                "the ten-code literal. A bridge-free exhaustive 21-case "
                "reachability proof covers every K Int, and the opposite "
                "interpretation mutation is rejected."
            )
        elif line in {25, 26, 27, 30, 36, 37}:
            status = "SOUND_DEFINITIONAL_SUMMARY"
            justification = (
                "Structural finite-sequence filter: constructor coverage is "
                "complete, guards are complementary, and recursion descends."
            )
        elif line in {6, 7, 11, 12, 40, 41, 46, 47, 53, 54}:
            status = "SOUND_DECLARATION_OR_MACRO"
            justification = (
                "Truthful constant/function or compile-time syntax macro; the "
                "program macro is mechanically identical to solution.mpy."
            )
        else:
            raise AssertionError(f"unclassified verification entry {entry['id']}")
    elif filename == "spec.k":
        status = "SOUND_REACHABILITY_CLAIM"
        justification = (
            "Freshly closes as part of the mutually circular four-claim proof "
            "group; its precondition has a ground witness and its postcondition "
            "tracks the exact result/state footprint."
        )
    else:
        base = Path(filename).name
        assert base in file_assessment
        is_used = line in used_lines.get(filename, set())
        if bool(entry["flags"]["opaque"]):
            status = "ACCEPT_FIXED_OPAQUE_UNUSED"
            justification = (
                "Immutable supplied-semantics primitive, explicitly opaque in "
                "the proof backend and unreachable from this submitted term."
            )
        elif is_used:
            status = "ACCEPT_FIXED_MATERIAL"
            justification = file_assessment[base]
        else:
            status = "ACCEPT_FIXED_UNUSED"
            justification = (
                file_assessment[base]
                + "; this declaration/rule has no reachable head symbol on "
                "the submitted program's execution path"
            )
    decisions.append(
        {
            "inventory_id": entry["id"],
            "keyword": entry["keyword"],
            "status": status,
            "justification": justification,
        }
    )

assert len(decisions) == len(inventory["entries"]) == 949
assert len({item["inventory_id"] for item in decisions}) == 949
status_counts = collections.Counter(item["status"] for item in decisions)
document = {
    "schema_version": 1,
    "inventory_sha256": hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
    "decision_count": len(decisions),
    "status_counts": dict(sorted(status_counts.items())),
    "decisions": decisions,
}
encoded = json.dumps(document, indent=2, sort_keys=True) + "\n"
output_path.write_text(encoded)
print(f"output={output_path}")
print(f"output_sha256={hashlib.sha256(encoded.encode()).hexdigest()}")
print(f"decision_count={len(decisions)}")
print(f"status_counts={dict(sorted(status_counts.items()))}")
