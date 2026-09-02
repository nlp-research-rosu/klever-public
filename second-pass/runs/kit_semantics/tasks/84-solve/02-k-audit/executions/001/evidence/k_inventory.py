#!/usr/bin/env python3
"""Emit an exhaustive declaration inventory for all K sources in this audit."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/84-solve")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
    ROOT / "bridge-verification.k",
    ROOT / "bridge-spec.k",
]

START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context alias|context|priority)\b"
)
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().replace("\t", " ")


def classify(kind: str, block: str) -> str:
    if kind == "configuration":
        return "configuration"
    if kind == "syntax":
        attribute_text = " ".join(re.findall(r"\[[^\]\n]*\]", block))
        flags = []
        for flag in (
            "function",
            "functional",
            "total",
            "macro-rec",
            "macro",
            "no-evaluators",
            "symbol",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(flag)}\b", attribute_text):
                flags.append(flag)
        return "syntax" + (":" + ",".join(flags) if flags else "")
    if kind in {"context", "context alias"}:
        return kind
    if kind == "priority":
        return "priority-declaration"
    if kind == "claim":
        return "reachability-claim"
    if "[simplification" in block:
        return "simplification-rule"
    if "[macro" in block:
        return "macro-rule"
    if "<k>" in block:
        return "operational-rule"
    return "equational-rule"


def disposition(path: Path, line: int, classification: str) -> str:
    relative = str(path.relative_to(ROOT))
    if relative.startswith("reference-semantics/"):
        return "FIXED_SUPPLIED_SEMANTICS"
    if relative == "verification.k":
        if line == 10:
            return "ACCEPT_EXACT_PROGRAM_AST"
        if line in {100, 103}:
            return "ACCEPT_PROVED_INTEGER_EQUALITY"
        if line >= 108:
            return "ACCEPT_TRUTHFUL_POSTCONDITION_DEFINITION"
        return "REVIEWED_PROOF_LOCAL"
    if relative in {"spec.k", "bridge-spec.k"}:
        return "CLAIM_REVIEWED_SEPARATELY"
    return "IMPORT_ONLY"


def main() -> None:
    rows = []
    counts: collections.Counter[str] = collections.Counter()
    attribute_counts: collections.Counter[str] = collections.Counter()
    file_counts: collections.Counter[str] = collections.Counter()
    opaque_rows = []

    for path in SOURCES:
        lines = path.read_text(encoding="utf-8").splitlines()
        module = "(outside-module)"
        modules_by_line = {}
        for number, line in enumerate(lines, start=1):
            match = MODULE.match(line)
            if match:
                module = match.group(1)
            modules_by_line[number] = module

        starts = [
            (index, START.match(line).group(1))
            for index, line in enumerate(lines)
            if START.match(line)
        ]
        for ordinal, (index, kind) in enumerate(starts):
            end = starts[ordinal + 1][0] if ordinal + 1 < len(starts) else len(lines)
            block_lines = lines[index:end]
            while block_lines and (
                block_lines[-1].strip() == ""
                or block_lines[-1].lstrip().startswith("//")
                or block_lines[-1].strip() == "endmodule"
            ):
                block_lines.pop()
            block = "\n".join(block_lines)
            summary = clean(block)
            digest = hashlib.sha256(block.encode("utf-8")).hexdigest()[:16]
            classification = classify(kind, block)
            relative = str(path.relative_to(ROOT))
            line_number = index + 1
            row = (
                relative,
                str(line_number),
                modules_by_line[line_number],
                kind,
                classification,
                disposition(path, line_number, classification),
                digest,
                summary,
            )
            rows.append(row)
            counts[classification] += 1
            file_counts[relative] += 1
            attribute_text = " ".join(re.findall(r"\[[^\]\n]*\]", block))
            for attribute in (
                "function",
                "functional",
                "total",
                "no-evaluators",
                "priority",
                "simplification",
                "owise",
                "concrete",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
            ):
                if re.search(rf"\b{re.escape(attribute)}\b", attribute_text):
                    attribute_counts[attribute] += 1
            if "no-evaluators" in classification:
                opaque_rows.append(f"{relative}:{line_number} {summary}")

    print(
        "\t".join(
            (
                "file",
                "line",
                "module",
                "kind",
                "classification",
                "audit_disposition",
                "block_sha256_16",
                "normalized_declaration",
            )
        )
    )
    for row in rows:
        print("\t".join(row))

    summary_path = Path("/audit-output/evidence/rule-inventory-summary.txt")
    with summary_path.open("w", encoding="utf-8") as stream:
        stream.write(f"source_files={len(SOURCES)}\n")
        stream.write(f"declarations={len(rows)}\n")
        for key, value in sorted(counts.items()):
            stream.write(f"classification[{key}]={value}\n")
        for key, value in sorted(attribute_counts.items()):
            stream.write(f"attribute_blocks[{key}]={value}\n")
        for key, value in sorted(file_counts.items()):
            stream.write(f"file[{key}]={value}\n")
        stream.write(f"no_evaluators_declarations={len(opaque_rows)}\n")
        for row in opaque_rows:
            stream.write(f"opaque_boundary={row}\n")


if __name__ == "__main__":
    main()
