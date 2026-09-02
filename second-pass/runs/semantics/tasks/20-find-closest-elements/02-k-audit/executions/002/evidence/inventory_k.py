#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory for the selected K theory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


REFERENCE_ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
OUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")
START = re.compile(
    r"^(?:requires\b|module\b|endmodule\b| {2}"
    r"(?:imports|configuration|syntax|context|rule|claim)\b)"
)
MATERIAL_BASELINE = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/operators.k",
    "semantics/int.k",
    "semantics/float.k",
    "semantics/list.k",
    "semantics/tuple.k",
    "semantics/subscript.k",
    "semantics/controls.k",
    "semantics/functions.k",
    "semantics/builtins.k",
    "semantics/call.k",
    "semantics/str.k",
}
FLAGS = [
    "function",
    "functional",
    "total",
    "macro",
    "macro-rec",
    "simplification",
    "concrete",
    "no-evaluators",
    "symbol",
    "priority",
    "owise",
    "strict",
    "seqstrict",
    "hook",
]


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if START.match(line):
            starts.append((index, line.strip().split()[0]))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:end]).rstrip()
        yield index + 1, kind, block


def origin_and_relative(path: Path) -> tuple[str, str, str]:
    if path.is_relative_to(REFERENCE_ROOT):
        relative = path.relative_to(REFERENCE_ROOT).as_posix()
        materiality = (
            "baseline_material"
            if relative in MATERIAL_BASELINE
            else "baseline_unused_by_submitted_program"
        )
        return "trusted_supplied_semantics", relative, materiality
    if path.name == "verification.k":
        return "candidate", path.name, "proof_local"
    return "candidate", path.name, "target_spec"


def disposition(origin: str, materiality: str, kind: str) -> str:
    if origin == "trusted_supplied_semantics":
        if materiality == "baseline_material":
            return (
                "FIXED_BASELINE; candidate-unaltered; material subset mapped and "
                "reviewed in REVIEW.md"
            )
        return "FIXED_BASELINE; candidate-unaltered; construct unused by submitted program"
    if materiality == "target_spec":
        return "TARGET_CLAIM; adequacy and non-vacuity reviewed in REVIEW.md"
    if kind in {"rule", "syntax", "context", "configuration"}:
        return "PROOF_LOCAL_EXTENSION; individual disposition in REVIEW.md"
    return "PROOF_LOCAL_MODULE_STRUCTURE"


def main() -> int:
    paths = sorted(REFERENCE_ROOT.rglob("*.k")) + CANDIDATE_FILES
    rows: list[list[str]] = []
    kind_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    flag_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    file_counts: collections.Counter[str] = collections.Counter()

    for path in paths:
        origin, relative, materiality = origin_and_relative(path)
        for line, kind, block in blocks(path):
            attribute_regions = " ".join(re.findall(r"\[[^\]]*\]", block)).lower()
            attribute_words = set(re.findall(r"[a-z][a-z0-9-]*", attribute_regions))
            flags = [flag for flag in FLAGS if flag in attribute_words]
            compact = " ".join(block.split())
            escaped = block.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")
            rows.append(
                [
                    origin,
                    relative,
                    str(line),
                    kind,
                    materiality,
                    ",".join(flags),
                    disposition(origin, materiality, kind),
                    compact[:500],
                    escaped,
                ]
            )
            kind_counts[(origin, kind)] += 1
            file_counts[f"{origin}:{relative}"] += 1
            for flag in flags:
                flag_counts[(origin, flag)] += 1

    header = [
        "origin",
        "file",
        "line",
        "kind",
        "materiality",
        "attributes",
        "disposition",
        "compact_declaration",
        "full_block_escaped",
    ]
    with OUT.open("w", encoding="utf-8") as stream:
        stream.write("\t".join(header) + "\n")
        for row in rows:
            stream.write("\t".join(row) + "\n")

    with SUMMARY.open("w", encoding="utf-8") as stream:
        stream.write(f"inventory_file={OUT}\n")
        stream.write(f"source_file_count={len(paths)}\n")
        stream.write(f"declaration_block_count={len(rows)}\n")
        stream.write("kind_counts:\n")
        for key, value in sorted(kind_counts.items()):
            stream.write(f"  {key[0]} {key[1]} {value}\n")
        stream.write("attribute_counts:\n")
        for key, value in sorted(flag_counts.items()):
            stream.write(f"  {key[0]} {key[1]} {value}\n")
        stream.write("file_counts:\n")
        for key, value in sorted(file_counts.items()):
            stream.write(f"  {key} {value}\n")

    print(SUMMARY.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
