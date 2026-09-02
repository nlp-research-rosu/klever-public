#!/usr/bin/env python3
"""Emit an exhaustive line-addressable inventory of local K declarations."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


roots = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

declaration = re.compile(
    r"^(?:(requires|module|endmodule)\b|  "
    r"(imports|configuration|syntax|context|rule|claim|alias|macro)\b)"
)


def classify(path: Path, line: int, kind: str, block: str) -> str:
    if path == Path("/candidate/spec.k") and kind == "claim":
        return "candidate_reachability_claim"
    if path == Path("/candidate/verification.k"):
        if kind == "rule" and line >= 107:
            return "candidate_operational_bridge"
        if kind == "rule":
            return "candidate_function_equation"
        if kind == "syntax":
            if "function" in block:
                return "candidate_function_declaration"
            return "candidate_syntax_declaration"
    if str(path).startswith("/reference/reference-semantics"):
        if kind == "rule":
            return "supplied_fixed_semantics_rule"
        if kind == "syntax":
            attrs = set(re.findall(r"\b(?:function|functional|total|macro(?:-rec)?|"
                                   r"no-evaluators|concrete|owise|priority)\b", block))
            if "function" in attrs:
                return "supplied_function_declaration"
            return "supplied_syntax_declaration"
        if kind == "context":
            return "supplied_evaluation_context"
        if kind == "configuration":
            return "supplied_configuration"
        return "supplied_structure"
    return "other"


records = []
for path in roots:
    lines = path.read_text().splitlines()
    starts = []
    for index, text in enumerate(lines):
        match = declaration.match(text)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:end]).rstrip()
        # Comments between declarations belong to neither declaration.
        while "\n//" in block:
            block = block[: block.rfind("\n//")].rstrip()
        attributes = sorted(
            set(
                re.findall(
                    r"\b(?:function|functional|total|simplification|macro(?:-rec)?|"
                    r"no-evaluators|concrete|owise|anywhere|priority(?:\(\d+\))?)\b",
                    block,
                )
            )
        )
        normalized = re.sub(r"\s+", " ", block).strip()
        records.append(
            {
                "file": str(path),
                "line": start + 1,
                "kind": kind,
                "classification": classify(path, start + 1, kind, block),
                "attributes": ",".join(attributes) if attributes else "-",
                "sha12": hashlib.sha256(block.encode()).hexdigest()[:12],
                "text": normalized,
            }
        )

print("id\tfile\tline\tkind\tclassification\tattributes\tsha12\tdeclaration")
for identifier, record in enumerate(records, 1):
    print(
        f"{identifier}\t{record['file']}\t{record['line']}\t{record['kind']}\t"
        f"{record['classification']}\t{record['attributes']}\t"
        f"{record['sha12']}\t{record['text']}"
    )

counts = collections.Counter(record["classification"] for record in records)
kind_counts = collections.Counter(record["kind"] for record in records)
print("SUMMARY")
print(f"records={len(records)}")
for key, count in sorted(kind_counts.items()):
    print(f"kind.{key}={count}")
for key, count in sorted(counts.items()):
    print(f"classification.{key}={count}")
