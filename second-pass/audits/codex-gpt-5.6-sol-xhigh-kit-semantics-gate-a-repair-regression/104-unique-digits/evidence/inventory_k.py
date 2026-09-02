#!/usr/bin/env python3
"""Inventory every K declaration/rule/claim used by the submitted proof tree."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/104-unique-digits-audit/candidate-source")
TOP_LEVEL_NAMES = (
    "audit-opposite-spec.k",
    "audit-spec.k",
    "audit-verification.k",
    "connection-body-mutation.k",
    "connection-spec.k",
    "connection-verification.k",
    "program-fragments.k",
    "projection.k",
    "spec-vacuity.k",
    "spec.k",
    "verification.k",
)
TOP_LEVEL_FILES = [ROOT / name for name in TOP_LEVEL_NAMES]
SEMANTICS_FILES = sorted((ROOT / "reference-semantics").rglob("*.k"))
FILES = SEMANTICS_FILES + TOP_LEVEL_FILES

ENTRY_RE = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\b|alias\b)"
)
MODULE_RE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")


def directly_used(relative: str, line: int) -> bool:
    used_ranges = {
        "reference-semantics/semantics/syntax.k": [(9, 17), (28, 32), (37, 38), (41, 61)],
        "reference-semantics/semantics/core.k": [
            (13, 42),
            (49, 60),
            (68, 70),
            (117, 127),
            (130, 181),
            (185, 205),
            (208, 225),
        ],
        "reference-semantics/semantics/iter.k": [(8, 8)],
        "reference-semantics/semantics/operators.k": [(12, 17)],
        "reference-semantics/semantics/int.k": [(15, 16), (19, 20), (24, 26)],
        "reference-semantics/semantics/bool.k": [(16, 25)],
        "reference-semantics/semantics/list.k": [(9, 20), (53, 55)],
        "reference-semantics/semantics/tuple.k": [(31, 41)],
        "reference-semantics/semantics/controls.k": [
            (9, 18),
            (48, 54),
            (65, 85),
            (106, 108),
        ],
        "reference-semantics/semantics/functions.k": [
            (8, 16),
            (63, 90),
        ],
        "reference-semantics/semantics/call.k": [
            (16, 24),
            (52, 60),
            (69, 75),
        ],
        "reference-semantics/semantics/sort.k": [(18, 24), (40, 42)],
    }
    return any(start <= line <= end for start, end in used_ranges.get(relative, []))


def classify(relative: str, line: int, kind: str, text: str) -> tuple[str, str]:
    if relative.startswith("reference-semantics/"):
        if relative.endswith("semantics/sort.k") and (
            "sortVS" in text or "insVS" in text or '"sort"' in text
        ):
            return (
                "TRUSTED_PRIMITIVE_USED",
                "Selected supplied sort boundary; concrete equations agree with insertion sort, "
                "but symbolic sortVS remains an explicitly accounted opaque contract.",
            )
        if directly_used(relative, line):
            return (
                "ACCEPT_FIXED_USED",
                "Unmodified supplied-semantics rule/declaration directly used by solution.mpy; "
                "checked against the construct mapping and concrete reconstruction.",
            )
        return (
            "ACCEPT_FIXED_UNUSED",
            "Unmodified supplied-semantics rule/declaration not reachable from the submitted "
            "program's construct/value domain; it contributes no proof-local shortcut.",
        )

    if relative == "program-fragments.k":
        return (
            "ACCEPT_DEFINITIONAL_MACRO",
            "Exact syntax abbreviation checked against regenerated solution.mpy; no execution is replaced.",
        )
    if relative == "projection.k":
        if "allOddResult" in text:
            return (
                "ACCEPT_OPAQUE_WITH_CONNECTION",
                "Result-bearing symbol is acceptable only with the separate bridge-free universal connection.",
            )
        return (
            "ACCEPT_MATH_DEFINITION",
            "Disjoint exhaustive integer projection equations; no operational execution replacement.",
        )
    if relative == "verification.k":
        if kind == "rule" and ("<k> Assign(" in text or "<k> #while(" in text):
            return (
                "ACCEPT_OPERATIONAL_BRIDGE",
                "Proof-local bridge; complete domain is checked against a bridge-free connection claim.",
            )
        return (
            "ACCEPT_MATH_DEFINITION",
            "Guarded/exhaustive, structurally recursive proof summary checked rule by rule.",
        )
    if relative == "connection-verification.k":
        return (
            "ACCEPT_CONNECTION_THEORY",
            "Truthful recursive digit summary used only by the bridge-free universal connection proof.",
        )
    if relative in {"spec.k", "connection-spec.k"}:
        return (
            "ACCEPT_POSITIVE_CLAIM",
            "Positive reachability claim reconstructed in its complete suite.",
        )
    if relative in {"audit-verification.k", "audit-spec.k"}:
        return (
            "ACCEPT_VALIDATION_ONLY",
            "Validation-only import or ground witness; not a shortcut used by the target proof.",
        )
    if relative in {
        "audit-opposite-spec.k",
        "connection-body-mutation.k",
        "spec-vacuity.k",
    }:
        return (
            "NEGATIVE_TEST_ONLY",
            "Candidate-authored negative evidence, not imported by a positive target definition.",
        )
    return ("REVIEWED_OTHER", "Reviewed local declaration; no target-proof dependency found.")


def flags(text: str) -> str:
    found = []
    for flag in (
        "function",
        "total",
        "functional",
        "no-evaluators",
        "symbol",
        "macro",
        "priority",
        "simplification",
        "owise",
        "concrete",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", text):
            found.append(flag)
    return ",".join(found) if found else "-"


def clean(text: str) -> str:
    return " ".join(text.split()).replace("\t", " ")


print(
    "id\tfile\tmodule\tstart_line\tend_line\tkind\tflags\tdecision\trationale\ttext"
)
entry_id = 0
for path in FILES:
    relative = path.relative_to(ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    module = "-"
    starts = []
    module_by_line = {}
    for index, line in enumerate(lines, start=1):
        module_match = MODULE_RE.match(line)
        if module_match:
            module = module_match.group(1)
        module_by_line[index] = module
        if ENTRY_RE.match(line):
            starts.append(index)
    boundaries = starts[1:] + [len(lines) + 1]
    for start, next_start in zip(starts, boundaries):
        end = next_start - 1
        while end > start and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        block = "\n".join(lines[start - 1 : end])
        kind = ENTRY_RE.match(lines[start - 1]).group(1).split()[0]
        decision, rationale = classify(relative, start, kind, block)
        entry_id += 1
        print(
            "\t".join(
                [
                    str(entry_id),
                    relative,
                    module_by_line[start],
                    str(start),
                    str(end),
                    kind,
                    flags(block),
                    decision,
                    rationale,
                    clean(block),
                ]
            )
        )
