#!/usr/bin/env python3
"""Build an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import argparse
import collections
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias)\b")


@dataclass(frozen=True)
class Item:
    relative_path: str
    start: int
    end: int
    kind: str
    text: str
    origin: str

    @property
    def tags(self) -> list[str]:
        found: list[str] = []
        checks = [
            ("function", r"\bfunction\b"),
            ("functional", r"\bfunctional\b"),
            ("total", r"\btotal\b"),
            ("macro", r"\bmacro(?:-rec)?\b"),
            ("simplification", r"\bsimplification\b"),
            ("priority", r"\bpriority\s*\("),
            ("owise", r"\bowise\b"),
            ("concrete", r"\bconcrete\b"),
            ("symbol", r"\bsymbol\s*(?:\(|[,}\]])"),
            ("no-evaluators", r"\bno-evaluators\b"),
        ]
        for name, pattern in checks:
            if re.search(pattern, self.text):
                found.append(name)
        if re.search(r"\bopaque\b", self.text, flags=re.IGNORECASE):
            found.append("mentions-opaque")
        return found


def source_items(path: Path, root: Path, origin: str) -> list[Item]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))

    items: list[Item] = []
    for position, (start, kind) in enumerate(starts):
        boundary = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = boundary
        while end > start and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        text = "\n".join(lines[start:end]).rstrip()
        items.append(
            Item(
                relative_path=str(path.relative_to(root)),
                start=start + 1,
                end=end,
                kind=kind,
                text=text,
                origin=origin,
            )
        )
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    selected_semantics = sorted(
        (args.scratch / "reference-semantics").rglob("*.k")
    )
    proof_local = [
        args.scratch / "verification.k",
        args.scratch / "spec.k",
    ]

    items: list[Item] = []
    for path in selected_semantics:
        items.extend(
            source_items(
                path,
                args.scratch,
                "selected supplied semantics; byte-identical trusted baseline",
            )
        )
    for path in proof_local:
        items.extend(source_items(path, args.scratch, "candidate proof-local"))

    counts: collections.Counter[tuple[str, str]] = collections.Counter(
        (item.relative_path, item.kind) for item in items
    )
    source_relative_paths = [
        str(path.relative_to(args.scratch))
        for path in selected_semantics + proof_local
    ]
    paths_with_items = {item.relative_path for item in items}
    tag_counts: collections.Counter[str] = collections.Counter(
        tag for item in items for tag in item.tags
    )
    source_digest = hashlib.sha256()
    for path in selected_semantics + proof_local:
        source_digest.update(str(path.relative_to(args.scratch)).encode())
        source_digest.update(b"\0")
        source_digest.update(path.read_bytes())
        source_digest.update(b"\0")

    with args.output.open("w", encoding="utf-8") as output:
        output.write("# Exhaustive K declaration and rule inventory\n\n")
        output.write(
            "Generated from the fresh scratch source. The supplied-semantics "
            "entries are fixed by the trusted byte-identical baseline; proof-local "
            "entries require independent substantive review.\n\n"
        )
        output.write(f"SOURCE_SET_SHA256: `{source_digest.hexdigest()}`\n\n")
        output.write(f"TOTAL_ITEMS: {len(items)}\n\n")
        output.write("## Counts by file and kind\n\n")
        output.write("| File | Kind | Count |\n|---|---:|---:|\n")
        for relative_path in source_relative_paths:
            if relative_path not in paths_with_items:
                output.write(
                    f"| `{relative_path}` | no local syntax/config/rule/claim | 0 |\n"
                )
        for (relative_path, kind), count in sorted(counts.items()):
            output.write(f"| `{relative_path}` | {kind} | {count} |\n")
        output.write("\n## Attribute/tag counts\n\n")
        output.write("| Tag | Count |\n|---|---:|\n")
        for tag, count in sorted(tag_counts.items()):
            output.write(f"| {tag} | {count} |\n")

        output.write("\n## Every declaration/rule/claim\n\n")
        for item_id, item in enumerate(items, start=1):
            tags = ", ".join(item.tags) if item.tags else "none"
            if item.origin.startswith("selected supplied"):
                disposition = (
                    "FIXED_BASELINE: accepted as the selected operational "
                    "language definition in SUPPLIED_SEMANTICS mode; any opaque "
                    "or partial boundary is accounted for separately if reachable."
                )
            else:
                disposition = "PROOF_LOCAL: see the hand-audited per-item review."
            output.write(
                f"### K-{item_id:04d}: `{item.relative_path}:{item.start}`\n\n"
            )
            output.write(f"- Kind: {item.kind}\n")
            output.write(f"- Lines: {item.start}-{item.end}\n")
            output.write(f"- Origin: {item.origin}\n")
            output.write(f"- Tags: {tags}\n")
            output.write(f"- Disposition: {disposition}\n\n")
            output.write("```k\n")
            output.write(item.text)
            output.write("\n```\n\n")

    print(f"OUTPUT={args.output}")
    print(f"TOTAL_ITEMS={len(items)}")
    print(f"SOURCE_SET_SHA256={source_digest.hexdigest()}")
    print("TAG_COUNTS=" + ",".join(f"{key}:{tag_counts[key]}" for key in sorted(tag_counts)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
