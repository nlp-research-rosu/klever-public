#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
SOURCES = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
SOURCES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(
    r"^\s*(syntax|configuration|rule|context|claim|alias)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")

# Source declarations/rules that participate directly in this submitted
# program's parse, execution, loop proof, or result. Other supplied rules are
# still inventoried and inspected, but cannot match this program's reachable
# terms.
USED_STARTS: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 33, 34, 35, 36, 37, 38, 39, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13, 14, 15, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        68, 69, 70, 75, 95, 96, 97, 98, 100, 101, 102,
        117, 118, 124, 125, 126, 127, 130, 131, 132,
        157, 158, 185, 186, 189, 190, 191, 194, 195,
        199, 200, 208, 209, 210, 213, 214, 215, 217, 218, 219,
    },
    "semantics/iter.k": {8},
    "semantics/operators.k": {10, 12, 15, 16, 17},
    "semantics/int.k": {9, 13, 24, 26},
    "semantics/str.k": {8, 9, 13, 14, 15, 16, 20, 21, 22, 25},
    "semantics/list.k": {13, 14, 15, 18, 19, 20, 53},
    "semantics/tuple.k": {31, 32},
    "semantics/controls.k": {
        9, 20, 35, 36, 48, 51, 52, 53, 54, 65, 69, 71, 72, 73,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/call.k": {16, 19, 20, 21, 24, 52, 53, 69},
    "verification.k": {
        7, 8, 21, 22, 28, 29, 37, 38, 46, 47, 48, 50, 52,
        55, 56, 58, 59, 60, 62, 65, 66, 68, 71, 72, 74, 76,
        79, 80, 83, 84, 85, 87, 90, 91, 93, 95, 98, 99,
        103, 104, 105, 107, 108, 112, 115, 116, 121, 122,
        123, 125, 127, 129, 132, 133, 135, 136,
    },
    "spec.k": {8, 27},
}


def relative(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return path.relative_to(ROOT).as_posix()
    return path.name


def classify(path_name: str, line: int, kind: str, text: str, attrs: str) -> tuple[str, str]:
    used = line in USED_STARTS.get(path_name, set())
    if path_name == "verification.k":
        if kind == "syntax":
            return "proof-function-declaration", "ACCEPTED_PROOF_DEFINITION"
        if kind == "rule":
            return "proof-definitional-equation", "ACCEPTED_PROOF_DEFINITION"
    if path_name == "spec.k" and kind == "claim":
        label = "loop-circularity" if "scan-loop" in text else "entry-theorem"
        return label, "ACCEPTED_MACHINE_CLOSED_CLAIM"
    if "no-evaluators" in attrs:
        return "supplied-opaque-symbol", "FIXED_OPAQUE_UNUSED_BY_PROGRAM"
    if path_name == "semantics/concrete.k":
        return "supplied-concrete-only", "FIXED_CONCRETE_UNUSED_BY_PROOF"
    if kind == "syntax":
        role = "supplied-syntax"
    elif kind == "configuration":
        role = "supplied-configuration"
    elif kind == "context":
        role = "supplied-evaluation-context"
    elif kind == "rule" and "<k>" in text:
        role = "supplied-operational-rule"
    elif kind == "rule":
        role = "supplied-equation"
    else:
        role = f"supplied-{kind}"
    decision = (
        "FIXED_USED_REVIEWED_ACCEPT"
        if used
        else "FIXED_NONMATCHING_REVIEWED_ACCEPT"
    )
    return role, decision


print(
    "\t".join(
        [
            "id",
            "file",
            "line",
            "kind",
            "attributes",
            "role",
            "review_decision",
            "normalized_declaration",
        ]
    )
)

entry_id = 0
for source in SOURCES:
    lines = source.read_text().splitlines()
    starts = [
        (index + 1, START.match(line).group(1))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    for position, (line_no, kind) in enumerate(starts):
        next_line = starts[position + 1][0] if position + 1 < len(starts) else len(lines) + 1
        block_lines = lines[line_no - 1 : next_line - 1]
        # Do not absorb a module terminator or a new module into the preceding
        # declaration's display text.
        display_lines = []
        for line in block_lines:
            if line.strip() in {"endmodule"} or line.lstrip().startswith("module "):
                break
            display_lines.append(line.strip())
        text = " ".join(part for part in display_lines if part)
        attrs = ",".join(ATTR.findall(text))
        path_name = relative(source)
        role, decision = classify(path_name, line_no, kind, text, attrs)
        entry_id += 1
        safe_text = text.replace("\t", " ")
        print(
            "\t".join(
                [
                    str(entry_id),
                    path_name,
                    str(line_no),
                    kind,
                    attrs,
                    role,
                    decision,
                    safe_text,
                ]
            )
        )
