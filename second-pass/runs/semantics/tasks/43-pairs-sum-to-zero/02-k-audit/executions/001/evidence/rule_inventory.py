#!/usr/bin/env python3
"""Produce a source-indexed inventory of every local K declaration and rule."""

from __future__ import annotations

import collections
import re
from dataclasses import dataclass
from pathlib import Path


BASELINE_ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [
    Path("/tmp/audit-work/pairs-audit/verification.k"),
    Path("/tmp/audit-work/pairs-audit/spec.k"),
]

START = re.compile(
    r'^\s*(requires\s+"|module\b|endmodule\b|imports\b|'
    r"syntax\b|configuration\b|context\b|rule\b|claim\b|alias\b)"
)
KIND = re.compile(
    r'^\s*(requires|module|endmodule|imports|syntax|configuration|'
    r"context|rule|claim|alias)\b"
)


@dataclass(frozen=True)
class Item:
    source_class: str
    path: Path
    line: int
    kind: str
    text: str

    @property
    def attrs(self) -> str:
        found = []
        for attr in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", self.text):
                found.append(attr)
        return ",".join(found) if found else "-"


def normalized(lines: list[str]) -> str:
    pieces = []
    in_block_comment = False
    for raw in lines:
        text = raw.strip()
        if in_block_comment:
            if "*/" in text:
                text = text.split("*/", 1)[1].strip()
                in_block_comment = False
            else:
                continue
        while "/*" in text:
            before, after = text.split("/*", 1)
            if "*/" in after:
                after = after.split("*/", 1)[1]
                text = f"{before} {after}".strip()
            else:
                text = before.strip()
                in_block_comment = True
                break
        if "//" in text:
            text = text.split("//", 1)[0].rstrip()
        if text:
            pieces.append(text)
    return " ".join(" ".join(pieces).split())


def inventory_file(path: Path, source_class: str) -> list[Item]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    items: list[Item] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        text = normalized(lines[start:end])
        match = KIND.match(lines[start])
        if not match or not text:
            continue
        items.append(
            Item(
                source_class=source_class,
                path=path,
                line=start + 1,
                kind=match.group(1),
                text=text,
            )
        )
    return items


def display_path(item: Item) -> str:
    if item.source_class == "SUPPLIED_BASELINE":
        return str(item.path.relative_to(BASELINE_ROOT))
    return item.path.name


def main() -> int:
    files = sorted(BASELINE_ROOT.rglob("*.k"))
    items: list[Item] = []
    for path in files:
        items.extend(inventory_file(path, "SUPPLIED_BASELINE"))
    for path in CANDIDATE_FILES:
        items.extend(inventory_file(path, "CANDIDATE_LOCAL"))

    print("RULE INVENTORY")
    print(f"baseline_root={BASELINE_ROOT}")
    print("candidate_copies=/tmp/audit-work/pairs-audit/{verification.k,spec.k}")
    print(f"file_count={len(files) + len(CANDIDATE_FILES)}")
    print(f"item_count={len(items)}")

    by_source = collections.Counter(item.source_class for item in items)
    by_kind = collections.Counter(item.kind for item in items)
    print("counts_by_source=" + repr(dict(sorted(by_source.items()))))
    print("counts_by_kind=" + repr(dict(sorted(by_kind.items()))))

    attrs = collections.Counter()
    for item in items:
        for attr in item.attrs.split(","):
            if attr != "-":
                attrs[attr] += 1
    print("counts_by_attribute=" + repr(dict(sorted(attrs.items()))))

    print("\nPER_FILE_COUNTS")
    per_file = collections.Counter(
        (item.source_class, display_path(item), item.kind) for item in items
    )
    for (source_class, path, kind), count in sorted(per_file.items()):
        print(f"{source_class}|{path}|{kind}|{count}")

    print("\nOPAQUE_OR_SPECIAL_DECLARATIONS")
    for item in items:
        if item.kind == "syntax" and (
            "symbol" in item.attrs
            or "no-evaluators" in item.attrs
            or "functional" in item.attrs
        ):
            print(
                f"{item.source_class}|{display_path(item)}:{item.line}|"
                f"attrs={item.attrs}|{item.text}"
            )

    print("\nPRIORITY_SIMPLIFICATION_CONCRETE_RULES")
    for item in items:
        if item.kind in {"rule", "claim"} and any(
            attr in item.attrs
            for attr in ("priority", "simplification", "concrete")
        ):
            print(
                f"{item.source_class}|{display_path(item)}:{item.line}|"
                f"{item.kind}|attrs={item.attrs}|{item.text}"
            )

    print("\nCOMPLETE_INVENTORY")
    for index, item in enumerate(items, 1):
        print(
            f"{index:04d}|{item.source_class}|{display_path(item)}:{item.line}|"
            f"{item.kind}|attrs={item.attrs}|{item.text}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
