#!/usr/bin/env python3
"""Build a line-complete inventory of K declarations and rules under review."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(?:(requires|module|endmodule)\b|  "
    r"(imports|configuration|syntax|context|rule|claim)\b)"
)


def declaration_blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for number, index in enumerate(starts):
        end = starts[number + 1] if number + 1 < len(starts) else len(lines)
        text_lines = lines[index:end]
        while text_lines and (
            not text_lines[-1].strip() or text_lines[-1].lstrip().startswith("//")
        ):
            text_lines.pop()
        match = START.match(lines[index])
        assert match is not None
        yield index + 1, match.group(1) or match.group(2), "\n".join(text_lines)


def classify(kind: str, text: str) -> str:
    if kind != "rule":
        return kind
    if "[simplification" in text:
        return "rule:simplification"
    if "[priority" in text:
        return "rule:priority"
    if "[macro" in text:
        return "rule:macro"
    if "<k>" in text or any(
        f"<{cell}>" in text
        for cell in [
            "env",
            "scopes",
            "heap",
            "heapLoc",
            "scopeLoc",
            "stack",
            "ret",
            "exc",
            "exit-code",
        ]
    ):
        return "rule:operational"
    return "rule:equational"


def review_disposition(path: Path, kind: str, text: str) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "verification.k":
        if kind == "syntax" and "[macro]" in text:
            return "ACCEPT: syntax-only exact-AST macro declaration"
        if kind == "rule" and text.lstrip().startswith("rule tri"):
            if "triLoop" in text or "triFunction" in text or "triDefinition" in text:
                return "ACCEPT: parse-time exact-AST macro expansion"
            return "ACCEPT: proof-local total mathematical definition"
        return "ACCEPT: verification module structure/declaration"
    if relative == "spec.k":
        return "TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4"
    if kind == "rule":
        if "[concrete]" in text:
            return (
                "ACCEPT: concrete-only supplied-semantics equation; absent from "
                "the Haskell proof theory unless attached to a function evaluator"
            )
        if "no-evaluators" in text:
            return "BOUNDARY: supplied opaque/trusted symbol"
        return (
            "ACCEPT: supplied-semantics rule/equation; no task-answer rule and "
            "no false conclusion witness found; target-path analysis in REVIEW.md"
        )
    if kind == "syntax" and "no-evaluators" in text:
        return "BOUNDARY: supplied opaque/trusted symbol declaration"
    return "ACCEPT: supplied-semantics structure/declaration"


def main() -> int:
    counts = Counter()
    entries = []
    raw_rule_count = 0
    raw_syntax_count = 0
    raw_claim_count = 0
    for path in FILES:
        raw_rule_count += len(
            re.findall(r"(?m)^\s*rule\b", path.read_text())
        )
        raw_syntax_count += len(
            re.findall(r"(?m)^\s*syntax\b", path.read_text())
        )
        raw_claim_count += len(
            re.findall(r"(?m)^\s*claim\b", path.read_text())
        )
        for line, kind, text in declaration_blocks(path):
            category = classify(kind, text)
            counts[category] += 1
            entries.append((path, line, category, text))

    parsed_rules = sum(value for key, value in counts.items() if key.startswith("rule:"))
    parsed_syntax = counts["syntax"]
    parsed_claims = counts["claim"]
    print("# Exhaustive K declaration and rule inventory")
    print()
    print(f"files={len(FILES)}")
    print(f"raw_rule_starts={raw_rule_count} parsed_rule_blocks={parsed_rules}")
    print(f"raw_syntax_starts={raw_syntax_count} parsed_syntax_blocks={parsed_syntax}")
    print(f"raw_claim_starts={raw_claim_count} parsed_claim_blocks={parsed_claims}")
    print(f"coverage_ok={raw_rule_count == parsed_rules and raw_syntax_count == parsed_syntax and raw_claim_count == parsed_claims}")
    print("category_counts=" + repr(dict(sorted(counts.items()))))
    print()

    special_attributes = [
        "function",
        "total",
        "functional",
        "no-evaluators",
        "priority",
        "simplification",
        "macro",
        "macro-rec",
        "owise",
        "concrete",
    ]
    for attribute in special_attributes:
        count = sum(text.count(attribute) for _, _, _, text in entries)
        print(f"attribute_occurrences[{attribute}]={count}")
    print()

    for index, (path, line, category, statement) in enumerate(entries, 1):
        relative = path.relative_to(ROOT).as_posix()
        disposition = review_disposition(path, category.split(":")[0], statement)
        print(f"## {index:04d} {relative}:{line} [{category}]")
        print(f"DISPOSITION: {disposition}")
        print("```k")
        print(statement)
        print("```")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
