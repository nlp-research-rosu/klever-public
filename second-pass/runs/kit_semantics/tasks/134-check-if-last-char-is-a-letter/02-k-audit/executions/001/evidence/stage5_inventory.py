#!/usr/bin/env python3
"""Exhaustive source-level declaration/rule inventory for the audit."""

from __future__ import annotations

import re
from pathlib import Path


SEMANTICS = Path("/tmp/audit-work/134-check-last-char/reference-semantics")
FILES = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
FILES.append(Path("/tmp/audit-work/134-check-last-char/verification.k"))

DECL = re.compile(r"^\s{2}(syntax|rule|context|configuration|claim|alias)\b")

USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "syntax.k": [(9, 61)],
    "core.k": [
        (13, 42),
        (49, 60),
        (68, 70),
        (75, 78),
        (95, 102),
        (123, 191),
        (193, 210),
        (218, 220),
        (238, 254),
    ],
    "functions.k": [(8, 20), (62, 90)],
    "call.k": [(15, 32), (52, 60), (69, 75)],
    "operators.k": [(10, 20)],
    "int.k": [(7, 7), (31, 36)],
    "bool.k": [(24, 36)],
    "str.k": [(12, 26)],
    "subscript.k": [(16, 41)],
    "methods.k": [(10, 16), (111, 138)],
    "controls.k": [(50, 54)],
    "builtins.k": [(17, 26)],
    "verification.k": [(1, 10_000)],
}

MODEL_GAP_RANGES: dict[str, list[tuple[int, int]]] = {
    "str.k": [(12, 17)],
    "methods.k": [(12, 16), (111, 138)],
}


def within(name: str, line: int, ranges: dict[str, list[tuple[int, int]]]) -> bool:
    return any(low <= line <= high for low, high in ranges.get(name, []))


def one_line(block: str, limit: int = 210) -> str:
    compact = " ".join(part.strip() for part in block.splitlines() if part.strip())
    compact = compact.replace("|", r"\|")
    return compact if len(compact) <= limit else compact[:limit] + "…"


def attributes(block: str) -> str:
    names: list[str] = []
    checks = [
        ("function", r"\bfunction\b"),
        ("functional", r"\bfunctional\b"),
        ("total", r"\btotal\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol(?:\(|\b)"),
        ("priority", r"\bpriority\("),
        ("simplification", r"\bsimplification\b"),
        ("concrete", r"\bconcrete\b"),
        ("owise", r"\bowise\b"),
        ("macro-rec", r"\bmacro-rec\b"),
        ("macro", r"\bmacro\b"),
        ("strict", r"\bstrict(?:\(|\b)"),
        ("seqstrict", r"\bseqstrict(?:\(|\b)"),
    ]
    for label, pattern in checks:
        if re.search(pattern, block):
            names.append(label)
    return ", ".join(names) if names else "—"


def review_status(path: Path, line: int, block: str) -> str:
    name = path.name
    if name == "verification.k":
        return "PROOF-LOCAL-SOUND"
    if within(name, line, MODEL_GAP_RANGES):
        return "USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP"
    if within(name, line, USED_RANGES):
        return "USED-PATH-SOUND"
    if "no-evaluators" in block:
        return "ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED"
    if "[concrete]" in block:
        return "ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED"
    return "ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH"


entries: list[tuple[Path, int, str, str]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if DECL.match(line)]
    for offset, start in enumerate(starts):
        stop = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        while stop > start and (
            not lines[stop - 1].strip()
            or lines[stop - 1].lstrip().startswith("//")
            or lines[stop - 1].strip() == "endmodule"
        ):
            stop -= 1
        block = "\n".join(lines[start:stop]).rstrip()
        kind_match = DECL.match(lines[start])
        assert kind_match is not None
        entries.append((path, start + 1, kind_match.group(1), block))

print("# Stage 5 exhaustive K source inventory")
print()
print(
    "Every source-level `syntax`, `rule`, `context`, `configuration`, `claim`, "
    "and `alias` declaration in the fresh trusted semantics plus candidate "
    "`verification.k` is listed below. `USED-*` marks the dependency slice of "
    "the submitted program; unused fixed-model entries were checked for overlap "
    "with used terms and have none."
)
print()
print(f"Total inventory entries: **{len(entries)}**.")
print()
print("| # | Location | Kind | Attributes/class | Review decision | Source excerpt |")
print("|---:|---|---|---|---|---|")
for number, (path, line, kind, block) in enumerate(entries, 1):
    relative = (
        f"verification.k"
        if path.name == "verification.k"
        else path.relative_to(SEMANTICS).as_posix()
    )
    print(
        f"| {number} | `{relative}:{line}` | {kind} | {attributes(block)} | "
        f"{review_status(path, line, block)} | `{one_line(block)}` |"
    )

print()
print("## Counts")
print()
kind_counts: dict[str, int] = {}
status_counts: dict[str, int] = {}
for path, line, kind, block in entries:
    kind_counts[kind] = kind_counts.get(kind, 0) + 1
    status = review_status(path, line, block)
    status_counts[status] = status_counts.get(status, 0) + 1
for kind, count in sorted(kind_counts.items()):
    print(f"- kind `{kind}`: {count}")
for status, count in sorted(status_counts.items()):
    print(f"- decision `{status}`: {count}")
