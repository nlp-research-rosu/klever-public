#!/usr/bin/env python3
"""Exhaustive source-level inventory of K declarations and rules in audit scope."""

from __future__ import annotations

import collections
import re
from pathlib import Path


REFERENCE_ROOT = Path("/reference/reference-semantics")
EXTRA_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
OUTPUT = Path("/audit-output/evidence/rule-inventory.txt")

START = re.compile(
    r"^(?:requires\b|module\b|endmodule\b|"
    r"  (?:imports\b|syntax\b|configuration\b|context\b|rule\b|claim\b))"
)


def kind_of(text: str) -> str:
    stripped = text.lstrip()
    for kind in (
        "requires",
        "module",
        "endmodule",
        "imports",
        "syntax",
        "configuration",
        "context",
        "rule",
        "claim",
    ):
        if stripped.startswith(kind):
            return kind
    return "unknown"


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        chunk = lines[start:end]
        while chunk and (not chunk[-1].strip() or chunk[-1].lstrip().startswith("//")):
            chunk.pop()
        if not chunk:
            continue
        text = "\n".join(chunk)
        yield start + 1, kind_of(text), text


def normalize(text: str) -> str:
    content = []
    for line in text.splitlines():
        code = line.split("//", 1)[0].strip()
        if code:
            content.append(code)
    return " ".join(content)


def attributes(text: str) -> str:
    names = []
    for attribute_group in re.findall(r"\[([^\]]+)\]", text):
        for item in attribute_group.split(","):
            name = item.strip()
            if name:
                names.append(name)
    if "no-evaluators" in text and "no-evaluators" not in names:
        names.append("no-evaluators")
    return ",".join(names) if names else "-"


def main() -> int:
    files = sorted(REFERENCE_ROOT.rglob("*.k")) + EXTRA_FILES
    counts = collections.Counter()
    file_counts: dict[str, collections.Counter] = {}
    entries = []

    for path in files:
        relative = (
            "reference-semantics/" + path.relative_to(REFERENCE_ROOT).as_posix()
            if path.is_relative_to(REFERENCE_ROOT)
            else "candidate/" + path.name
        )
        local = collections.Counter()
        for line, kind, text in blocks(path):
            counts[kind] += 1
            local[kind] += 1
            entries.append((relative, line, kind, attributes(text), normalize(text)))
        file_counts[relative] = local

    output = []
    output.append("K SOURCE INVENTORY")
    output.append("==================")
    output.append(f"files={len(files)}")
    output.append("total_counts=" + " ".join(f"{key}:{counts[key]}" for key in sorted(counts)))
    output.append("")
    output.append("PER-FILE COUNTS")
    output.append("----------------")
    for relative in sorted(file_counts):
        local = file_counts[relative]
        output.append(
            relative + " " + " ".join(f"{key}:{local[key]}" for key in sorted(local))
        )
    output.append("")
    output.append("EVERY DECLARATION / RULE / CLAIM")
    output.append("--------------------------------")
    for relative, line, kind, attrs, text in entries:
        output.append(f"{relative}:{line}\t{kind}\tattrs={attrs}\t{text}")
    output.append("")

    OUTPUT.write_text("\n".join(output), encoding="utf-8")
    print(f"inventory={OUTPUT}")
    print(f"files={len(files)}")
    print("total_counts=" + " ".join(f"{key}:{counts[key]}" for key in sorted(counts)))
    for relative in sorted(file_counts):
        local = file_counts[relative]
        print(relative + " " + " ".join(f"{key}:{local[key]}" for key in sorted(local)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
