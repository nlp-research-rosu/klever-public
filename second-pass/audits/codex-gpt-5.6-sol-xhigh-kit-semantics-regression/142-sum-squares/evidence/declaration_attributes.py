#!/usr/bin/env python3
"""Exact non-comment declaration and rule-attribute census."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/142-sum-squares")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
DECL_TAGS = (
    "function",
    "total",
    "functional",
    "no-evaluators",
    "symbol",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)
RULE_TAGS = ("priority", "concrete", "owise", "simplification", "anywhere")
STOP = re.compile(
    r"^\s*(rule|syntax|context|configuration|module|endmodule|claim)\b"
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def rule_blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        if re.match(r"^\s*rule\b", lines[index]):
            start = index
            index += 1
            while index < len(lines) and not STOP.match(lines[index]):
                index += 1
            yield start + 1, "\n".join(lines[start:index])
            continue
        index += 1


def main() -> None:
    declaration_counts = {tag: 0 for tag in DECL_TAGS}
    rule_counts = {tag: 0 for tag in RULE_TAGS}
    syntax_headlines = 0
    contexts = 0
    configurations = 0
    claims = 0
    rules = 0

    print("DECORATED SYNTAX/PRODUCTION LINES")
    for source in SOURCES:
        for line_no, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            stripped = raw.lstrip()
            if stripped.startswith("//"):
                continue
            code = raw.split("//", 1)[0]
            if re.match(r"^\s*syntax\b", raw):
                syntax_headlines += 1
            if re.match(r"^\s*context\b", raw):
                contexts += 1
            if re.match(r"^\s*configuration\b", raw):
                configurations += 1
            if re.match(r"^\s*claim\b", raw):
                claims += 1
            tags = [tag for tag in DECL_TAGS if re.search(rf"\b{re.escape(tag)}\b", code)]
            if tags and ("syntax" in code or stripped.startswith("|")):
                for tag in tags:
                    declaration_counts[tag] += 1
                print(f"{rel(source)}:{line_no}\ttags={','.join(tags)}\t{raw.strip()}")

        for line_no, block in rule_blocks(source):
            rules += 1
            code_block = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
            tags = []
            for tag in RULE_TAGS:
                pattern = rf"\[{re.escape(tag)}(?:\(|\])"
                if re.search(pattern, code_block):
                    tags.append(tag)
                    rule_counts[tag] += 1
            if tags:
                print(
                    f"{rel(source)}:{line_no}\trule-tags={','.join(tags)}\t"
                    + " ".join(block.split())
                )

    print("SUMMARY")
    print(f"syntax_headlines={syntax_headlines}")
    print(f"context_headlines={contexts}")
    print(f"configuration_headlines={configurations}")
    print(f"claim_headlines={claims}")
    print(f"rule_headlines={rules}")
    for tag in DECL_TAGS:
        print(f"declaration_lines_with_{tag}={declaration_counts[tag]}")
    for tag in RULE_TAGS:
        print(f"rules_with_{tag}={rule_counts[tag]}")


if __name__ == "__main__":
    main()
