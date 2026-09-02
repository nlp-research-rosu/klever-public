#!/usr/bin/env python3
"""Sentence-level exhaustive inventory for the submitted K sources."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/82/reference-semantics"),
    Path("/tmp/audit-work/82/verification.k"),
    Path("/tmp/audit-work/82/spec.k"),
]
START = re.compile(
    r"^(?:(requires)\b|\s*(module|endmodule|imports|syntax|configuration|"
    r"context|rule|claim|alias|macro)\b)"
)


def source_files() -> list[Path]:
    result: list[Path] = []
    for root in ROOTS:
        if root.is_dir():
            result.extend(sorted(root.rglob("*.k")))
        else:
            result.append(root)
    return sorted(result)


def classify(kind: str, text: str) -> tuple[str, str]:
    attrs: list[str] = []
    for attr in (
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "owise",
        "priority",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
        "symbol",
        "no-evaluators",
    ):
        if re.search(rf"\b{re.escape(attr)}\b", text):
            attrs.append(attr)
    if kind == "rule":
        if "simplification" in attrs:
            category = "simplification-rule"
        elif "concrete" in attrs:
            category = "concrete-rule"
        elif "priority" in attrs:
            category = "priority-rule"
        elif "macro" in attrs or "macro-rec" in attrs:
            category = "macro-rule"
        elif "owise" in attrs:
            category = "owise-rule"
        else:
            category = "ordinary-rule"
    elif kind == "syntax":
        if "function" in attrs:
            category = "function-declaration"
        elif "macro" in attrs or "macro-rec" in attrs:
            category = "macro-declaration"
        else:
            category = "syntax-declaration"
    else:
        category = kind
    return category, ",".join(attrs) if attrs else "-"


counts: collections.Counter[str] = collections.Counter()
for path in source_files():
    if path.is_symlink():
        print(f"ERROR\tsymlink\t{path}")
        sys.exit(2)
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            starts.append((lineno, match.group(1) or match.group(2)))
    for index, (start, kind) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start - 1 : end])
        # Drop blank/comment-only tails which belong conceptually before the next sentence.
        block_lines = block.splitlines()
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
            end -= 1
        normalized_parts: list[str] = []
        for piece in block_lines:
            if not piece.strip() or piece.lstrip().startswith("//"):
                continue
            code = piece.split("//", 1)[0].strip()
            if code:
                normalized_parts.append(code)
        normalized = " ".join(normalized_parts)
        category, attrs = classify(kind, normalized)
        counts[category] += 1
        rel = path.as_posix().replace("/tmp/audit-work/82/", "")
        print(
            f"ITEM\t{rel}\t{start}-{end}\t{kind}\t{category}\t{attrs}\t{normalized}"
        )

print("COUNTS")
for category, count in sorted(counts.items()):
    print(f"COUNT\t{category}\t{count}")
