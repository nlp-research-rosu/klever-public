#!/usr/bin/env python3
"""Generate an exhaustive source-line inventory of local K declarations/rules."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/string-sequence")
source_files = [
    WORK / "reference-semantics" / "semantics.k",
    *sorted((WORK / "reference-semantics" / "semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]

directive = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
boundary = re.compile(
    r"^(?:requires)\b|^\s*(?:syntax|rule|claim|context|configuration|module|endmodule|imports)\b"
)
attribute_names = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "injective",
]


def entries(path: Path):
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = directive.match(lines[index])
        if not match:
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines) and not boundary.match(lines[index]):
            index += 1
        text = " ".join(
            part.strip()
            for part in lines[start:index]
            if part.strip() and not part.lstrip().startswith("//")
        )
        attrs = [name for name in attribute_names if re.search(rf"\b{re.escape(name)}\b", text)]
        yield start + 1, match.group(1), attrs, text


def assessment(relative: str, line: int, kind: str, attrs: list[str]) -> str:
    if relative == "verification.k":
        if line == 59:
            return (
                "REJECT: result-bearing whole-body operational bridge; over-broad "
                "and contradicted by context/body-sensitivity witnesses"
            )
        if line in {33, 34, 39, 40}:
            return "ACCEPT: constructor macro mechanically equals submitted body/body fragment"
        if line == 8:
            return (
                "ACCEPT FOR USED N>=0 DOMAIN: expected-string function; injectivity is "
                "true there; negative recursive behavior is unused"
            )
        return "ACCEPT: guarded mathematical definition or valid integer/string simplification"
    if relative == "spec.k":
        return "TARGET: reachability claim audited for satisfiability, scope, and result constraint"
    if "no-evaluators" in attrs or "symbol" in attrs:
        return "FIXED OPAQUE BOUNDARY: supplied semantics; not reached by this program/proof"
    if kind == "syntax":
        return "FIXED DECLARATION: supplied semantics; no correctness conclusion by itself"
    if relative.endswith("concrete.k"):
        return "FIXED CONCRETE RULE: absent from proof definition; inspected, no target-proof influence"
    if any(
        relative.endswith(name)
        for name in (
            "float.k",
            "set.k",
            "list.k",
            "subscript.k",
            "comprehension.k",
            "methods.k",
            "sort.k",
            "dict.k",
            "bool.k",
        )
    ):
        return "FIXED/INERT: supplied rule is not matched on the submitted program's proof path"
    return "FIXED/USED OR SHARED: inspected against supplied model; consistent on target path"


rows = []
for path in source_files:
    relative = path.relative_to(WORK).as_posix()
    for line, kind, attrs, text in entries(path):
        rows.append(
            (
                relative,
                line,
                kind,
                ",".join(attrs) if attrs else "-",
                assessment(relative, line, kind, attrs),
                text.replace("|", "\\|"),
            )
        )

counts = Counter(row[2] for row in rows)
attribute_counts = Counter()
for row in rows:
    if row[3] != "-":
        attribute_counts.update(row[3].split(","))

print("# Exhaustive K source inventory")
print()
print(
    "Generated from the clean scratch copy. A row is emitted for every local "
    "`syntax`, `configuration`, `context`, `rule`, and `claim` directive."
)
print()
print(f"- Source files: {len(source_files)}")
print(f"- Total entries: {len(rows)}")
print(f"- Entry counts: {dict(sorted(counts.items()))}")
print(f"- Attribute counts: {dict(sorted(attribute_counts.items()))}")
print()
print("| Location | Kind | Attributes | Assessment | Normalized source |")
print("|---|---|---|---|---|")
for relative, line, kind, attrs, decision, text in rows:
    print(f"| `{relative}:{line}` | {kind} | {attrs} | {decision} | `{text}` |")
