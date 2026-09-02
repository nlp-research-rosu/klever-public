#!/usr/bin/env python3
"""Exhaustive source-indexed inventory of supplied and proof-local K declarations."""

from __future__ import annotations

import collections
import re
from pathlib import Path

TRUSTED = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate")
FILES = sorted(TRUSTED.rglob("*.k")) + [
    CANDIDATE / "verification.k",
    CANDIDATE / "spec.k",
]

START = re.compile(
    r"^(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
ATTR_WORDS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "no-evaluators",
    "concrete",
    "macro",
    "macro-rec",
    "owise",
    "strict",
    "seqstrict",
    "symbol",
)


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    result = []
    for index, line in enumerate(lines):
        stripped_line = line.strip()
        match = START.match(stripped_line)
        if line.startswith('requires "'):
            kind = "requires"
        elif match is not None:
            kind = match.group(1)
        else:
            continue
        block = [stripped_line]
        if kind not in {"requires", "module", "endmodule", "imports"}:
            cursor = index + 1
            while cursor < len(lines):
                stripped = lines[cursor].strip()
                if (
                    not stripped
                    or stripped.startswith("//")
                    or START.match(stripped)
                    or lines[cursor].startswith('requires "')
                ):
                    break
                block.append(stripped)
                cursor += 1
        normalized = " ".join(block)
        attrs = [word for word in ATTR_WORDS if re.search(rf"\b{re.escape(word)}\b", normalized)]
        result.append((index + 1, kind, attrs, normalized))
    return result


print("# Exhaustive K declaration and rule inventory")
print()
print("Generated from the mounted trusted supplied semantics and mounted candidate sources.")
print()
print("## Counts by file")
print()
print("| File | modules | syntax | contexts | configuration | rules | claims | priority | simplification | function | total | functional | opaque/no-evaluators | concrete | macros |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

all_decls = {}
totals = collections.Counter()
for path in FILES:
    decls = declarations(path)
    all_decls[path] = decls
    counts = collections.Counter(kind for _, kind, _, _ in decls)
    attr_counts = collections.Counter(attr for _, _, attrs, _ in decls for attr in attrs)
    relative = (
        "trusted/" + str(path.relative_to(TRUSTED))
        if path.is_relative_to(TRUSTED)
        else "candidate/" + path.name
    )
    print(
        f"| `{relative}` | {counts['module']} | {counts['syntax']} | "
        f"{counts['context']} | {counts['configuration']} | {counts['rule']} | "
        f"{counts['claim']} | {attr_counts['priority']} | "
        f"{attr_counts['simplification']} | {attr_counts['function']} | "
        f"{attr_counts['total']} | {attr_counts['functional']} | "
        f"{attr_counts['no-evaluators']} | {attr_counts['concrete']} | "
        f"{attr_counts['macro'] + attr_counts['macro-rec']} |"
    )
    totals.update(counts)
    totals.update({f"attr:{key}": value for key, value in attr_counts.items()})

print()
print(
    "Totals: "
    f"{totals['syntax']} syntax declarations; {totals['context']} contexts; "
    f"{totals['configuration']} configurations; {totals['rule']} rules; "
    f"{totals['claim']} claims; {totals['attr:priority']} priority-bearing declarations; "
    f"{totals['attr:simplification']} simplifications; "
    f"{totals['attr:function']} function declarations; {totals['attr:total']} total declarations; "
    f"{totals['attr:functional']} functional declarations; "
    f"{totals['attr:no-evaluators']} explicit opaque/no-evaluators declarations."
)

for path, decls in all_decls.items():
    relative = (
        "trusted/" + str(path.relative_to(TRUSTED))
        if path.is_relative_to(TRUSTED)
        else "candidate/" + path.name
    )
    print()
    print(f"## `{relative}`")
    print()
    for line_number, kind, attrs, normalized in decls:
        attr_text = ", ".join(attrs) if attrs else "none"
        print(
            f"- L{line_number} — `{kind}` — attributes: {attr_text} — "
            f"`{normalized.replace('`', chr(92) + '`')}`"
        )
