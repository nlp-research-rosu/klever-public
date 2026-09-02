#!/usr/bin/env python3
"""Lexical, exhaustive inventory of local K source constructs."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
CANDIDATE_ROOT = Path("/candidate")
PROOF_FILES = [
    "verification-base.k",
    "connection-rule.k",
    "verification.k",
    "spec.k",
    "connection-spec.k",
    "source-connection-spec.k",
    "identity-spec.k",
    "ground-value-spec.k",
]

TOP_LEVEL = re.compile(
    r"^[ \t]{0,2}(module|endmodule|imports|syntax|configuration|"
    r"context(?:\s+alias)?|rule|claim|macro|alias)\b"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blocks(path: Path) -> list[tuple[str, int, str]]:
    lines = path.read_text().splitlines()
    result: list[tuple[str, int, str]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("requires "):
            kind = "requires"
        else:
            match = TOP_LEVEL.match(line)
            kind = match.group(1) if match is not None else ""
        if not kind:
            index += 1
            continue
        start = index
        index += 1
        if kind not in {"module", "endmodule", "imports", "requires"}:
            while index < len(lines):
                next_line = lines[index]
                if next_line.startswith("requires ") or TOP_LEVEL.match(
                    next_line
                ):
                    break
                index += 1
        text = "\n".join(lines[start:index]).rstrip()
        result.append((kind, start + 1, text))
    return result


def attributes(text: str) -> list[str]:
    found = []
    for name in [
        "function",
        "total",
        "functional",
        "simplification",
        "priority",
        "owise",
        "symbol",
        "strict",
        "seqstrict",
        "macro",
    ]:
        if re.search(rf"\b{re.escape(name)}\b", text):
            found.append(name)
    return found


def main() -> None:
    paths = sorted(SEMANTICS_ROOT.rglob("*.k"))
    paths.extend(CANDIDATE_ROOT / name for name in PROOF_FILES)
    grand = collections.Counter()
    attribute_grand = collections.Counter()
    print(f"source_file_count={len(paths)}")
    for path in paths:
        local = blocks(path)
        counts = collections.Counter(kind for kind, _, _ in local)
        grand.update(counts)
        for _, _, text in local:
            attribute_grand.update(attributes(text))
        print(
            f"FILE {path} sha256={sha256_file(path)} "
            f"constructs={len(local)} counts={dict(sorted(counts.items()))}"
        )
    print(f"TOTAL_COUNTS {dict(sorted(grand.items()))}")
    print(f"TOTAL_ATTRIBUTES {dict(sorted(attribute_grand.items()))}")
    print("BEGIN_EXHAUSTIVE_INVENTORY")
    inventory_number = 0
    for path in paths:
        for kind, line, source in blocks(path):
            inventory_number += 1
            attrs = attributes(source)
            print(
                f"ITEM {inventory_number:04d} {path}:{line} "
                f"kind={kind} attrs={attrs}"
            )
            print(source)
            print("END_ITEM")
    print(f"END_EXHAUSTIVE_INVENTORY items={inventory_number}")

    solution = (CANDIDATE_ROOT / "solution.mpy").read_text()
    constructors = sorted(
        set(re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*\(", solution))
    )
    print(f"USED_CONSTRUCTORS {constructors}")
    semantics_lines: list[tuple[Path, int, str]] = []
    for path in sorted(SEMANTICS_ROOT.rglob("*.k")):
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            semantics_lines.append((path, line_number, line))
    for constructor in constructors:
        declaration_hits = []
        rule_hits = []
        token = re.compile(rf"\b{re.escape(constructor)}\s*\(")
        for path, line_number, line in semantics_lines:
            if not token.search(line):
                continue
            record = f"{path}:{line_number}:{line.strip()}"
            if re.match(r"^\s*(syntax|\|)", line):
                declaration_hits.append(record)
            if re.match(r"^\s*rule\b", line) or "<k>" in line:
                rule_hits.append(record)
        print(
            f"CONSTRUCTOR {constructor} declarations={len(declaration_hits)} "
            f"rule_line_hits={len(rule_hits)}"
        )
        for record in declaration_hits:
            print(f"  DECL {record}")
        for record in rule_hits:
            print(f"  RULE {record}")


if __name__ == "__main__":
    main()
