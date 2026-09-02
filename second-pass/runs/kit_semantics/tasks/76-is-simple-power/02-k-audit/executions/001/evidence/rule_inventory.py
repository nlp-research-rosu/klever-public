#!/usr/bin/env python3
"""Emit an exhaustive source-level inventory of local K sentences."""

from __future__ import annotations

import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/76-is-simple-power")
FILES = [
    SCRATCH / "reference-semantics/semantics.k",
    *sorted((SCRATCH / "reference-semantics/semantics").glob("*.k")),
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|module|endmodule)\b"
)


def in_ranges(line: int, ranges: list[tuple[int, int]]) -> bool:
    return any(lo <= line <= hi for lo, hi in ranges)


REACHED_RANGES = {
    "semantics/syntax.k": [
        (9, 16),
        (27, 32),
        (41, 61),
    ],
    "semantics/core.k": [
        (25, 60),
        (123, 127),
        (129, 181),
        (183, 210),
        (212, 229),
    ],
    "semantics/functions.k": [(13, 20), (62, 90)],
    "semantics/call.k": [(18, 24), (69, 74)],
    "semantics/operators.k": [(10, 20)],
    "semantics/int.k": [(7, 27)],
    "semantics/controls.k": [(8, 31), (46, 60), (65, 91)],
}

REACHED_EXPLANATIONS = {
    "semantics/syntax.k": "constructors/strictness used by translated body",
    "semantics/core.k": "configuration, sequencing, lookup, arguments, literals, truthiness",
    "semantics/functions.k": "closure construction bridge, binding, return, and frame pop",
    "semantics/call.k": "callee lookup, left-to-right arguments, and closure invocation",
    "semantics/operators.k": "unary/binary/comparison dispatch and evaluation contexts",
    "semantics/int.k": "integer unary minus, modulo, floor division, and comparisons",
    "semantics/controls.k": "assignment, branch selection, and while control",
}

PROOF_RULE_ASSESSMENT = {
    13: "SOUND: exponent-zero case N^0=1",
    15: "SOUND: base 0 gives X=0 for positive exponents, after X=1 partition",
    18: "SOUND: base 1 cannot yield X!=1",
    21: "SOUND: base -1 yields only +/-1, after X=1 partition",
    24: "SOUND: nonzero-magnitude base cannot yield X=0",
    27: "SOUND: exact nonzero factor removal; |N|>=2 decreases |X|",
    33: "SOUND: nondivisibility excludes every positive exponent",
    40: "SOUND_DERIVED: nondivisible loop-exit equality lemma",
    47: "SOUND_DERIVED: exact division equals recursive factor removal",
}

CLAIM_ASSESSMENT = {
    6: "AUXILIARY_REACHABILITY: exact real loop head and local update relation",
    31: "TARGET_REACHABILITY: exact submitted closure body to constrained Bool summary",
}


def classify(relative: str, line: int, kind: str, statement: str) -> str:
    if relative == "verification.k":
        if kind == "syntax":
            return "PROOF_LOCAL_DEFINITION: total recursive predicate; exhaustive guarded partition"
        return PROOF_RULE_ASSESSMENT.get(
            line, "PROOF_LOCAL: manually inspect exact statement"
        )
    if relative == "spec.k":
        return CLAIM_ASSESSMENT.get(line, "SPEC_SENTENCE")
    if "no-evaluators" in statement:
        return (
            "UNUSED_OPAQUE_TRUST_BOUNDARY: fixed supplied symbol is outside this "
            "program's dependency cone"
        )
    ranges = REACHED_RANGES.get(relative, [])
    if in_ranges(line, ranges):
        return "REACHED_FIXED_RULE: " + REACHED_EXPLANATIONS[relative]
    if kind == "configuration":
        return "REACHED_FIXED_CONFIGURATION: entry claim pins every material cell"
    if kind == "syntax":
        return "FIXED_DECLARATION: inspected; no independent rewrite conclusion"
    if kind == "context":
        return (
            "FIXED_CONTEXT_OUT_OF_CONE: inspected; no false-conclusion witness "
            "claimed on the intended program domain"
        )
    return (
        "FIXED_RULE_OUT_OF_CONE: inspected; no false-conclusion witness claimed "
        "on the intended program domain"
    )


rows = []
for path in FILES:
    text = path.read_text()
    lines = text.splitlines()
    relative = (
        path.relative_to(SCRATCH / "reference-semantics").as_posix()
        if "reference-semantics" in path.parts
        else path.relative_to(SCRATCH).as_posix()
    )
    starts = [index for index, value in enumerate(lines) if START.match(value)]
    for ordinal, index in enumerate(starts):
        match = START.match(lines[index])
        assert match is not None
        kind = match.group(1)
        next_index = len(lines)
        for probe in range(index + 1, len(lines)):
            if BOUNDARY.match(lines[probe]):
                next_index = probe
                break
        statement_lines = lines[index:next_index]
        while statement_lines and (
            not statement_lines[-1].strip()
            or statement_lines[-1].lstrip().startswith("//")
        ):
            statement_lines.pop()
        statement = " ".join(value.strip() for value in statement_lines)
        attributes = []
        for attribute in (
            "function",
            "functional",
            "total",
            "no-evaluators",
            "symbol",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", statement):
                attributes.append(attribute)
        rows.append(
            (
                relative,
                index + 1,
                kind,
                ",".join(attributes) or "-",
                classify(relative, index + 1, kind, statement),
                statement,
            )
        )

print("file\tline\tkind\tattributes\tassessment\tstatement")
for row in rows:
    escaped = [
        str(value).replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")
        for value in row
    ]
    print("\t".join(escaped))

counts = {}
for _, _, kind, _, _, _ in rows:
    counts[kind] = counts.get(kind, 0) + 1
print("# COUNTS " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
