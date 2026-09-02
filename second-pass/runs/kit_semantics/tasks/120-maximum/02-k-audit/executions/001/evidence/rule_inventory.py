#!/usr/bin/env python3
"""Exhaustive source-level declaration inventory for the submitted K theory."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-source")
OUTPUT = Path("/audit-output/evidence/rule-inventory.txt")
TOP_LEVEL = re.compile(r"^(requires|module|endmodule)\b")
MODULE_LEVEL = re.compile(
    r"^(\s{1,4})(imports|configuration|"
    r"syntax(?:\s+priorit(?:y|ies))?|context(?:\s+alias)?|"
    r"rule|claim|alias|macro)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "concrete",
    "simplification",
    "macro",
    "alias",
    "strict",
    "seqstrict",
)


def source_files() -> list[Path]:
    semantics = sorted((ROOT / "reference-semantics").rglob("*.k"))
    return semantics + [ROOT / "verification.k"]


def declarations(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        top_match = TOP_LEVEL.match(line)
        module_match = MODULE_LEVEL.match(line)
        if top_match:
            starts.append((index, top_match.group(1)))
        elif module_match:
            starts.append((index, module_match.group(2)))
    result: list[tuple[int, str, str]] = []
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        result.append((index + 1, kind, "\n".join(block_lines)))
    return result


def classify(kind: str, block: str) -> str:
    if kind.startswith("syntax"):
        flags = [name for name in ATTRIBUTES if re.search(rf"\b{re.escape(name)}\b", block)]
        return "syntax" + (f"[{','.join(flags)}]" if flags else "")
    if kind == "rule":
        flags = [name for name in ATTRIBUTES if re.search(rf"\b{re.escape(name)}\b", block)]
        if "<k>" in block or any(
            cell in block
            for cell in (
                "<env>",
                "<scopes>",
                "<heap>",
                "<stack>",
                "<ret>",
                "<exc>",
                "<exit-code>",
            )
        ):
            base = "operational-rule"
        else:
            base = "equational-rule"
        return base + (f"[{','.join(flags)}]" if flags else "")
    return kind


def main() -> None:
    counts: Counter[str] = Counter()
    attribute_counts: Counter[str] = Counter()
    file_counts: dict[str, Counter[str]] = {}
    blocks: list[str] = []
    for path in source_files():
        relative = path.relative_to(ROOT).as_posix()
        per_file: Counter[str] = Counter()
        for line, kind, block in declarations(path):
            category = classify(kind, block)
            counts[category] += 1
            per_file[category] += 1
            for attribute in ATTRIBUTES:
                if re.search(rf"\b{re.escape(attribute)}\b", block):
                    attribute_counts[attribute] += 1
            blocks.append(
                f"\n=== {relative}:{line} | {category} ===\n{block}\n"
            )
        file_counts[relative] = per_file

    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write("K THEORY DECLARATION INVENTORY\n")
        stream.write(f"source_files={len(source_files())}\n")
        stream.write(f"declaration_blocks={sum(counts.values())}\n")
        stream.write("\nCATEGORY COUNTS\n")
        for key, value in sorted(counts.items()):
            stream.write(f"{key}: {value}\n")
        stream.write("\nATTRIBUTE-BEARING BLOCK COUNTS\n")
        for key, value in sorted(attribute_counts.items()):
            stream.write(f"{key}: {value}\n")
        stream.write("\nPER-FILE COUNTS\n")
        for relative, per_file in file_counts.items():
            rendered = ", ".join(f"{key}={value}" for key, value in sorted(per_file.items()))
            stream.write(f"{relative}: {rendered}\n")
        stream.write("\nDECLARATION BLOCKS\n")
        stream.writelines(blocks)

    print(f"output={OUTPUT}")
    print(f"source_files={len(source_files())}")
    print(f"declaration_blocks={sum(counts.values())}")
    print(f"rules={sum(value for key, value in counts.items() if 'rule' in key)}")
    print(f"syntax={sum(value for key, value in counts.items() if key.startswith('syntax'))}")
    print(f"contexts={sum(value for key, value in counts.items() if key.startswith('context'))}")
    print(f"claims={counts['claim']}")
    print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
    print("RULE_INVENTORY_CREATED")


if __name__ == "__main__":
    main()
