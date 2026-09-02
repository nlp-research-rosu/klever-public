#!/usr/bin/env python3
"""Produce a line-addressed inventory of declarations in K source files."""

from __future__ import annotations

import collections
import hashlib
import re
import sys
from pathlib import Path


START = re.compile(
    r"^(requires)\b|^\s*(module|endmodule|imports|configuration|syntax|rule|claim|context|alias|macro)\b"
)


def sources(arguments: list[str]) -> list[Path]:
    result: list[Path] = []
    for argument in arguments:
        path = Path(argument)
        if path.is_dir():
            result.extend(sorted(path.rglob("*.k")))
        else:
            result.append(path)
    return sorted(dict.fromkeys(result), key=lambda item: str(item))


def clean(block: list[str]) -> str:
    parts: list[str] = []
    in_block_comment = False
    for raw in block:
        line = raw
        while True:
            if in_block_comment:
                end = line.find("*/")
                if end < 0:
                    line = ""
                    break
                line = line[end + 2 :]
                in_block_comment = False
            start = line.find("/*")
            slash = line.find("//")
            if slash >= 0 and (start < 0 or slash < start):
                line = line[:slash]
                break
            if start < 0:
                break
            end = line.find("*/", start + 2)
            if end < 0:
                line = line[:start]
                in_block_comment = True
                break
            line = line[:start] + " " + line[end + 2 :]
        if line.strip():
            parts.append(line.strip())
    return " ".join(" ".join(parts).split())


def classify(kind: str, text: str) -> str:
    tags: list[str] = []
    if kind == "syntax":
        for tag in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "macro",
            "token",
            "assoc",
            "comm",
            "unit",
            "hook",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"(?:\b|\[|,){re.escape(tag)}(?:\b|\(|,|\])", text):
                tags.append(tag)
        if "no-evaluators" in tags:
            tags.append("opaque")
    elif kind == "rule":
        priority = re.search(r"priority\((\d+)\)", text)
        if priority:
            tags.append(f"priority={priority.group(1)}")
        for tag in ("simplification", "concrete", "owise", "macro", "anywhere", "cool", "heat"):
            if re.search(rf"\b{tag}\b", text):
                tags.append(tag)
        if not tags:
            tags.append("ordinary")
    elif kind == "claim":
        label = re.search(r"claim\s*\[([^\]]+)\]", text)
        tags.append(f"label={label.group(1)}" if label else "unlabeled")
    return ",".join(tags) if tags else "-"


def main() -> int:
    paths = sources(sys.argv[1:])
    if not paths:
        print(f"usage: {sys.argv[0]} K_FILE_OR_DIRECTORY [...]", file=sys.stderr)
        return 64
    totals: collections.Counter[str] = collections.Counter()
    tag_totals: collections.Counter[str] = collections.Counter()
    all_entries: list[tuple[Path, int, str, str, str]] = []
    print(f"FILES: {len(paths)}")
    for path in paths:
        data = path.read_bytes()
        lines = data.decode("utf-8").splitlines()
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = START.match(line)
            if match:
                starts.append((index, match.group(1) or match.group(2)))
        file_counts: collections.Counter[str] = collections.Counter()
        for position, (index, kind) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            text = clean(lines[index:end])
            tags = classify(kind, text)
            all_entries.append((path, index + 1, kind, tags, text))
            file_counts[kind] += 1
            totals[kind] += 1
            for tag in tags.split(","):
                if tag != "-":
                    tag_totals[f"{kind}:{tag}"] += 1
        digest = hashlib.sha256(data).hexdigest()
        print(
            f"FILE {path} sha256={digest} lines={len(lines)} declarations={sum(file_counts.values())} counts={dict(sorted(file_counts.items()))}"
        )
    print(f"TOTAL_DECLARATIONS: {len(all_entries)}")
    print(f"KIND_COUNTS: {dict(sorted(totals.items()))}")
    print(f"TAG_COUNTS: {dict(sorted(tag_totals.items()))}")
    print("BEGIN_INVENTORY")
    for path, line, kind, tags, declaration in all_entries:
        print(f"{path}:{line}: {kind} [{tags}] {declaration}")
    print("END_INVENTORY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
