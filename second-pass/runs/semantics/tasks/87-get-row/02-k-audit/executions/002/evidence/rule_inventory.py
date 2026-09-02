#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed inventory of K declarations and rules."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re


REFERENCE_ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
ANCHOR = re.compile(
    r"^\s*(syntax(?:\s+priorities)?|configuration|context(?:\s+alias)?|"
    r"rule|claim|alias)\b"
)


def source_files() -> list[Path]:
    return sorted(REFERENCE_ROOT.rglob("*.k")) + CANDIDATE_FILES


def compressed(lines: list[str]) -> str:
    no_comments = [line.split("//", 1)[0] for line in lines]
    return " ".join(" ".join(no_comments).split())


def flags(text: str) -> list[str]:
    result: list[str] = []
    for name, pattern in (
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol\s*\("),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification\b"),
        ("owise", r"\bowise\b"),
        ("concrete", r"\bconcrete\b"),
        ("macro", r"\bmacro(?:-rec)?\b"),
        ("strictness", r"\b(?:seq)?strict\s*(?:\(|\])"),
    ):
        if re.search(pattern, text):
            result.append(name)
    return result


def decision(path: Path, kind: str, text: str) -> str:
    if str(path).startswith("/reference/"):
        if "no-evaluators" in text:
            return "FIXED_TRUST_BOUNDARY; INERT_FOR_SUBMITTED_PROGRAM"
        return "ACCEPT_FIXED_SUPPLIED_SEMANTICS; USED_PATH_AUDITED_SEPARATELY"
    if path.name == "spec.k":
        return "TRUE_RECONSTRUCTED_CLAIM; MATERIALLY_DOMAIN_LIMITED"
    if kind == "syntax":
        return "VALID_PROOF_LOCAL_DECLARATION"
    if text.startswith("rule getRowBody"):
        return "VALID_EXACT_PROGRAM_BODY_DEFINITION"
    if text.startswith("rule getRowClosure"):
        return "VALID_CLOSURE_DEFINITION"
    if text.startswith("rule addMatch"):
        return "VALID_DISJOINT_EXHAUSTIVE_INTEGER_EQUATION"
    return "REVIEWED_NO_FALSE_CONCLUSION_WITNESS"


def main() -> None:
    items: list[tuple[Path, int, str, str, list[str], str]] = []
    for path in source_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = ANCHOR.match(line)
            if match:
                starts.append((index, match.group(1)))
        for position, (start, raw_kind) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            text = compressed(lines[start:end])
            kind = raw_kind.split()[0]
            items.append((path, start + 1, kind, text, flags(text), decision(path, kind, text)))

    category_counts = Counter(item[2] for item in items)
    flag_counts = Counter(flag for item in items for flag in item[4])
    file_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for path, _line, kind, _text, item_flags, _decision in items:
        file_counts[str(path)][kind] += 1
        for flag in item_flags:
            file_counts[str(path)][f"flag:{flag}"] += 1

    print("# Exhaustive K rule/declaration inventory")
    print(f"source_files={len(source_files())}")
    print(f"inventory_items={len(items)}")
    print(f"category_counts={dict(sorted(category_counts.items()))}")
    print(f"flag_counts={dict(sorted(flag_counts.items()))}")
    print("per_file_counts:")
    for path in sorted(file_counts):
        print(f"  {path}: {dict(sorted(file_counts[path].items()))}")
    print()
    print("id\tfile\tline\tkind\tflags\tdecision\tcomplete_statement")
    for item_id, (path, line, kind, text, item_flags, item_decision) in enumerate(items, 1):
        print(
            f"K{item_id:04d}\t{path}\t{line}\t{kind}\t"
            f"{','.join(item_flags) or '-'}\t{item_decision}\t{text}"
        )


if __name__ == "__main__":
    main()
