#!/usr/bin/env python3
"""Emit an exhaustive, source-located inventory of local K declarations.

This intentionally inventories source statements rather than trusting a
candidate-provided compiled definition.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
KEYWORD = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|alias|rule|claim)\b"
)
ATTR_TOKEN = re.compile(
    r"(?:\bfunction\b|\btotal\b|\bno-evaluators\b|\bconcrete\b|\bowise\b|"
    r"\bsimplification\b|\bmacro-rec\b|\bmacro\b|strict(?:\([^)]*\))?|"
    r"seqstrict\([^)]*\)|priority\([^)]*\)|symbol\([^)]*\))"
)
BRACKETS = re.compile(r"\[([^\]]*)\]")


def sources() -> list[Path]:
    return [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k")), *CANDIDATE_FILES]


def statement_kind(line: str) -> str | None:
    if line.startswith('requires "'):
        return "requires"
    match = KEYWORD.match(line)
    return match.group(1) if match else None


def statements(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if statement_kind(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[start]
        kind = statement_kind(first)
        assert kind is not None
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = "\n".join(block_lines)
        yield kind, start + 1, start + len(block_lines), text


def main() -> int:
    totals: Counter[str] = Counter()
    per_file: dict[str, Counter[str]] = defaultdict(Counter)
    attributes: Counter[str] = Counter()
    opaque = []
    priority = []
    simplification = []
    concrete = []
    macros = []

    all_statements = []
    for path in sources():
        rel = (
            path.relative_to(ROOT).as_posix()
            if path.is_relative_to(ROOT)
            else path.as_posix()
        )
        for kind, start, end, text in statements(path):
            totals[kind] += 1
            per_file[rel][kind] += 1
            compact = " ".join(line.strip() for line in text.splitlines())
            attrs = [
                match.group(0)
                for brackets in BRACKETS.finditer(compact)
                for match in ATTR_TOKEN.finditer(brackets.group(1))
            ]
            for attr in attrs:
                attributes[attr] += 1
            record = (rel, kind, start, end, compact, attrs)
            all_statements.append(record)
            if "no-evaluators" in attrs:
                opaque.append(record)
            if any(attr.startswith("priority(") for attr in attrs):
                priority.append(record)
            if "simplification" in attrs:
                simplification.append(record)
            if "concrete" in attrs:
                concrete.append(record)
            if "macro" in attrs or "macro-rec" in attrs:
                macros.append(record)

    print("# Exhaustive K source inventory")
    print()
    print("Every local statement is listed below with its source range and full compact text.")
    print()
    print(f"files={len(sources())}")
    print(f"statements={len(all_statements)}")
    print("totals=" + repr(dict(sorted(totals.items()))))
    print("attributes=" + repr(dict(sorted(attributes.items()))))
    print()
    print("## Per-file counts")
    print()
    for rel in sorted(per_file):
        print(f"- {rel}: {dict(sorted(per_file[rel].items()))}")
    print()
    print(f"opaque_no_evaluators={len(opaque)}")
    for rel, kind, start, end, compact, _ in opaque:
        print(f"- {rel}:{start}-{end} [{kind}] {compact}")
    print()
    print(f"priority_statements={len(priority)}")
    for rel, kind, start, end, compact, _ in priority:
        print(f"- {rel}:{start}-{end} [{kind}] {compact}")
    print()
    print(f"simplification_statements={len(simplification)}")
    for rel, kind, start, end, compact, _ in simplification:
        print(f"- {rel}:{start}-{end} [{kind}] {compact}")
    print()
    print(f"concrete_statements={len(concrete)}")
    for rel, kind, start, end, compact, _ in concrete:
        print(f"- {rel}:{start}-{end} [{kind}] {compact}")
    print()
    print(f"macro_statements={len(macros)}")
    for rel, kind, start, end, compact, _ in macros:
        print(f"- {rel}:{start}-{end} [{kind}] {compact}")
    print()
    print("## All statements")
    print()
    for rel, kind, start, end, compact, attrs in all_statements:
        print(
            f"- {rel}:{start}-{end} | {kind} | attrs={attrs!r} | {compact}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
