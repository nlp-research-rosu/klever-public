#!/usr/bin/env python3
"""Mechanical inventory of K declarations/rules for the static audit.

This does not decide soundness. It ensures every declaration anchor and every
semantically relevant attribute in the supplied semantics and verification
extension is enumerated with its complete source block and location.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k"))
FILES.append(ROOT / "verification.k")

ANCHOR_RE = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\b|context\s+alias\b)"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "symbol",
    "opaque",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "macro",
    "anywhere",
    "hook",
)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def anchors(lines: list[str]) -> list[int]:
    return [i for i, line in enumerate(lines) if ANCHOR_RE.match(line)]


def trim_block(block: list[str]) -> list[str]:
    while block and not block[-1].strip():
        block.pop()
    while block and block[-1].lstrip().startswith("//"):
        block.pop()
        while block and not block[-1].strip():
            block.pop()
    return block


def code_without_line_comments(text: str) -> str:
    """Remove // comments while retaining // inside K string tokens."""
    output: list[str] = []
    for line in text.splitlines():
        in_string = False
        escaped = False
        cut = len(line)
        for index, char in enumerate(line):
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "/" and index + 1 < len(line) and line[index + 1] == "/":
                cut = index
                break
        output.append(line[:cut])
    return "\n".join(output)


counter: Counter[str] = Counter()
attribute_entries: list[tuple[str, int, str]] = []
opaque_candidates: list[tuple[str, int, str]] = []
records: list[str] = []

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = anchors(lines)
    records.append(f"\n## {relative(path)}\n")
    records.append(f"Declaration anchors: {len(starts)}\n")
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = trim_block(lines[start:end])
        first = block[0].strip()
        kind = first.split(maxsplit=1)[0]
        counter[kind] += 1
        text = "\n".join(block)
        code = code_without_line_comments(text)
        attribute_text = " ".join(re.findall(r"\[[^\]\n]+\]", code))
        found_attrs = [
            attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", attribute_text)
        ]
        for attr in found_attrs:
            counter[f"attr:{attr}"] += 1
            attribute_entries.append((relative(path), start + 1, attr))
        if kind == "syntax" and (
            "symbol" in found_attrs
            or "opaque" in found_attrs
            or ("function" in found_attrs and "concrete" in found_attrs)
        ):
            opaque_candidates.append((relative(path), start + 1, first))
        attr_suffix = f" attrs={','.join(found_attrs)}" if found_attrs else ""
        records.append(
            f"\n### {kind.upper()} {relative(path)}:{start + 1}{attr_suffix}\n\n"
        )
        records.append("```k\n")
        for line_number, line in enumerate(block, start=start + 1):
            records.append(f"{line_number:5d} {line}\n")
        records.append("```\n")

print("# Exhaustive K declaration and rule inventory")
print()
print("Source set:")
for path in FILES:
    print(f"- `{relative(path)}`")
print()
print("Mechanical counts:")
for key in sorted(counter):
    print(f"- `{key}`: {counter[key]}")
print()
print("Every attribute occurrence by containing declaration block:")
for path, line, attr in attribute_entries:
    print(f"- `{attr}` — `{path}:{line}`")
print()
print("Opaque/symbolic/concrete-only declaration candidates:")
if opaque_candidates:
    for path, line, first in opaque_candidates:
        print(f"- `{path}:{line}` — `{first}`")
else:
    print("- none")
print("".join(records))
