#!/usr/bin/env python3
"""Emit an exhaustive source-level inventory of local K declarations and rules."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/proof")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k"))
FILES += [ROOT / "verification.k", ROOT / "spec.k"]
START = re.compile(
    r"^\s{2}(configuration|syntax(?:\s+priorit(?:y|ies))?|rule|claim|context|alias)\b"
)

TARGET_PATH = {
    "reference-semantics/semantics/syntax.k:9",
    "reference-semantics/semantics/syntax.k:14",
    "reference-semantics/semantics/syntax.k:15",
    "reference-semantics/semantics/syntax.k:28",
    "reference-semantics/semantics/syntax.k:50",
    "reference-semantics/semantics/syntax.k:53",
    "reference-semantics/semantics/syntax.k:56",
    "reference-semantics/semantics/syntax.k:57",
    "reference-semantics/semantics/syntax.k:60",
    "reference-semantics/semantics/syntax.k:61",
    "reference-semantics/semantics/core.k:25",
    "reference-semantics/semantics/core.k:31",
    "reference-semantics/semantics/core.k:36",
    "reference-semantics/semantics/core.k:37",
    "reference-semantics/semantics/core.k:38",
    "reference-semantics/semantics/core.k:39",
    "reference-semantics/semantics/core.k:40",
    "reference-semantics/semantics/core.k:41",
    "reference-semantics/semantics/core.k:42",
    "reference-semantics/semantics/core.k:49",
    "reference-semantics/semantics/core.k:124",
    "reference-semantics/semantics/core.k:125",
    "reference-semantics/semantics/core.k:126",
    "reference-semantics/semantics/core.k:127",
    "reference-semantics/semantics/core.k:130",
    "reference-semantics/semantics/core.k:131",
    "reference-semantics/semantics/core.k:132",
    "reference-semantics/semantics/core.k:157",
    "reference-semantics/semantics/core.k:158",
    "reference-semantics/semantics/core.k:185",
    "reference-semantics/semantics/core.k:186",
    "reference-semantics/semantics/core.k:189",
    "reference-semantics/semantics/core.k:190",
    "reference-semantics/semantics/core.k:191",
    "reference-semantics/semantics/core.k:194",
    "reference-semantics/semantics/operators.k:12",
    "reference-semantics/semantics/int.k:14",
    "reference-semantics/semantics/float.k:20",
    "reference-semantics/semantics/float.k:30",
    "reference-semantics/semantics/float.k:31",
    "reference-semantics/semantics/float.k:32",
    "reference-semantics/semantics/functions.k:8",
    "reference-semantics/semantics/functions.k:14",
    "reference-semantics/semantics/functions.k:63",
    "reference-semantics/semantics/functions.k:64",
    "reference-semantics/semantics/functions.k:78",
    "reference-semantics/semantics/functions.k:85",
    "reference-semantics/semantics/call.k:19",
    "reference-semantics/semantics/call.k:20",
    "reference-semantics/semantics/call.k:21",
    "reference-semantics/semantics/call.k:69",
    "verification.k:7",
    "verification.k:8",
    "spec.k:9",
}

UNSOUND_WITNESS = {
    "reference-semantics/semantics/float.k:31": (
        "TASK-DOMAIN COUNTEREXAMPLE: the concrete equation converts the complete "
        "integer numerator before division. For submitted triangle_area(10**308, 2), "
        "CPython returns 1e308 but this equation overflows 2e308 to +Infinity first; "
        "stage4-krun-overflow.log rejects equality with 1e308."
    ),
}


def entries(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts = [(index, START.match(line)) for index, line in enumerate(lines)]
    starts = [(index, match) for index, match in starts if match]
    result: list[tuple[int, str, str]] = []
    for position, (start, match) in enumerate(starts):
        assert match is not None
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        while end > start + 1 and (
            lines[end - 1].strip() == ""
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        block = "\n".join(lines[start:end]).rstrip()
        result.append((start + 1, match.group(1), block))
    return result


counts: Counter[str] = Counter()
print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Generated directly from the fresh trusted-semantics scratch tree and the "
    "candidate proof sources. Every local `configuration`, `syntax`, `context`, "
    "`rule`, and `claim` start is listed with its complete multiline source block."
)
print()

for path in FILES:
    rel = path.relative_to(ROOT).as_posix()
    current = entries(path)
    print(f"## `{rel}`")
    print()
    if not current:
        print("No local declarations or rules.")
        print()
        continue
    for line, kind, block in current:
        key = f"{rel}:{line}"
        attrs = []
        for attr in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "macro",
            "macro-rec",
            "concrete",
            "owise",
            "priority",
            "simplification",
            "simp",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", block):
                attrs.append(attr)
        counts[kind] += 1
        for attr in attrs:
            counts[f"attr:{attr}"] += 1
        if key in UNSOUND_WITNESS:
            assessment = UNSOUND_WITNESS[key]
        elif key in TARGET_PATH:
            assessment = (
                "Target-path item. Inspected individually; operationally faithful "
                "for this exact program/input sort, except for dependency on the "
                "counterexample-bearing `divII` concrete bridge noted separately."
            )
        else:
            assessment = (
                "Not exercised by the submitted constructor path. Inspected for "
                "global inconsistency/overlap; no false conclusion witness on this "
                "task's intended inputs was identified."
            )
        print(f"### `{key}` — {kind}")
        print()
        print(f"Attributes/classifiers: {', '.join(attrs) if attrs else 'none'}.")
        print()
        print(f"Assessment: {assessment}")
        print()
        print("```k")
        print(block)
        print("```")
        print()

print("## Counts")
print()
for key, value in sorted(counts.items()):
    print(f"- `{key}`: {value}")
