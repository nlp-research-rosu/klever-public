#!/usr/bin/env python3
"""Lexical, source-complete inventory of K top-level sentences."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/proof")
SEMANTICS = ROOT / "reference-semantics"
FILES = sorted(SEMANTICS.rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
    ROOT / "lemma-spec.k",
]
START = re.compile(
    r"^[ \t]*(module|endmodule|imports|syntax|rule|configuration|"
    r"context|claim|alias)\b",
    re.MULTILINE,
)


def mask_comments_and_strings(text: str) -> str:
    output = list(text)
    index = 0
    state = "code"
    block_depth = 0
    while index < len(text):
        current = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if current == "\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block-comment":
            if current == "/" and following == "*":
                output[index] = output[index + 1] = " "
                block_depth += 1
                index += 2
                continue
            if current == "*" and following == "/":
                output[index] = output[index + 1] = " "
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
                continue
            if current != "\n":
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if current == "\\" and following:
                output[index] = output[index + 1] = " "
                index += 2
                continue
            if current == '"':
                state = "code"
            elif current != "\n":
                output[index] = " "
            index += 1
            continue
        if current == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line-comment"
            index += 2
            continue
        if current == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block-comment"
            block_depth = 1
            index += 2
            continue
        if current == '"':
            state = "string"
        index += 1
    return "".join(output)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def classify(keyword: str, text: str) -> str:
    if keyword == "rule":
        attributes = []
        if "simplification" in text:
            attributes.append("simplification")
        priority = re.search(r"priority\s*\(\s*([0-9]+)\s*\)", text)
        if priority:
            attributes.append(f"priority({priority.group(1)})")
        if "owise" in text:
            attributes.append("owise")
        return "rule" + (":" + ",".join(attributes) if attributes else ":ordinary")
    if keyword == "syntax":
        attributes = [
            marker
            for marker in (
                "function",
                "total",
                "functional",
                "macro",
                "token",
                "symbol",
                "hook",
            )
            if re.search(rf"\b{marker}\b", text)
        ]
        return "syntax" + (":" + ",".join(attributes) if attributes else "")
    return keyword


def main() -> int:
    totals: Counter[str] = Counter()
    per_file: dict[str, Counter[str]] = defaultdict(Counter)
    documents: list[dict[str, object]] = []

    for path in FILES:
        text = path.read_text()
        masked = mask_comments_and_strings(text)
        matches = list(START.finditer(masked))
        relative = (
            path.relative_to(ROOT).as_posix()
            if path.is_relative_to(ROOT)
            else str(path)
        )
        for index, match in enumerate(matches):
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            keyword = match.group(1)
            statement = text[start:end].strip()
            if keyword in {"module", "endmodule"}:
                statement = statement.splitlines()[0].strip()
                end = start + len(text[start:].splitlines(keepends=True)[0])
            category = classify(keyword, statement)
            totals[category] += 1
            per_file[relative][category] += 1
            documents.append(
                {
                    "id": f"{relative}:{line_number(text, start)}",
                    "file": relative,
                    "start_line": line_number(text, start),
                    "end_line": line_number(text, max(start, end - 1)),
                    "keyword": keyword,
                    "category": category,
                    "sha256": hashlib.sha256(statement.encode()).hexdigest(),
                    "text": statement,
                }
            )

    print("SUMMARY")
    print(json.dumps(dict(sorted(totals.items())), sort_keys=True))
    print("PER_FILE")
    for path, counts in sorted(per_file.items()):
        print(path, json.dumps(dict(sorted(counts.items())), sort_keys=True))
    print("STATEMENTS")
    for document in documents:
        print(json.dumps(document, ensure_ascii=False, sort_keys=True))
    print(f"STATEMENT_COUNT={len(documents)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
