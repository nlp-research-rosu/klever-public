#!/usr/bin/env python3
"""Produce an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/intersperse-audit")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\b|endmodule\b|module\b)"
)


def collect_blocks(lines: list[str]):
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for offset, (start, kind) in enumerate(starts):
        if kind in {"module", "endmodule"}:
            continue
        end = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].lstrip().startswith("/*")
        ):
            block_lines.pop()
        yield start + 1, kind, "\n".join(block_lines)


def tags(kind: str, block: str) -> list[str]:
    result: list[str] = []
    for tag in [
        "function",
        "functional",
        "total",
        "macro",
        "strict",
        "seqstrict",
        "priority",
        "owise",
        "simplification",
        "concrete",
        "symbol",
        "no-evaluators",
    ]:
        if re.search(rf"\b{re.escape(tag)}\b", block):
            result.append(tag)
    if kind == "rule":
        result.append("operational" if "<k>" in block else "equational")
    return result


def normalized(block: str) -> str:
    return re.sub(r"\s+", " ", block).strip()


def main() -> None:
    grand = Counter()
    opaque_candidates: list[str] = []
    for source in SOURCES:
        relative = source.relative_to(ROOT)
        lines = source.read_text().splitlines()
        modules = [
            (index + 1, match.group(1))
            for index, line in enumerate(lines)
            if (match := re.match(r"^\s*module\s+([A-Za-z0-9-]+)", line))
        ]
        print(f"\nFILE {relative}")
        print("MODULES " + ", ".join(f"{name}@{line}" for line, name in modules))
        counts = Counter()
        for line_number, kind, block in collect_blocks(lines):
            block_tags = tags(kind, block)
            counts[kind] += 1
            grand[kind] += 1
            for tag in block_tags:
                counts[f"tag:{tag}"] += 1
                grand[f"tag:{tag}"] += 1
            if "no-evaluators" in block_tags:
                opaque_candidates.append(
                    f"{relative}:{line_number}: {normalized(block)}"
                )
            print(
                f"{relative}:{line_number}: {kind.upper()} "
                f"[{','.join(block_tags) if block_tags else '-'}] "
                f"{normalized(block)}"
            )
        print(
            "FILE_COUNTS "
            + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        )
    print("\nGLOBAL_COUNTS")
    print(" ".join(f"{key}={value}" for key, value in sorted(grand.items())))
    print("\nOPAQUE_OR_NO_EVALUATOR_DECLARATIONS")
    if opaque_candidates:
        for item in opaque_candidates:
            print(item)
    else:
        print("none")


if __name__ == "__main__":
    main()
