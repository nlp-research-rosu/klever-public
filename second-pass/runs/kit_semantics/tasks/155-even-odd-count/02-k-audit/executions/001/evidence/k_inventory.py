#!/usr/bin/env python3
"""Emit a source-derived inventory of every local K declaration and rule."""

from __future__ import annotations

import re
from pathlib import Path


WORK = Path("/tmp/audit-work/155-even-odd-count/work")
SOURCES = sorted((WORK / "reference-semantics").rglob("*.k")) + sorted(
    path for path in WORK.glob("*.k") if path.is_file()
)
START = re.compile(
    r"^(?:"
    r"(?:requires|module|endmodule)\b"
    r"|  (?:imports|syntax|configuration|context|rule|claim|alias)\b"
    r")"
)
KIND = re.compile(
    r"^\s*(requires|module|endmodule|imports|syntax|configuration|"
    r"context|rule|claim|alias)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "trusted",
    "anywhere",
)


def records(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) is not None
    ]
    result: list[tuple[int, str, str]] = []
    for offset, start in enumerate(starts):
        stop = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        fragment_lines = lines[start:stop]
        while fragment_lines and (
            not fragment_lines[-1].strip()
            or fragment_lines[-1].lstrip().startswith("//")
        ):
            fragment_lines.pop()
        first = fragment_lines[0]
        match = KIND.match(first)
        if match is None:
            raise AssertionError(f"unclassified record: {path}:{start + 1}")
        normalized = " ".join(
            line.strip()
            for line in fragment_lines
            if line.strip() and not line.lstrip().startswith("//")
        )
        result.append((start + 1, match.group(1), normalized))
    return result


def main() -> None:
    print(
        "source\tline\tkind\tattributes\torigin_review_class\tdeclaration"
    )
    counts: dict[str, int] = {}
    attribute_counts: dict[str, int] = {}
    source_count = 0
    total = 0
    for path in SOURCES:
        source_count += 1
        relative = path.relative_to(WORK).as_posix()
        if relative.startswith("reference-semantics/"):
            origin = "SUPPLIED_BASE"
        elif relative == "verification-with-lemma.k":
            origin = "PROOF_OPERATIONAL_BRIDGE"
        elif relative == "verification.k":
            origin = "PROOF_LOCAL_THEORY"
        else:
            origin = "CLAIM_OR_TEST_ARTIFACT"
        for line, kind, text in records(path):
            found = [
                attribute
                for attribute in ATTRIBUTES
                if re.search(rf"(?<![A-Za-z-]){re.escape(attribute)}(?![A-Za-z-])", text)
            ]
            for attribute in found:
                attribute_counts[attribute] = (
                    attribute_counts.get(attribute, 0) + 1
                )
            counts[kind] = counts.get(kind, 0) + 1
            total += 1
            escaped = text.replace("\t", " ").replace("\n", " ")
            print(
                f"{relative}\t{line}\t{kind}\t{','.join(found) or '-'}"
                f"\t{origin}\t{escaped}"
            )
    print(f"# sources={source_count}")
    print(f"# records={total}")
    print(f"# kind_counts={dict(sorted(counts.items()))}")
    print(f"# attribute_counts={dict(sorted(attribute_counts.items()))}")


if __name__ == "__main__":
    main()
