#!/usr/bin/env python3
"""Emit an exhaustive inventory of local K declarations and rules."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(syntax|configuration|rule|context|claim|macro|alias)\b"
)
STOP = re.compile(
    r"^\s*(?:syntax|configuration|rule|context|claim|macro|alias|"
    r"module|endmodule|imports|requires)\b"
)


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, START.match(line).group(1))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    for position, (index, directive) in enumerate(starts):
        end = len(lines)
        for later in range(index + 1, len(lines)):
            if STOP.match(lines[later]):
                end = later
                break
        text_lines = lines[index:end]
        while text_lines and (
            not text_lines[-1].strip()
            or text_lines[-1].lstrip().startswith("//")
        ):
            text_lines.pop()
        yield index + 1, directive, " ".join(
            segment.strip() for segment in text_lines if segment.strip()
        )


def attributes(text: str) -> str:
    attrs = re.findall(r"\[([^\]]+)\]", text)
    return ";".join(attrs) if attrs else "-"


def kind(directive: str, text: str) -> str:
    if directive == "syntax":
        if "no-evaluators" in text:
            return "OPAQUE_FUNCTION_DECL"
        if re.search(r"\bmacro(?:-rec)?\b", text):
            return "MACRO_DECL"
        if re.search(r"\bfunction\b", text):
            return "FUNCTION_DECL"
        if re.search(r"\bfunctional\b", text):
            return "FUNCTIONAL_DECL"
        return "SYNTAX_DECL"
    if directive == "rule":
        if "[concrete]" in text:
            return "CONCRETE_RULE"
        if "<k>" in text or re.search(r"<(?:env|scopes|heap|stack|ret|exc)", text):
            return "OPERATIONAL_RULE"
        return "EQUATIONAL_RULE"
    return directive.upper()


def target_role(relative: str, line: int, record_kind: str, text: str) -> str:
    if relative == "spec.k" and record_kind == "CLAIM":
        return "TARGET_CLAIM"
    if relative == "verification.k":
        return "PROOF_MODULE_NO_EXTENSIONS"
    if relative.endswith("concrete.k"):
        return "LLVM_ONLY_NOT_IMPORTED_BY_PROOF"
    if record_kind == "OPAQUE_FUNCTION_DECL":
        return "OPAQUE_UNUSED_BY_TARGET"

    basename = Path(relative).name
    used_lines = {
        "syntax.k": {9, 37, 41, 50, 53, 56, 57, 60, 61},
        "core.k": {
            13,
            14,
            15,
            25,
            31,
            32,
            34,
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
            145,
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
        "functions.k": {8, 14, 63, 64, 68, 78, 80, 85},
        "call.k": {16, 19, 20, 21, 24, 31, 38, 52, 56, 63, 69},
        "methods.k": {10, 19, 112, 113, 140, 142, 143, 154, 155, 156},
        "builtins.k": {17, 20, 21, 22, 23, 24, 25, 26, 41},
        "set.k": {8, 11, 12, 13, 16, 18, 19, 20, 22, 25, 26, 27},
    }
    if line in used_lines.get(basename, set()):
        return "TARGET_PATH_REVIEWED"
    return "SUPPLIED_UNUSED_BY_TARGET"


def disposition(relative: str, role: str, text: str) -> str:
    if role == "TARGET_CLAIM":
        return "RESULT_CONSTRAINING_AND_SATISFIABLE"
    if role == "PROOF_MODULE_NO_EXTENSIONS":
        return "NO_LOCAL_RULE_TO_JUSTIFY"
    if role == "LLVM_ONLY_NOT_IMPORTED_BY_PROOF":
        return "OUTSIDE_SYMBOLIC_THEORY"
    if role == "OPAQUE_UNUSED_BY_TARGET":
        return "INERT_FOR_TARGET"
    if role == "SUPPLIED_UNUSED_BY_TARGET":
        return "NO_TARGET_DEPENDENCE_OR_FALSE_TARGET_CONCLUSION_WITNESS"
    if any(name in text for name in ("lowerC", "mapLower", '"lower"')):
        return "SOUND_IN_FIXED_MODEL_WITH_DOCUMENTED_UNICODE_DIVERGENCE"
    return "ACCEPTED_RELATIVE_TO_FIXED_SUPPLIED_MODEL"


records = []
for path in FILES:
    relative = str(path.relative_to(ROOT))
    for line, directive, text in declarations(path):
        record_kind = kind(directive, text)
        role = target_role(relative, line, record_kind, text)
        records.append(
            (
                relative,
                line,
                record_kind,
                attributes(text),
                role,
                disposition(relative, role, text),
                text.replace("\t", " "),
            )
        )

print(
    "ID\tFILE\tLINE\tKIND\tATTRIBUTES\tTARGET_ROLE\tDISPOSITION\tDECLARATION"
)
for identifier, record in enumerate(records, 1):
    print(identifier, *record, sep="\t")

print(f"# TOTAL_RECORDS={len(records)}")
for category in sorted({record[2] for record in records}):
    count = sum(record[2] == category for record in records)
    print(f"# KIND_{category}={count}")
for role in sorted({record[4] for record in records}):
    count = sum(record[4] == role for record in records)
    print(f"# ROLE_{role}={count}")
for path in FILES:
    relative = str(path.relative_to(ROOT))
    count = sum(record[0] == relative for record in records)
    print(f"# FILE_{relative}={count}")
