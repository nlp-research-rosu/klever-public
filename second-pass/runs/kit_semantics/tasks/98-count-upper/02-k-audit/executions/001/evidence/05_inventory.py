#!/usr/bin/env python3
"""Emit a complete declaration/rule inventory for the mounted K sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate")

# Rule/declaration start lines on the real target's load or entry-proof path.
# The review explains each dependency and treats strictness/context productions
# as compiler-generated evaluation rules.
USED: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 38, 39, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13,
        15,
        25,
        31,
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
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        199,
        203,
        208,
        209,
        210,
        213,
        214,
        215,
        227,
        228,
        229,
    },
    "semantics/operators.k": {15, 16, 17},
    "semantics/int.k": {11},
    "semantics/str.k": {
        13,
        14,
        15,
        16,
        29,
        32,
        33,
        34,
        35,
        37,
        38,
        39,
        40,
    },
    "semantics/subscript.k": {
        16,
        17,
        18,
        27,
        28,
        35,
        37,
        40,
        44,
        49,
        50,
        51,
        52,
        54,
        55,
        56,
        61,
        63,
        68,
        72,
        73,
        76,
        81,
        83,
        84,
        90,
        93,
        102,
        103,
        105,
        116,
        117,
        120,
    },
    "semantics/controls.k": {9, 20, 77, 78, 79, 81, 85},
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/call.k": {19, 20, 21, 69},
}

START = re.compile(
    r"^\s*(requires|module|imports|configuration|syntax|context(?:\s+alias)?|"
    r"rule|claim|endmodule)\b"
)


def strip_line_comment(line: str) -> str:
    in_string = False
    escaped = False
    for index in range(len(line) - 1):
        char = line[index]
        if escaped:
            escaped = False
        elif char == "\\" and in_string:
            escaped = True
        elif char == '"':
            in_string = not in_string
        elif not in_string and line[index : index + 2] == "//":
            return line[:index]
    return line


def blocks(path: Path) -> list[tuple[int, int, str, str]]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    lines = [strip_line_comment(line).rstrip() for line in raw_lines]
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            # Only column-zero `requires` is an import declaration. Indented
            # `requires` clauses belong to the preceding rule/claim.
            if match.group(1) == "requires" and line != line.lstrip():
                continue
            starts.append((index, match.group(1)))
    found = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else len(lines)
        while end >= start and not lines[end - 1].strip():
            end -= 1
        text = " ".join(
            line.strip() for line in lines[start - 1 : end] if line.strip()
        )
        found.append((start, end, kind, text))
    return found


def flags(text: str) -> list[str]:
    ordered = [
        "function",
        "total",
        "functional",
        "simplification",
        "priority",
        "owise",
        "concrete",
        "symbol",
        "no-evaluators",
        "macro-rec",
        "macro",
        "strict",
        "seqstrict",
        "bracket",
    ]
    return [flag for flag in ordered if re.search(rf"\b{re.escape(flag)}\b", text)]


def disposition(relative: str, start: int, kind: str, text: str) -> str:
    if relative == "verification.k":
        if kind == "rule":
            return "PROOF-LOCAL—review individually"
        return "PROOF-LOCAL declaration"
    if relative == "spec.k":
        return "TARGET CLAIM—review individually"
    if kind in {"module", "imports", "requires", "endmodule"}:
        return "ASSEMBLY"
    if start in USED.get(relative, set()):
        return "FIXED-SUPPLIED—target/load path"
    if "no-evaluators" in text or (
        "[total" in text and "symbol(" in text
    ):
        return "FIXED-SUPPLIED—opaque, target-unreachable"
    return "FIXED-SUPPLIED—target-unreachable"


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("|", "&#124;").replace("`", "&#96;")


paths = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
paths.extend([CANDIDATE / "verification.k", CANDIDATE / "spec.k"])

totals: dict[str, int] = {}
dispositions: dict[str, int] = {}
print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Generated from the trusted supplied-semantics tree plus the candidate's "
    "proof-local files. “Target-unreachable” means its LHS/sort/operator cannot "
    "occur on the submitted program's load/call path; it remains part of the "
    "fixed supplied trust boundary."
)
print()
for path in paths:
    relative = (
        path.relative_to(ROOT).as_posix()
        if path.is_relative_to(ROOT)
        else path.name
    )
    print(f"## {relative}")
    print()
    print("| Lines | Kind | Attributes | Disposition | Normalized declaration |")
    print("|---:|---|---|---|---|")
    for start, end, kind, text in blocks(path):
        totals[kind] = totals.get(kind, 0) + 1
        status = disposition(relative, start, kind, text)
        dispositions[status] = dispositions.get(status, 0) + 1
        line_range = str(start) if start == end else f"{start}-{end}"
        print(
            f"| {line_range} | {kind} | {', '.join(flags(text)) or '—'} | "
            f"{status} | {escape(text)} |"
        )
    print()

print("## Counts")
print()
print("Kinds: " + ", ".join(f"{key}={value}" for key, value in sorted(totals.items())))
print()
print(
    "Dispositions: "
    + ", ".join(f"{key}={value}" for key, value in sorted(dispositions.items()))
)
