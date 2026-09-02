#!/usr/bin/env python3
"""Emit a complete source-level inventory of K declarations, rules, and claims."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/tmp/audit-work/37-sort-even")
SOURCE_PATHS = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
    ROOT / "spec-connection.k",
]

START = re.compile(
    r'^(?P<filekind>requires)\s+"'
    r"|^(?P<modulekind>module|endmodule)\b"
    r"|^  (?P<kind>imports|configuration|syntax|context|rule|claim|alias)\b"
)
ATTRIBUTE_NAMES = [
    "function",
    "functional",
    "total",
    "macro",
    "macro-rec",
    "concrete",
    "simplification",
    "priority",
    "owise",
    "symbol",
    "no-evaluators",
]


@dataclass
class Item:
    path: Path
    line_start: int
    line_end: int
    kind: str
    text: str
    attributes: tuple[str, ...]


def compact(lines: list[str]) -> str:
    kept: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if "//" in stripped:
            stripped = stripped.split("//", 1)[0].rstrip()
        kept.append(stripped)
    return " ".join(" ".join(kept).split())


def parse(path: Path) -> list[Item]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if not match:
            continue
        kind = (
            match.group("filekind")
            or match.group("modulekind")
            or match.group("kind")
        )
        starts.append((index, kind))
    items: list[Item] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        statement_lines = lines[start:end]
        while statement_lines and (
            not statement_lines[-1].strip()
            or statement_lines[-1].lstrip().startswith("//")
        ):
            statement_lines.pop()
            end -= 1
        text = compact(statement_lines)
        attributes = tuple(
            name
            for name in ATTRIBUTE_NAMES
            if re.search(rf"(?<![A-Za-z0-9-]){re.escape(name)}(?![A-Za-z0-9-])", text)
        )
        items.append(
            Item(
                path=path,
                line_start=start + 1,
                line_end=end,
                kind=kind,
                text=text,
                attributes=attributes,
            )
        )
    return items


def role(item: Item) -> str:
    relative = item.path.relative_to(ROOT).as_posix()
    if relative == "verification.k":
        if item.kind == "syntax" and "macro" in item.attributes:
            return "proof-local syntax macro"
        if item.kind == "syntax" and "function" in item.attributes:
            return "proof-local definitional function"
        if item.kind == "rule" and item.line_start in {27, 32}:
            return "proof-local macro equation"
        if item.kind == "rule" and item.line_start in {51, 54, 57, 65}:
            return "proof-local definitional equation"
        if item.kind == "rule" and item.line_start == 85:
            return "proof-local operational bridge"
        return "proof module structure"
    if relative in {"spec.k", "spec-connection.k"} and item.kind == "claim":
        return "reachability claim"
    if item.kind == "syntax" and "no-evaluators" in item.attributes:
        return "supplied opaque/trusted primitive declaration"
    if item.kind == "rule" and "concrete" in item.attributes:
        return "supplied concrete-only equation"
    if item.kind == "rule" and "priority" in item.attributes:
        return "supplied priority semantic rule"
    if item.kind == "rule" and "owise" in item.attributes:
        return "supplied fallback semantic/equational rule"
    if item.kind == "rule":
        return "supplied semantic/equational rule"
    if item.kind == "syntax":
        return "supplied syntax/declaration"
    if item.kind == "configuration":
        return "supplied configuration"
    return "module/import structure"


def main() -> None:
    all_items: list[Item] = []
    for source in SOURCE_PATHS:
        all_items.extend(parse(source))

    counts_by_file: dict[str, Counter[str]] = defaultdict(Counter)
    for item in all_items:
        relative = item.path.relative_to(ROOT).as_posix()
        counts_by_file[relative][item.kind] += 1

    print("# Exhaustive K source inventory")
    print()
    print(
        "Generated directly from the fresh scratch source tree. Each `syntax` "
        "row contains the complete declaration, including every alternative; "
        "each `rule`/`claim` row contains its complete cells, guards, and attributes."
    )
    print()
    print("## Counts")
    print()
    print("| File | Syntax | Rules | Contexts | Configurations | Claims | Other |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for relative, counter in sorted(counts_by_file.items()):
        other = sum(
            count
            for kind, count in counter.items()
            if kind not in {"syntax", "rule", "context", "configuration", "claim"}
        )
        print(
            f"| `{relative}` | {counter['syntax']} | {counter['rule']} | "
            f"{counter['context']} | {counter['configuration']} | "
            f"{counter['claim']} | {other} |"
        )
    totals = Counter(item.kind for item in all_items)
    other_total = sum(
        count
        for kind, count in totals.items()
        if kind not in {"syntax", "rule", "context", "configuration", "claim"}
    )
    print(
        f"| **TOTAL** | **{totals['syntax']}** | **{totals['rule']}** | "
        f"**{totals['context']}** | **{totals['configuration']}** | "
        f"**{totals['claim']}** | **{other_total}** |"
    )

    for source in SOURCE_PATHS:
        relative = source.relative_to(ROOT).as_posix()
        print()
        print(f"## `{relative}`")
        print()
        for item in parse(source):
            location = (
                f"{item.line_start}"
                if item.line_start == item.line_end
                else f"{item.line_start}-{item.line_end}"
            )
            attrs = ",".join(item.attributes) if item.attributes else "-"
            print(
                f"- `{location}` `{item.kind}` [{attrs}] — {role(item)}: "
                f"`{item.text.replace('`', chr(92) + '`')}`"
            )


if __name__ == "__main__":
    main()
