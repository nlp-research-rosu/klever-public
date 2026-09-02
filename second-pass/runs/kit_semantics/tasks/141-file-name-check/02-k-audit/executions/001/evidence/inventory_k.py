#!/usr/bin/env python3
"""Create a location-complete inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k"
]
DECLARATION = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias)\b"
)
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "macro",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "anywhere",
    "strict",
    "seqstrict",
    "hook",
)


def one_line(lines: list[str]) -> str:
    return " ".join(" ".join(lines).split())


def classify(kind: str, text: str) -> str:
    tags = [attribute for attribute in ATTRIBUTES if attribute in text]
    if kind == "rule":
        tags.append("operational-cell-rule" if "<k>" in text else "equational-rule")
        if not any(
            tag in tags
            for tag in (
                "priority",
                "simplification",
                "concrete",
                "owise",
                "anywhere",
            )
        ):
            tags.append("ordinary")
    if kind == "syntax" and "no-evaluators" in tags:
        tags.append("opaque-when-symbolic")
    return ",".join(tags) if tags else "ordinary"


def main() -> None:
    totals: collections.Counter[str] = collections.Counter()
    tag_totals: collections.Counter[str] = collections.Counter()
    print(
        "source\tstart\tend\tkind\tclassification\tdeclaration_or_rule"
    )
    for path in SOURCES:
        lines = path.read_text().splitlines()
        starts = [
            index
            for index, line in enumerate(lines)
            if DECLARATION.match(line)
        ]
        relative = path.relative_to(ROOT).as_posix()
        for position, start in enumerate(starts):
            next_start = starts[position + 1] if position + 1 < len(starts) else len(lines)
            end = next_start
            while end > start + 1:
                stripped = lines[end - 1].strip()
                if (
                    stripped
                    and not stripped.startswith("//")
                    and stripped not in {"endmodule"}
                    and not stripped.startswith("imports ")
                    and not stripped.startswith("module ")
                ):
                    break
                end -= 1
            match = DECLARATION.match(lines[start])
            assert match is not None
            kind = match.group(1)
            text = one_line(lines[start:end])
            classification = classify(kind, text)
            totals[kind] += 1
            for tag in classification.split(","):
                tag_totals[tag] += 1
            safe_text = text.replace("\t", " ")
            print(
                f"{relative}\t{start + 1}\t{end}\t{kind}\t"
                f"{classification}\t{safe_text}"
            )

    print("SUMMARY_BY_KIND")
    for kind, count in sorted(totals.items()):
        print(f"{kind}={count}")
    print("SUMMARY_BY_CLASSIFICATION_TAG")
    for tag, count in sorted(tag_totals.items()):
        print(f"{tag}={count}")
    print(f"source_files={len(SOURCES)}")
    print(f"declarations_total={sum(totals.values())}")


if __name__ == "__main__":
    main()
