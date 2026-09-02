#!/usr/bin/env python3
"""Generate an exhaustive declaration/rule inventory for audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


WORK = Path("/tmp/audit-work")
REFERENCE_ROOT = WORK / "reference-semantics"
DECLARATION = re.compile(
    r"^\s*(configuration\b|context(?:\s+alias)?\b|syntax\b|rule\b|claim\b)"
)
BOUNDARY = re.compile(
    r"^\s*(configuration\b|context(?:\s+alias)?\b|syntax\b|rule\b|claim\b|"
    r"module\b|endmodule\b|imports\b)"
)


def classify(path: Path, line: int, kind: str, block: str) -> str:
    if path.is_relative_to(REFERENCE_ROOT):
        if "no-evaluators" in block or "symbol(" in block:
            return "SUPPLIED_OPAQUE_OR_SYMBOLIC_PRIMITIVE"
        if "[concrete" in block:
            return "SUPPLIED_CONCRETE_RULE"
        return "SUPPLIED_FIXED_SEMANTICS"

    if path.name == "verification.k":
        if 8 <= line <= 37:
            return "ACCEPT_EXACT_PROGRAM_MACRO"
        if 41 <= line <= 45:
            return "ACCEPT_WITH_BOUNDARY_DECIMAL_VALUE_NAME"
        if 50 <= line <= 52:
            return "REJECT_RESULT_BEARING_OPAQUE_ORACLE"
        if 56 <= line <= 75:
            return "REJECT_UNJUSTIFIED_CONDITION_BRIDGE"
        if 78 <= line <= 87:
            return "ACCEPT_STRUCTURAL_INPUT_AND_ITERATOR"
        if 89 <= line <= 92:
            return "ACCEPT_TOTAL_POSITIVE_DOMAIN_PREDICATE"
        if 96 <= line <= 113:
            return "LOCALLY_SOUND_RELATIVE_TO_REJECTED_ORACLE"
        if 122 <= line <= 152:
            return "TEXTUALLY_DERIVED_LOOP_RULE_TAINTED_BY_REJECTED_ORACLE"
        return "REVIEWED_VERIFICATION_OTHER"

    if path.name == "spec.k":
        if line == 6:
            return "TARGET_LOOP_CLAIM_ORACLE_RELATIVE"
        if line == 42:
            return "TARGET_ENTRY_CLAIM_NOT_INTENT_RESULT_CONSTRAINING"
        return "SPEC_DECLARATION"

    return "UNCLASSIFIED"


def attributes(block: str) -> str:
    result: list[str] = []
    for marker in (
        "function",
        "total",
        "functional",
        "macro",
        "simplification",
        "priority",
        "owise",
        "anywhere",
        "concrete",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(marker)}\b", block):
            result.append(marker)
    return ",".join(result) if result else "-"


def entries(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, text in enumerate(lines) if DECLARATION.match(text)]
    result: list[tuple[int, str, str]] = []
    for pos, start in enumerate(starts):
        end = len(lines)
        for candidate in range(start + 1, len(lines)):
            if BOUNDARY.match(lines[candidate]):
                end = candidate
                break
        block_lines = lines[start:end]
        # Drop trailing blank/comment lines that introduce the next declaration.
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        kind_match = DECLARATION.match(lines[start])
        assert kind_match is not None
        kind = kind_match.group(1).replace(" ", "_")
        result.append((start + 1, kind, block))
    return result


def main() -> None:
    paths = [REFERENCE_ROOT / "semantics.k"]
    paths.extend(sorted((REFERENCE_ROOT / "semantics").glob("*.k")))
    paths.extend([WORK / "verification.k", WORK / "spec.k"])

    print(
        "origin\tpath\tline\tkind\tattributes\tdecision\t"
        "source_excerpt"
    )
    counts: dict[tuple[str, str], int] = {}
    for path in paths:
        origin = "supplied" if path.is_relative_to(REFERENCE_ROOT) else "candidate"
        relative = str(path.relative_to(WORK))
        for line, kind, block in entries(path):
            decision = classify(path, line, kind, block)
            counts[(origin, kind)] = counts.get((origin, kind), 0) + 1
            excerpt = re.sub(r"\s+", " ", block).strip().replace("\t", " ")
            print(
                f"{origin}\t{relative}\t{line}\t{kind}\t{attributes(block)}\t"
                f"{decision}\t{excerpt}"
            )

    print("# SUMMARY")
    for (origin, kind), count in sorted(counts.items()):
        print(f"# {origin}\t{kind}\t{count}")


if __name__ == "__main__":
    main()
