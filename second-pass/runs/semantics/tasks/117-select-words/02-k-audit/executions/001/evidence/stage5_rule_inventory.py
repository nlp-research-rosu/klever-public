#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


roots = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

start_re = re.compile(
    r"^\s*(module|endmodule|imports|syntax|configuration|context|"
    r"rule|claim|alias)\b"
)
record_re = re.compile(
    r"^\s*(syntax|configuration|context|rule|claim|alias)\b"
)


def classify(kind: str, text: str) -> str:
    tags: list[str] = []
    if kind == "syntax":
        for tag in (
            "function",
            "total",
            "functional",
            "macro",
            "symbol",
            "no-evaluators",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(tag)}\b", text):
                tags.append(tag)
        if "symbol" in tags or "no-evaluators" in tags:
            tags.append("opaque-symbol-boundary")
        elif "function" in tags:
            tags.append("equational-function")
        else:
            tags.append("constructor/syntax")
    elif kind == "rule":
        if "simplification" in text:
            tags.append("simplification")
        if "priority" in text:
            match = re.search(r"priority\((\d+)\)", text)
            tags.append(f"priority={match.group(1) if match else '?'}")
        if "owise" in text:
            tags.append("owise")
        if "macro" in text:
            tags.append("macro-expansion")
        if "<k>" in text or re.search(r"<[A-Za-z][^>]*>", text):
            tags.append("operational")
        else:
            tags.append("equational")
        if not any(
            tag in tags
            for tag in ("simplification", "macro-expansion", "operational")
        ):
            tags.append("ordinary-rule")
    elif kind == "claim":
        tags.append("reachability-claim")
        if "circularity" in text:
            tags.append("circularity")
        if "depends" in text:
            tags.append("depends")
    elif kind == "context":
        tags.append("evaluation-context")
    elif kind == "configuration":
        tags.append("configuration")
    return ",".join(tags) if tags else "declaration"


counts: Counter[str] = Counter()
records: list[tuple[Path, int, str, str, str]] = []
for path in roots:
    lines = path.read_text().splitlines()
    starts = [
        (index, record_re.match(line))
        for index, line in enumerate(lines)
        if record_re.match(line)
    ]
    for index, match in starts:
        assert match is not None
        kind = match.group(1)
        end = index + 1
        while end < len(lines):
            if start_re.match(lines[end]):
                break
            end += 1
        text = " ".join(
            part.strip()
            for part in lines[index:end]
            if part.strip() and not part.lstrip().startswith("//")
        )
        category = classify(kind, text)
        counts[kind] += 1
        records.append((path, index + 1, kind, category, text))

print(f"source_file_count={len(roots)}")
print(f"record_count={len(records)}")
print(
    "counts="
    + ",".join(f"{key}:{counts[key]}" for key in sorted(counts))
)
for path, line, kind, category, text in records:
    print(f"{path}:{line}\t{kind}\t{category}\t{text}")
