#!/usr/bin/env python3
"""Lexical, exhaustive sentence inventory for all audited K source files."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
from pathlib import Path
import re
import sys

sys.path.insert(0, "/opt/humaneval/tools")
from k_rule_inventory import _mask_non_code, _without_comments  # type: ignore


ROOT = Path("/tmp/audit-work/case")
KEYWORDS = (
    "syntax",
    "configuration",
    "context",
    "rule",
    "claim",
    "alias",
)
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "no-evaluators",
    "owise",
    "priority",
    "strict",
    "seqstrict",
    "macro",
    "macro-rec",
)


def normalize(text: str) -> str:
    return " ".join(text.split())


def sources() -> list[Path]:
    files = [ROOT / "reference-semantics" / "semantics.k"]
    files += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    files += [ROOT / "verification.k", ROOT / "spec.k"]
    return files


def sentence_spans(text: str) -> list[tuple[str, int, int]]:
    masked = _mask_non_code(text)
    starts: list[tuple[str, int, int]] = []
    offset = 0
    for line_number, line in enumerate(masked.splitlines(keepends=True), 1):
        stripped = line.lstrip(" \t")
        for keyword in KEYWORDS:
            if re.match(rf"{re.escape(keyword)}(?:\s|$)", stripped):
                starts.append((keyword, offset, line_number))
                break
        if re.match(r"endmodule(?:\s|$)", stripped):
            starts.append(("endmodule", offset, line_number))
        offset += len(line)
    spans: list[tuple[str, int, int]] = []
    for index, (kind, start, line_number) in enumerate(starts):
        if kind == "endmodule":
            continue
        end = starts[index + 1][1] if index + 1 < len(starts) else len(text)
        spans.append((kind, start, end))
    return spans


def attributes(sentence: str) -> list[str]:
    found = []
    for attribute in ATTRIBUTES:
        if attribute == "priority":
            pattern = r"\bpriority\s*\("
        else:
            pattern = rf"\b{re.escape(attribute)}\b"
        if re.search(pattern, sentence):
            found.append(attribute)
    return found


def main() -> None:
    totals: Counter[str] = Counter()
    attr_totals: Counter[str] = Counter()
    file_counts: dict[str, Counter[str]] = {}
    entries: list[tuple[str, int, str, list[str], str, str]] = []
    by_file_attributes: dict[str, Counter[str]] = defaultdict(Counter)

    for path in sources():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        counts: Counter[str] = Counter()
        for kind, start, end in sentence_spans(text):
            sentence = text[start:end].rstrip()
            line = text.count("\n", 0, start) + 1
            normalized = normalize(_without_comments(sentence))
            attrs = attributes(normalized)
            digest = hashlib.sha256(normalized.encode()).hexdigest()
            entries.append((relative, line, kind, attrs, digest, normalized))
            counts[kind] += 1
            totals[kind] += 1
            for attr in attrs:
                by_file_attributes[relative][attr] += 1
                attr_totals[attr] += 1
        file_counts[relative] = counts

    print("K SOURCE INVENTORY")
    print(f"files={len(file_counts)}")
    print(f"sentences={sum(totals.values())}")
    print(f"kind_totals={dict(sorted(totals.items()))}")
    print(f"attribute_totals={dict(sorted(attr_totals.items()))}")
    print("FILE COUNTS")
    for path in file_counts:
        print(
            f"{path}: kinds={dict(sorted(file_counts[path].items()))} "
            f"attributes={dict(sorted(by_file_attributes[path].items()))}"
        )
    print("SENTENCE TABLE")
    for relative, line, kind, attrs, digest, normalized in entries:
        print(
            f"{relative}:{line}\t{kind}\tattrs={','.join(attrs) or '-'}"
            f"\tsha256={digest}\t{normalized}"
        )


if __name__ == "__main__":
    main()
