#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventoried K construct."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/28-concatenate")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
STARTERS = (
    "requires ",
    "module ",
    "imports ",
    "configuration",
    "syntax ",
    "context ",
    "rule ",
    "claim",
    "endmodule",
)

# These are the supplied-semantics constructs actually traversed by the
# submitted program/claims. Other supplied rules are sort/name-disjoint and
# are never reached on the three claims' well-typed paths.
USED_RULES = {
    "reference-semantics/semantics/core.k": {
        118, 125, 126, 127, 131, 132, 152, 158, 189, 190, 191, 214, 215, 218, 219
    },
    "reference-semantics/semantics/call.k": {20, 21, 69},
    "reference-semantics/semantics/controls.k": {9, 20, 36, 69, 71, 72, 73, 106},
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 85},
    "reference-semantics/semantics/list.k": {9, 10, 14, 15},
    "reference-semantics/semantics/str.k": {14, 15, 16, 21, 22, 24},
    "reference-semantics/semantics/tuple.k": {32},
}

PROOF_LOCAL = {
    ("verification.k", 7): (
        "ACCEPTED_DECLARATION",
        "Total Boolean string-shape predicate; str and owise equations cover Val.",
    ),
    ("verification.k", 8): (
        "SOUND",
        "Returns true exactly for a str value.",
    ),
    ("verification.k", 9): (
        "SOUND",
        "Owise complement returns false for non-str Val constructors.",
    ),
    ("verification.k", 11): (
        "ACCEPTED_DECLARATION",
        "Total structural fold over the two ValSeq constructors.",
    ),
    ("verification.k", 12): ("SOUND", "Empty sequence contains only strings."),
    ("verification.k", 13): (
        "SOUND",
        "Structural conjunction exactly characterizes all-string sequences.",
    ),
    ("verification.k", 19): (
        "COVERAGE_GAP_OUTSIDE_USE",
        "Declared total on Val but has an equation only for str; every proof-side use is guarded by allStringValues/isStringValue.",
    ),
    ("verification.k", 20): (
        "SOUND_ON_USED_DOMAIN",
        "Projection of str(S) is S; no equation fixes non-string values.",
    ),
    ("verification.k", 21): (
        "CONNECTION_EVIDENCE_GAP",
        "Agrees with fixed str/str addition after V=str(S), but the fresh complete-guard bridge-free theorem did not close.",
    ),
    ("verification.k", 26): (
        "ACCEPTED_DECLARATION",
        "Structural accumulator fold; used only with all-string ValSeq.",
    ),
    ("verification.k", 27): ("SOUND", "Empty fold returns the accumulator."),
    ("verification.k", 28): (
        "SOUND_ON_USED_DOMAIN",
        "Cons fold appends the head codes then descends; allStringValues supplies the string domain.",
    ),
    ("verification.k", 31): (
        "ACCEPTED_DECLARATION",
        "Total structural fold returning old value for empty and last value otherwise.",
    ),
    ("verification.k", 32): ("SOUND", "No iteration preserves the old loop target."),
    ("verification.k", 33): ("SOUND", "Nonempty iteration leaves the final element in the target."),
    ("verification.k", 38): ("EXACT_ALIAS", "Zero-argument syntax alias for the submitted loop body."),
    ("verification.k", 39): ("SOUND_PROGRAM_PIN", "Expands byte-identically to solution.mpy loop body."),
    ("verification.k", 42): ("EXACT_ALIAS", "Zero-argument syntax alias for the submitted function body."),
    ("verification.k", 43): ("SOUND_PROGRAM_PIN", "Expands to the exact submitted assignment/loop/return sequence."),
    ("verification.k", 50): ("EXACT_ALIAS", "Zero-argument syntax alias for the translated module."),
    ("verification.k", 51): ("SOUND_PROGRAM_PIN", "Expands to the exact submitted Module term."),
    ("spec.k", 7): (
        "SOUND_HELPER_NOT_UNIVERSAL_ENTRY",
        "Result-constraining loop theorem, but it begins after call, binding, initialization, and iterable dereference.",
    ),
    ("spec.k", 36): (
        "SOUND_CONCRETE_ENTRY_ONLY",
        "Executes exact module for [] and proves the empty result.",
    ),
    ("spec.k", 58): (
        "SOUND_CONCRETE_ENTRY_ONLY",
        "Executes exact module for ['a','b','c'] and proves 'abc'.",
    ),
}


def is_start(line: str) -> bool:
    stripped = line.strip()
    return line.startswith(("module ", "requires ")) or (
        line.startswith("  ") and not line.startswith("    ") and stripped.startswith(STARTERS)
    )


def kind(text: str) -> str:
    first = text.lstrip()
    for candidate in (
        "requires",
        "module",
        "imports",
        "configuration",
        "syntax",
        "context",
        "rule",
        "claim",
        "endmodule",
    ):
        if first.startswith(candidate):
            return candidate
    return "other"


with Path("/audit-output/evidence/stage5/construct_assessment.csv").open(
    "w", newline=""
) as output:
    writer = csv.writer(output)
    writer.writerow(["source", "line", "kind", "decision", "notes", "first_line"])
    for path in FILES:
        relative = str(path.relative_to(ROOT))
        lines = path.read_text().splitlines()
        starts = [index for index, line in enumerate(lines) if is_start(line)]
        for position, start in enumerate(starts):
            stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
            block = "\n".join(lines[start:stop])
            record_kind = kind(block)
            key = (relative, start + 1)
            first_line = re.sub(r"\s+", " ", lines[start].strip())
            if key in PROOF_LOCAL:
                decision, notes = PROOF_LOCAL[key]
            elif relative.startswith("reference-semantics/"):
                if record_kind == "rule" and start + 1 in USED_RULES.get(relative, set()):
                    decision = "TRUSTED_SUPPLIED_USED"
                    notes = "Selected fixed semantics; reviewed in the real-program execution route."
                elif record_kind in {"syntax", "configuration", "context"}:
                    decision = "TRUSTED_SUPPLIED_DECLARATION"
                    notes = "Unmodified selected semantics; exact text is in rule_inventory.txt."
                else:
                    decision = "TRUSTED_SUPPLIED_NOT_REACHED"
                    notes = "Unmodified selected semantics and not matched on the submitted claims' typed execution paths."
            else:
                decision = "STRUCTURAL"
                notes = "Module/import/terminator structure; no independent execution conclusion."
            writer.writerow([relative, start + 1, record_kind, decision, notes, first_line])
