#!/usr/bin/env python3
"""Create a line-addressable exhaustive inventory of all audited K source."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/105-by-length/candidate")
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.md")
FULL_OUTPUT = Path("/audit-output/evidence/k-sources-numbered.txt")

sources = sorted((SCRATCH / "reference-semantics").rglob("*.k"))
sources += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

declaration = re.compile(
    r"^(?:"
    r"(requires)\b"
    r"|(module)\b"
    r"|(endmodule)\b"
    r"|  (imports|configuration|syntax|context|rule|claim)\b"
    r")"
)
attribute_words = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "concrete",
    "simplification",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "token",
)


def relative(path: Path) -> str:
    return str(path.relative_to(SCRATCH))


def declaration_blocks(lines: list[str]):
    starts = [
        index
        for index, line in enumerate(lines)
        if declaration.match(line) and not line.lstrip().startswith("//")
    ]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        match = declaration.match(lines[start])
        assert match
        kind = next(group for group in match.groups() if group is not None)
        yield kind, start + 1, end, "".join(lines[start:end]).rstrip()


def main() -> None:
    summary = Counter()
    markdown = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated from the clean scratch copy. Every declaration block is shown "
        "with its complete source text and line range.",
        "",
    ]
    numbered = []

    for path in sources:
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        label = relative(path)
        markdown.extend([f"## `{label}`", ""])
        numbered.append(f"===== {label} =====\n")
        for number, line in enumerate(lines, 1):
            numbered.append(f"{number:5d}\t{line}")
        if lines and not lines[-1].endswith("\n"):
            numbered.append("\n")

        for kind, start, end, block in declaration_blocks(lines):
            summary[(label, kind)] += 1
            attributes = [
                word
                for word in attribute_words
                if re.search(rf"(?<![A-Za-z0-9-]){re.escape(word)}(?![A-Za-z0-9-])", block)
            ]
            for attribute in attributes:
                summary[(label, f"attr:{attribute}")] += 1
            attr_text = ", ".join(attributes) if attributes else "none"
            markdown.extend(
                [
                    f"### {kind} at lines {start}-{end}",
                    "",
                    f"Attributes/classifiers: {attr_text}",
                    "",
                    "```k",
                    block,
                    "```",
                    "",
                ]
            )

    markdown.extend(["# Per-file counts", ""])
    for path in sources:
        label = relative(path)
        fields = []
        for (entry_label, kind), count in sorted(summary.items()):
            if entry_label == label:
                fields.append(f"{kind}={count}")
        markdown.append(f"- `{label}`: " + ", ".join(fields))
    markdown.append("")

    OUTPUT.write_text("\n".join(markdown), encoding="utf-8")
    FULL_OUTPUT.write_text("".join(numbered), encoding="utf-8")
    print(f"source_file_count={len(sources)}")
    print(f"inventory={OUTPUT}")
    print(f"numbered_sources={FULL_OUTPUT}")
    print(f"inventory_bytes={OUTPUT.stat().st_size}")
    print(f"numbered_sources_bytes={FULL_OUTPUT.stat().st_size}")
    for path in sources:
        label = relative(path)
        rule_count = summary[(label, "rule")]
        syntax_count = summary[(label, "syntax")]
        claim_count = summary[(label, "claim")]
        print(
            f"{label}: syntax={syntax_count} rule={rule_count} "
            f"claim={claim_count}"
        )


if __name__ == "__main__":
    main()
