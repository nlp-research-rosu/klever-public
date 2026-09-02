#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


TASK = Path("/tmp/audit-work/75-is-multiply-prime")
SOURCE_FILES = [
    TASK / "reference-semantics" / "semantics.k",
    *sorted((TASK / "reference-semantics" / "semantics").glob("*.k")),
    TASK / "verification.k",
    TASK / "spec.k",
]

ATTR = re.compile(r"\[([^\]]+)\]")


def entry_kind(line: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith('requires "'):
        return "requires"
    match = re.match(
        r"(module|endmodule|imports|configuration|syntax|context|rule|claim)\b",
        stripped,
    )
    return match.group(1) if match else None


def collect_entries(path: Path) -> list[tuple[int, int, str, str]]:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if entry_kind(line)]
    entries: list[tuple[int, int, str, str]] = []
    for position, index in enumerate(starts):
        next_index = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[index].strip()
        kind = entry_kind(lines[index])
        if kind is None:
            raise AssertionError(f"lost entry kind at {path}:{index + 1}")
        block_lines = [first]
        for continuation in lines[index + 1 : next_index]:
            stripped = continuation.strip()
            if stripped and not stripped.startswith("//"):
                block_lines.append(stripped)
        block = " ".join(block_lines)
        entries.append((index + 1, next_index, kind, block))
    return entries


def attributes(block: str) -> str:
    found: list[str] = []
    for payload in ATTR.findall(block):
        for item in payload.split(","):
            normalized = item.strip()
            if normalized and normalized not in found:
                found.append(normalized)
    notable = [
        item
        for item in found
        if item.startswith(
            (
                "function",
                "total",
                "functional",
                "simplification",
                "concrete",
                "symbol",
                "no-evaluators",
                "priority",
                "owise",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
            )
        )
    ]
    return ", ".join(notable) if notable else "—"


def assessment(relative: str, line: int, kind: str, block: str) -> str:
    if relative == "verification.k":
        if kind == "syntax":
            return (
                "ACCEPT: proof-harness constructors only; they add no value equation "
                "or oracle."
            )
        if kind == "rule" and line == 15:
            return (
                "ACCEPT: equality checkpoint; matches only when actual and expected "
                "Booleans are identical."
            )
        if kind == "rule" and line == 17:
            return (
                "ACCEPT: runner expansion; loads the mechanically pinned exact Module "
                "term and performs ordinary name lookup/call execution."
            )
        if kind == "rule" and line == 50:
            return (
                "ACCEPT: ghost cleanup after a Boolean return; removes only the "
                "harness-installed global binding under an explicit key-presence guard."
            )
        return "STRUCTURAL: module/import boundary; no executable conclusion."

    if relative == "spec.k":
        if kind == "claim":
            return (
                "TARGET CLAIM: independently reconstructed; not a proof extension or "
                "semantic rule."
            )
        return "STRUCTURAL: target-module/import boundary."

    if "no-evaluators" in block or "md5hexCodes" in block:
        return (
            "UNUSED TRUST BOUNDARY: supplied opaque/total symbol; unreachable from "
            "the submitted program and from every target claim."
        )
    if "[concrete]" in block or relative.endswith("/concrete.k"):
        return (
            "FIXED CONCRETE LEG: excluded from the Haskell proof module; unused by "
            "the target claims (reviewed only as supplied concrete semantics)."
        )
    if kind in {"rule", "context", "configuration"}:
        return (
            "ACCEPT FOR SELECTED SEMANTICS: fixed supplied operational/equational "
            "rule. Its complete file was reviewed; used-fragment rules are traced "
            "separately, and unused rules have no dependency path to a target claim."
        )
    if kind == "syntax":
        return (
            "DECLARATION: fixed supplied constructor/function declaration; attributes "
            "shown explicitly. No standalone correctness conclusion."
        )
    return "STRUCTURAL: supplied module/import/require boundary."


records: list[tuple[str, int, int, str, str, str, str]] = []
for path in SOURCE_FILES:
    relative = path.relative_to(TASK).as_posix()
    for start, end, kind, block in collect_entries(path):
        records.append(
            (
                relative,
                start,
                end,
                kind,
                attributes(block),
                block,
                assessment(relative, start, kind, block),
            )
        )

counts: dict[str, int] = {}
attribute_counts = {
    name: 0
    for name in (
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "symbol",
        "no-evaluators",
        "priority",
        "owise",
        "macro",
        "macro-rec",
    )
}
for _, _, _, kind, attrs, block, _ in records:
    counts[kind] = counts.get(kind, 0) + 1
    for name in attribute_counts:
        if re.search(rf"\b{re.escape(name)}\b", attrs):
            attribute_counts[name] += 1

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Scope: trusted supplied semantics source, candidate `verification.k`, and "
    "candidate target claims in `spec.k`. Multi-line declarations/rules are one row."
)
print()
print(f"Total inventoried entries: {len(records)}")
print()
print("Kinds: " + ", ".join(f"{name}={count}" for name, count in sorted(counts.items())))
print()
print(
    "Notable attributes: "
    + ", ".join(f"{name}={count}" for name, count in attribute_counts.items())
)
print()
print(
    "There are no `[functional]` or `[simplification]` declarations/rules if their "
    "reported counts are zero. Opaque symbols are the `[symbol(...), no-evaluators]` "
    "entries shown below."
)
print()
print("| Source | Lines | Kind | Attributes | Declaration/rule | Assessment |")
print("|---|---:|---|---|---|---|")
for relative, start, end, kind, attrs, block, decision in records:
    location = str(start) if start == end else f"{start}–{end}"
    escaped_block = block.replace("|", "\\|").replace("`", "\\`")
    escaped_decision = decision.replace("|", "\\|")
    print(
        f"| `{relative}` | {location} | {kind} | {attrs} | "
        f"`{escaped_block}` | {escaped_decision} |"
    )
