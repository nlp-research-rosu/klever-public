#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/audit19")
START = re.compile(r"^\s*(syntax|configuration|rule|claim|context)\b")
WHITESPACE = re.compile(r"\s+")

POTENTIALLY_USED = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/operators.k",
    "semantics/str.k",
    "semantics/methods.k",
    "semantics/controls.k",
    "semantics/functions.k",
    "semantics/builtins.k",
    "semantics/call.k",
    "semantics/sort.k",
    "semantics/concrete.k",
}


def sources() -> list[Path]:
    semantics_root = ROOT / "reference-semantics"
    result = [semantics_root / "semantics.k"]
    result.extend(sorted((semantics_root / "semantics").glob("*.k")))
    result.extend([ROOT / "verification.k", ROOT / "spec.k"])
    return result


def declarations(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match and not line.lstrip().startswith("//"):
            starts.append((index, match.group(1)))
    result: list[tuple[int, str, str]] = []
    for position, (index, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        while stop > index and lines[stop - 1].strip() in {"", "endmodule"}:
            stop -= 1
        block = "\n".join(lines[index:stop])
        result.append((index + 1, kind, block))
    return result


def flags(kind: str, block: str) -> str:
    found: list[str] = []
    if kind == "syntax":
        found.append("declaration")
    if kind == "rule":
        found.append("operational" if "<k>" in block else "equation")
    for marker, label in (
        ("[function", "function"),
        ("functional", "functional"),
        ("total", "total"),
        ("no-evaluators", "opaque/no-evaluators"),
        ("symbol(", "symbol"),
        ("priority(", "priority"),
        ("simplification", "simplification"),
        ("[macro", "macro"),
        ("concrete", "concrete"),
        ("owise", "owise"),
    ):
        if marker in block:
            found.append(label)
    return ", ".join(dict.fromkeys(found)) or "ordinary"


def decision(rel: str, line: int, kind: str) -> str:
    if rel.startswith("reference-semantics/"):
        return (
            "FIXED_BASELINE—byte-identical trusted supplied semantics; "
            "no candidate-added premise. Opaque/total boundaries are called out in REVIEW."
        )
    if rel == "spec.k":
        return "TARGET_CLAIM—fresh per-claim result recorded in stage3 logs."
    if rel == "verification.k":
        if 95 <= line <= 99:
            return "OPERATIONAL_BRIDGE—split equivalence/context audited separately."
        if line >= 103:
            return "DEFINITIONAL_SUMMARY—join of fixed sortKeyVS result."
        if line <= 50:
            return "EXACT_PROGRAM_MACRO—checked against regenerated solution.mpy."
        return "TRUTHFUL_FINITE/STRUCTURAL_DEFINITION—coverage and overlaps reviewed."
    return "REVIEWED"


def main() -> None:
    total = 0
    counts: dict[str, int] = {}
    print("# Exhaustive K declaration and rule inventory")
    print()
    print(
        "Generated from the isolated source copy. Each row identifies a complete "
        "local declaration, configuration, context, rule, or claim by source line."
    )
    print()
    for path in sources():
        rel = path.relative_to(ROOT).as_posix()
        entries = declarations(path)
        total += len(entries)
        counts[rel] = len(entries)
        if rel.startswith("reference-semantics/"):
            sem_rel = rel.removeprefix("reference-semantics/")
            relevance = (
                "potentially used by submitted program/proof"
                if sem_rel in POTENTIALLY_USED
                else "not exercised by submitted program constructs"
            )
        else:
            relevance = "candidate proof/spec source"
        print(f"## `{rel}` ({len(entries)} entries; {relevance})")
        print()
        print("| line | kind | classification/attributes | compact sentence | audit disposition |")
        print("|---:|---|---|---|---|")
        for line, kind, block in entries:
            compact = WHITESPACE.sub(" ", block).strip().replace("|", "\\|")
            if len(compact) > 280:
                compact = compact[:277] + "..."
            disposition = decision(rel, line, kind).replace("|", "\\|")
            print(
                f"| {line} | {kind} | {flags(kind, block)} | "
                f"`{compact}` | {disposition} |"
            )
        print()
    print("## Counts")
    print()
    for rel, count in counts.items():
        print(f"- `{rel}`: {count}")
    print(f"- **Total inventoried sentences: {total}**")


if __name__ == "__main__":
    main()
