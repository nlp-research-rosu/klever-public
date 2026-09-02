#!/usr/bin/env python3
"""Emit a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


START = re.compile(r"^\s{2}(syntax|rule|claim|configuration|context|alias)\b")
BOUNDARY = re.compile(
    r"^\s{2}(?:syntax|rule|claim|configuration|context|alias|endmodule|module|imports)\b"
)
ATTRS = [
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "symbol",
    "no-evaluators",
    "macro",
    "macro-rec",
]


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for i in starts:
        end = i + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        yield i + 1, lines[i:end]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    paths: list[Path] = []
    for root in args.paths:
        if root.is_dir():
            paths.extend(sorted(root.glob("*.k")))
        else:
            paths.append(root)
    paths = sorted(dict.fromkeys(path.resolve() for path in paths))

    grand = collections.Counter()
    print("# Exhaustive K declaration inventory")
    print()
    print("Each numbered entry is one top-level local declaration. Continuation")
    print("lines, guards, cells, and attributes are included in its code block.")
    print()
    print("## Per-file counts")
    print()
    print("| File | Syntax | Rules | Claims | Configs | Contexts | Attributes |")
    print("|---|---:|---:|---:|---:|---:|---|")
    cached = {}
    for path in paths:
        items = list(blocks(path))
        cached[path] = items
        kinds = collections.Counter(item[1][0].strip().split(None, 1)[0] for item in items)
        text = path.read_text(encoding="utf-8")
        attrs = {name: len(re.findall(rf"\b{re.escape(name)}\b", text)) for name in ATTRS}
        grand.update(kinds)
        attr_text = ", ".join(f"{name}={count}" for name, count in attrs.items() if count)
        print(
            f"| `{path}` | {kinds['syntax']} | {kinds['rule']} | {kinds['claim']} "
            f"| {kinds['configuration']} | {kinds['context']} | {attr_text or 'none'} |"
        )

    print()
    print("## Grand declaration counts")
    print()
    for kind in ("syntax", "rule", "claim", "configuration", "context", "alias"):
        print(f"- {kind}: {grand[kind]}")

    serial = 0
    for path in paths:
        print()
        print(f"## {path}")
        for line_no, body in cached[path]:
            serial += 1
            kind = body[0].strip().split(None, 1)[0]
            body_text = "\n".join(body)
            present = [name for name in ATTRS if re.search(rf"\b{re.escape(name)}\b", body_text)]
            print()
            print(
                f"### INV-{serial:04d} — {kind} at `{path}:{line_no}`"
                + (f" — attributes: {', '.join(present)}" if present else "")
            )
            print()
            print("```k")
            print(body_text)
            print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
