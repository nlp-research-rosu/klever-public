#!/usr/bin/env python3
"""Exhaustive source-level inventory for the supplied and proof-local K files."""

from __future__ import annotations

import re
from pathlib import Path


root = Path("/tmp/audit-work/fresh")
paths = [
    root / "reference-semantics/semantics.k",
    *sorted((root / "reference-semantics/semantics").glob("*.k")),
    root / "verification.k",
    root / "spec.k",
]

start_re = re.compile(
    r"^(?:"
    r"(?P<requires>requires)\b|"
    r"\s*(?P<other>module|imports|endmodule|configuration|syntax|rule|context|claim)\b"
    r")"
)

# Source locations that are on the target's execution path or mechanically
# normalize the submitted module into the entry claim.
used_ranges: dict[str, list[tuple[int, int, str]]] = {
    "semantics/syntax.k": [
        (9, 16, "used Expr constructors and strictness"),
        (41, 61, "used Stmt/Params/Stmts/Module constructors"),
    ],
    "semantics/core.k": [
        (25, 60, "used values and configuration cells"),
        (123, 191, "module load, lookup, arguments, call tag"),
        (208, 215, "operator dispatch and argument accumulation"),
    ],
    "semantics/str.k": [(12, 17, "docstring normalization only")],
    "semantics/controls.k": [(46, 48, "docstring Expr discard only")],
    "semantics/functions.k": [
        (8, 20, "closure construction"),
        (62, 90, "parameter binding, return, frame pop"),
    ],
    "semantics/call.k": [
        (18, 32, "callee and argument routing"),
        (69, 74, "closure call frame"),
    ],
    "semantics/operators.k": [(10, 17, "binary operator dispatch")],
    "semantics/float.k": [(19, 39, "float literal and modulo primitive")],
}


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(root / "reference-semantics"))
    except ValueError:
        return str(path.relative_to(root))


def disposition(path: Path, line: int, kind: str) -> str:
    rel = relative(path)
    if rel == "verification.k":
        return "PROOF_LOCAL_NO_EXTENSION"
    if rel == "spec.k":
        return "TARGET_ENTRY_CLAIM_REVIEWED" if kind == "claim" else "TARGET_SPEC_ASSEMBLY"
    if rel == "semantics.k":
        return "FIXED_SUPPLIED_ASSEMBLY"
    for lo, hi, why in used_ranges.get(rel, []):
        if lo <= line <= hi:
            if "only" in why or "closure construction" in why:
                return "PINNING_NORMALIZATION_REVIEWED"
            return "TARGET_EXECUTION_PATH_REVIEWED"
    return "FIXED_SUPPLIED_NOT_TARGET_REACHABLE"


def code_without_line_comments(snippet: str) -> str:
    """Remove // comments while respecting quoted K string literals."""
    out: list[str] = []
    quoted = False
    escaped = False
    i = 0
    while i < len(snippet):
        ch = snippet[i]
        if quoted:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            i += 1
            continue
        if ch == '"':
            quoted = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < len(snippet) and snippet[i + 1] == "/":
            newline = snippet.find("\n", i + 2)
            if newline == -1:
                break
            out.append("\n")
            i = newline + 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def attributes(snippet: str) -> set[str]:
    code = code_without_line_comments(snippet)
    found: set[str] = set()
    for block in re.findall(r"\[([^\]]*)\]", code):
        for name in (
            "function",
            "total",
            "functional",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "macro",
        ):
            if re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", block):
                found.add(name)
    return found


entries: list[tuple[Path, int, int, str, str]] = []
for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for number, text in enumerate(lines, 1):
        match = start_re.match(text)
        if match:
            starts.append((number, match.group("requires") or match.group("other")))
    for index, (number, kind) in enumerate(starts):
        next_number = starts[index + 1][0] if index + 1 < len(starts) else len(lines) + 1
        if kind in {"requires", "module", "imports", "endmodule"}:
            end = number
        else:
            end = next_number - 1
            while end > number and not lines[end - 1].strip():
                end -= 1
            while end > number and lines[end - 1].lstrip().startswith("//"):
                end -= 1
        snippet = "\n".join(part.strip() for part in lines[number - 1 : end] if part.strip())
        entries.append((path, number, end, kind, snippet))

print(
    "id\tfile\tlines\tkind\tfunction\ttotal\tfunctional\topaque_no_evaluators"
    "\tpriority\tsimplification\tconcrete\towise\tmacro\tdisposition\tsource"
)
for entry_id, (path, start, end, kind, snippet) in enumerate(entries, 1):
    found = attributes(snippet)
    attrs = {
        "function": "function" in found,
        "total": "total" in found,
        "functional": "functional" in found,
        "opaque": "no-evaluators" in found,
        "priority": "priority" in found,
        "simplification": "simplification" in found,
        "concrete": "concrete" in found,
        "owise": "owise" in found,
        "macro": "macro" in found,
    }
    safe = snippet.replace("\t", " ").replace("\n", " ")
    print(
        "\t".join(
            [
                str(entry_id),
                relative(path),
                f"{start}-{end}",
                kind,
                str(attrs["function"]).lower(),
                str(attrs["total"]).lower(),
                str(attrs["functional"]).lower(),
                str(attrs["opaque"]).lower(),
                str(attrs["priority"]).lower(),
                str(attrs["simplification"]).lower(),
                str(attrs["concrete"]).lower(),
                str(attrs["owise"]).lower(),
                str(attrs["macro"]).lower(),
                disposition(path, start, kind),
                safe,
            ]
        )
    )

print("SUMMARY_ENTRIES", len(entries))
for key in (
    "syntax",
    "rule",
    "context",
    "configuration",
    "claim",
    "requires",
    "module",
    "imports",
    "endmodule",
):
    print("SUMMARY_KIND", key, sum(entry[3] == key for entry in entries))
for label, attribute in (
    ("function", "function"),
    ("total", "total"),
    ("functional", "functional"),
    ("opaque_no_evaluators", "no-evaluators"),
    ("priority", "priority"),
    ("simplification", "simplification"),
    ("concrete", "concrete"),
    ("owise", "owise"),
    ("macro", "macro"),
):
    print(
        "SUMMARY_ATTRIBUTE",
        label,
        sum(attribute in attributes(entry[4]) for entry in entries),
    )
for status in sorted({disposition(path, line, kind) for path, line, _, kind, _ in entries}):
    print(
        "SUMMARY_DISPOSITION",
        status,
        sum(disposition(path, line, kind) == status for path, line, _, kind, _ in entries),
    )
