#!/usr/bin/env python3
"""Build a line-addressable inventory of K declarations and rules."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path

START = re.compile(
    r"^\s*(configuration|context(?:\s+alias)?|syntax|rule|claim|alias)\b"
)
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")
BOUNDARY = re.compile(
    r"^\s*(?:module\b|endmodule\b|imports\b|requires\b|"
    r"configuration\b|context(?:\s+alias)?\b|syntax\b|rule\b|claim\b|alias\b)"
)


def compact(lines: list[str]) -> str:
    code_lines = []
    for line in lines:
        code = line.split("//", 1)[0]
        if code.strip():
            code_lines.append(" ".join(code.strip().split()))
    return " ".join(code_lines).strip()


def classify(kind: str, text: str) -> str:
    tags: list[str] = []
    if kind == "syntax":
        tags.append("syntax-declaration")
    elif kind == "rule":
        tags.append("simplification-rule" if "simplification" in text else "ordinary-rule")
    else:
        tags.append(kind.replace(" ", "-"))
    for flag in (
        "function",
        "total",
        "functional",
        "no-evaluators",
        "opaque",
        "symbol",
        "priority",
        "macro",
        "anywhere",
        "owise",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", text):
            tags.append(flag)
    if "no-evaluators" in tags:
        tags.append("opaque-symbol")
    return ", ".join(tags)


def entries_for(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    module = "(outside-module)"
    i = 0
    while i < len(lines):
        module_match = MODULE.match(lines[i])
        if module_match:
            module = module_match.group(1)
        start = START.match(lines[i])
        if not start:
            i += 1
            continue
        kind = start.group(1)
        begin = i
        i += 1
        while i < len(lines) and not BOUNDARY.match(lines[i]):
            i += 1
        text = compact(lines[begin:i])
        yield {
            "file": path,
            "line": begin + 1,
            "module": module,
            "kind": kind,
            "classification": classify(kind, text),
            "text": text,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted(args.root.rglob("*.k")) + [args.verification]
    entries = [entry for path in paths for entry in entries_for(path)]
    counts = collections.Counter(entry["kind"] for entry in entries)
    class_counts = collections.Counter(
        tag.strip()
        for entry in entries
        for tag in entry["classification"].split(",")
    )

    out: list[str] = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated mechanically from the fresh scratch source copy. Each entry "
        "records the full declaration/rule text compacted to one line; source "
        "files and line numbers are authoritative.",
        "",
        f"- Files inventoried: {len(paths)}",
        f"- Total entries: {len(entries)}",
        f"- Kinds: {dict(sorted(counts.items()))}",
        f"- Class tags: {dict(sorted(class_counts.items()))}",
        "",
    ]
    grouped: dict[Path, list[dict]] = collections.defaultdict(list)
    for entry in entries:
        grouped[entry["file"]].append(entry)
    for path in paths:
        out.extend([f"## {path}", ""])
        for number, entry in enumerate(grouped[path], 1):
            out.append(
                f"{number}. L{entry['line']} · `{entry['module']}` · "
                f"**{entry['classification']}** — `{entry['text'].replace('`', chr(39))}`"
            )
        out.append("")

    args.output.write_text("\n".join(out), encoding="utf-8")
    print(f"FILES={len(paths)}")
    print(f"ENTRIES={len(entries)}")
    print(f"KINDS={dict(sorted(counts.items()))}")
    print(f"CLASS_TAGS={dict(sorted(class_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
