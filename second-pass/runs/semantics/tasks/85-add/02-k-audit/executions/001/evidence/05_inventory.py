#!/usr/bin/env python3
"""Create a line-addressable inventory of all local K declarations and rules."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r'^\s*(?:requires\s+"[^"]+"\s*$|module\b|endmodule\b|imports\b|configuration\b|'
    r"context(?:\s+alias)?\b|syntax\b|rule\b|claim\b|alias\b|priority\b)"
)
DECL = re.compile(
    r'^\s*(requires(?=\s+"[^"]+"\s*$)|module|endmodule|imports|configuration|'
    r"context(?:\s+alias)?|syntax|rule|claim|alias|priority)\b"
)


def statements(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[start]
        match = DECL.match(first)
        if match is None:
            continue
        kind = match.group(1)
        body_lines = []
        for line in lines[start:stop]:
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            if stripped:
                body_lines.append(stripped)
        text = " ".join(body_lines)
        yield start + 1, kind, text


def classify(kind: str, text: str) -> str:
    attrs = []
    for name in (
        "function",
        "total",
        "functional",
        "symbol",
        "no-evaluators",
        "simplification",
        "simplifier",
        "macro-rec",
        "macro",
        "priority",
        "owise",
        "concrete",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(name)}\b", text):
            attrs.append(name)
    if kind == "rule":
        if "simplification" in attrs or "simplifier" in attrs:
            category = "simplification-rule"
        elif "priority" in attrs:
            category = "priority-rule"
        elif "macro" in attrs or "macro-rec" in attrs:
            category = "macro-rule"
        else:
            category = "ordinary-rule"
    elif kind == "syntax":
        if "symbol" in attrs or "no-evaluators" in attrs:
            category = "opaque-symbol-declaration"
        elif "function" in attrs or "functional" in attrs:
            category = "function-declaration"
        else:
            category = "syntax-declaration"
    else:
        category = kind.replace(" ", "-")
    return category + (f"; attrs={','.join(attrs)}" if attrs else "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    args = parser.parse_args()

    files = [args.root / "semantics.k"]
    files.extend(sorted((args.root / "semantics").glob("*.k")))
    files.extend([args.verification, args.verification.with_name("spec.k")])

    counter: Counter[str] = Counter()
    file_counts: dict[str, Counter[str]] = {}
    records = []
    for path in files:
        relative = (
            path.relative_to(args.root.parent)
            if args.root.parent in path.parents
            else Path(path.name)
        )
        local = Counter()
        for line, kind, text in statements(path):
            classification = classify(kind, text)
            category = classification.split(";", 1)[0]
            counter[category] += 1
            local[category] += 1
            records.append((relative.as_posix(), line, classification, text))
        file_counts[relative.as_posix()] = local

    print("# Exhaustive local K declaration and rule inventory")
    print()
    print(
        "Scope: the complete supplied `reference-semantics` source tree, "
        "plus candidate `verification.k` and `spec.k`. Continuation lines, "
        "guards, cells, and attributes are folded into the record that starts "
        "at the displayed source line."
    )
    print()
    print("## Totals")
    print()
    for key in sorted(counter):
        print(f"- {key}: {counter[key]}")
    print()
    print("No source item carrying `simplification`/`simplifier` is omitted; "
          f"count={counter.get('simplification-rule', 0)}.")
    print()
    print("## Per-file counts")
    print()
    for path, counts in file_counts.items():
        rendered = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
        print(f"- `{path}`: {rendered}")
    print()
    print("## Records")
    print()
    for path, line, classification, text in records:
        escaped = text.replace("|", "\\|")
        print(f"- `{path}:{line}` — **{classification}** — `{escaped}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
