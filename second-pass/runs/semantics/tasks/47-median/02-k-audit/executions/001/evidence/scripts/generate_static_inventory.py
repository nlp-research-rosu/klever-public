#!/usr/bin/env python3
"""Create a complete declaration/rule inventory for the audited K source tree."""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path


START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
ENDMODULE = re.compile(r"^\s*endmodule\b")
ATTRIBUTES = {
    "function": re.compile(r"\bfunction\b"),
    "functional": re.compile(r"\bfunctional\b"),
    "total": re.compile(r"\btotal\b"),
    "symbol": re.compile(r"\bsymbol\s*\("),
    "no-evaluators": re.compile(r"\bno-evaluators\b"),
    "priority": re.compile(r"\bpriority\s*\("),
    "simplification": re.compile(r"\bsimplification\b"),
    "concrete": re.compile(r"\bconcrete\b"),
    "owise": re.compile(r"\bowise\b"),
    "macro": re.compile(r"\bmacro(?:-rec)?\b"),
    "strict": re.compile(r"\b(?:seq)?strict(?:\s*\(|\b)"),
}


def blocks(lines: list[str]):
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for ordinal, start in enumerate(starts):
        next_start = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        stop = next_start
        for index in range(start + 1, next_start):
            if ENDMODULE.match(lines[index]):
                stop = index
                break
        while stop > start + 1 and (
            not lines[stop - 1].strip() or lines[stop - 1].lstrip().startswith("//")
        ):
            stop -= 1
        match = START.match(lines[start])
        assert match is not None
        yield match.group(1), start + 1, "".join(lines[start:stop]).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    files = [args.root / "reference-semantics" / "semantics.k"]
    files.extend(sorted((args.root / "reference-semantics" / "semantics").glob("*.k")))
    files.extend([args.root / "verification.k", args.root / "spec.k"])

    rendered = [
        "# Exhaustive K source inventory",
        "",
        "Generated directly from the fresh scratch source copy. Every local `syntax`,",
        "`configuration`, `context`, `rule`, and `claim` entry is listed with its",
        "complete source block and attributes. Imported K builtins are outside this",
        "local-source inventory.",
        "",
    ]
    aggregate = Counter()
    per_file: list[tuple[str, Counter, str, int]] = []
    all_blocks = {}

    for path in files:
        relative = str(path.relative_to(args.root))
        content = path.read_bytes()
        lines = content.decode("utf-8").splitlines(keepends=True)
        entries = list(blocks(lines))
        counts = Counter(kind for kind, _, _ in entries)
        for _, _, block in entries:
            for attribute, pattern in ATTRIBUTES.items():
                if pattern.search(block):
                    counts[f"attr:{attribute}"] += 1
        counts["opaque-declaration"] = sum(
            1
            for kind, _, block in entries
            if kind == "syntax"
            and ATTRIBUTES["symbol"].search(block)
            and ATTRIBUTES["no-evaluators"].search(block)
        )
        aggregate.update(counts)
        digest = hashlib.sha256(content).hexdigest()
        per_file.append((relative, counts, digest, len(lines)))
        all_blocks[relative] = entries

    rendered.extend(
        [
            "## Summary",
            "",
            "| File | Lines | SHA-256 | Syntax | Config | Context | Rules | Claims | Function | Total | Functional | Opaque | Priority | Simplification | Concrete |",
            "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for relative, counts, digest, line_count in per_file:
        rendered.append(
            f"| `{relative}` | {line_count} | `{digest}` | {counts['syntax']} | "
            f"{counts['configuration']} | {counts['context']} | {counts['rule']} | "
            f"{counts['claim']} | {counts['attr:function']} | {counts['attr:total']} | "
            f"{counts['attr:functional']} | {counts['opaque-declaration']} | "
            f"{counts['attr:priority']} | {counts['attr:simplification']} | "
            f"{counts['attr:concrete']} |"
        )

    rendered.extend(
        [
            "",
            f"Aggregate local entries: **{sum(aggregate[k] for k in ('syntax', 'configuration', 'context', 'rule', 'claim'))}** "
            f"({aggregate['syntax']} syntax, {aggregate['configuration']} configuration, "
            f"{aggregate['context']} context, {aggregate['rule']} rule, {aggregate['claim']} claim).",
            "",
            "## Complete inventory",
            "",
        ]
    )

    for relative, _, _, _ in per_file:
        rendered.extend([f"### `{relative}`", ""])
        entries = all_blocks[relative]
        if not entries:
            rendered.extend(["No local declaration or rule entries.", ""])
            continue
        for kind, line_number, block in entries:
            tags = [
                attribute
                for attribute, pattern in ATTRIBUTES.items()
                if pattern.search(block)
            ]
            if (
                kind == "syntax"
                and "symbol" in tags
                and "no-evaluators" in tags
            ):
                tags.append("opaque-declaration")
            rendered.append(
                f"- **{kind} at line {line_number}**"
                + (f" — tags: {', '.join(tags)}" if tags else "")
            )
            rendered.extend(["", "```k", block, "```", ""])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(rendered) + "\n", encoding="utf-8")
    print(f"output={args.output}")
    print(
        "aggregate="
        + ",".join(
            f"{key}:{aggregate[key]}"
            for key in (
                "syntax",
                "configuration",
                "context",
                "rule",
                "claim",
                "attr:function",
                "attr:total",
                "attr:functional",
                "opaque-declaration",
                "attr:priority",
                "attr:simplification",
                "attr:concrete",
            )
        )
    )
    print(f"file_count={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
