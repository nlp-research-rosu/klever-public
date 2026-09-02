#!/usr/bin/env python3
"""Exhaustive textual inventory of local K declarations used by the audit."""

from __future__ import annotations

import collections
import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/src")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(module|endmodule|imports|syntax|rule|claim|configuration|context|alias)\b"
)
INVENTORY_KINDS = {"syntax", "rule", "claim", "configuration", "context", "alias"}


def source_class(path: Path) -> str:
    if path.name == "verification.k":
        return "proof_extension"
    if path.name == "spec.k":
        return "proof_claim"
    return "supplied_semantics"


def attrs(kind: str, text: str) -> list[str]:
    found: list[str] = []
    checks: tuple[tuple[str, str], ...] = ()
    if kind == "syntax":
        checks = (
            ("function", r"\bfunction\b"),
            ("functional", r"\bfunctional\b"),
            ("total", r"\btotal\b"),
            ("symbol", r"\bsymbol\s*\("),
            ("no-evaluators", r"\bno-evaluators\b"),
            ("macro", r"\bmacro(?:-rec)?\b"),
            ("strict", r"\b(?:seq)?strict\b"),
        )
    elif kind == "rule":
        checks = (
            ("simplification", r"\bsimplification\b"),
            ("priority", r"\bpriority\s*\("),
            ("owise", r"\bowise\b"),
        )
    for label, pattern in checks:
        if re.search(pattern, text):
            found.append(label)
    if kind == "rule":
        found.append("operational" if "<k>" in text else "equational")
    return found


def declarations(path: Path) -> list[tuple[int, int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[int, int, str, str]] = []
    for offset, (index, kind) in enumerate(starts):
        if kind not in INVENTORY_KINDS:
            continue
        next_index = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        block = lines[index:next_index]
        while block and (
            not block[-1].strip() or block[-1].lstrip().startswith("//")
        ):
            block.pop()
        text = " ".join(
            part.strip()
            for part in block
            if part.strip() and not part.lstrip().startswith("//")
        )
        result.append((index + 1, index + len(block), kind, text))
    return result


def main() -> int:
    counts: collections.Counter[tuple[str, str]] = collections.Counter()
    file_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    attribute_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    rows: list[str] = []
    opaque_rows: list[str] = []
    priority_rows: list[str] = []

    for path in FILES:
        rel = path.relative_to(ROOT)
        classification = source_class(path)
        for start, end, kind, text in declarations(path):
            declaration_attrs = attrs(kind, text)
            counts[(classification, kind)] += 1
            file_counts[(str(rel), kind)] += 1
            for attribute in declaration_attrs:
                attribute_counts[(classification, attribute)] += 1
            location = f"{rel}:{start}-{end}"
            rows.append(
                "\t".join(
                    (
                        classification,
                        kind,
                        ",".join(declaration_attrs) or "-",
                        location,
                        text,
                    )
                )
            )
            if "symbol" in declaration_attrs or "no-evaluators" in declaration_attrs:
                opaque_rows.append(f"{location}\t{text}")
            if "priority" in declaration_attrs or "owise" in declaration_attrs:
                priority_rows.append(
                    f"{location}\t{','.join(declaration_attrs)}\t{text}"
                )

    print("INVENTORY_COUNTS")
    for key, value in sorted(counts.items()):
        print(f"{key[0]}\t{key[1]}\t{value}")
    print("ATTRIBUTE_COUNTS")
    for key, value in sorted(attribute_counts.items()):
        print(f"{key[0]}\t{key[1]}\t{value}")
    print("FILE_COUNTS")
    for key, value in sorted(file_counts.items()):
        print(f"{key[0]}\t{key[1]}\t{value}")
    print("OPAQUE_OR_NO_EVALUATOR_DECLARATIONS")
    for row in opaque_rows:
        print(row)
    print("PRIORITY_OR_OWISE_RULES")
    for row in priority_rows:
        print(row)
    print("ALL_DECLARATIONS_TSV")
    print("source_class\tkind\tattributes\tlocation\tdeclaration")
    for row in rows:
        print(row)
    print(f"TOTAL_INVENTORIED_DECLARATIONS\t{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
