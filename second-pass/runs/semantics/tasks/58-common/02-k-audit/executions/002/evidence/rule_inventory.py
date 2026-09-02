#!/usr/bin/env python3
"""Produce a line-addressed inventory of every K declaration and rule in scope."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SEMANTICS = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
START = re.compile(
    r"^(?:(requires|module|endmodule)\b|  (imports|configuration|syntax|context|rule|claim|priority)\b)"
)
DECLARATIONS = {"configuration", "syntax", "context", "rule", "claim", "priority"}
ATTRIBUTES = (
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
)


def clean(lines: list[str]) -> str:
    pieces: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if "//" in stripped:
            stripped = stripped.split("//", 1)[0].rstrip()
        pieces.append(stripped)
    return " ".join(pieces)


def records(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (index, kind) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = clean(lines[index:next_index])
        yield kind, index + 1, text


def main() -> None:
    files = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
    files.extend(CANDIDATE_FILES)
    global_counts: collections.Counter[str] = collections.Counter()
    attribute_counts: collections.Counter[str] = collections.Counter()

    for path in files:
        rel = str(path)
        print(f"\n=== {rel} ===")
        local_counts: collections.Counter[str] = collections.Counter()
        for kind, line, text in records(path):
            local_counts[kind] += 1
            global_counts[kind] += 1
            if kind in DECLARATIONS:
                tags = [
                    attribute
                    for attribute in ATTRIBUTES
                    if re.search(
                        rf"(?<![A-Za-z0-9_-]){re.escape(attribute)}(?:\b|\()",
                        text,
                    )
                ]
                for tag in tags:
                    attribute_counts[tag] += 1
                tag_text = ",".join(tags) if tags else "-"
                print(f"{rel}:{line}: kind={kind}; attrs={tag_text}; {text}")
        print(f"FILE_COUNTS {rel} {dict(sorted(local_counts.items()))}")

    print("\n=== GLOBAL COUNTS ===")
    print(dict(sorted(global_counts.items())))
    print("ATTRIBUTE-BEARING-DECLARATION COUNTS")
    print(dict(sorted(attribute_counts.items())))


if __name__ == "__main__":
    main()
