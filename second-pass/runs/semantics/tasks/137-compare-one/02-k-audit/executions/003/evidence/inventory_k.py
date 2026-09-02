#!/usr/bin/env python3
"""Exhaustive lexical inventory of supplied and proof-local K sentences."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


OUTER_KEYWORDS = {
    "alias",
    "claim",
    "configuration",
    "context",
    "contextalias",
    "imports",
    "module",
    "endmodule",
    "rule",
    "syntax",
}


def mask_non_code(text: str) -> str:
    output = list(text)
    index = 0
    block_depth = 0
    state = "code"
    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if char in "\r\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if char == "\\" and following:
                output[index] = output[index + 1] = " "
                index += 2
                continue
            if char == '"':
                state = "code"
            elif char not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if state == "block-comment":
            if char == "/" and following == "*":
                output[index] = output[index + 1] = " "
                block_depth += 1
                index += 2
                continue
            if char == "*" and following == "/":
                output[index] = output[index + 1] = " "
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
                continue
            if char not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if char == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line-comment"
            index += 2
            continue
        if char == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block-comment"
            block_depth = 1
            index += 2
            continue
        if char == '"':
            state = "string"
        index += 1
    return "".join(output)


def attributes(text: str) -> list[str]:
    tokens: list[str] = []
    for body in re.findall(r"\[([^\[\]]*)\]", text, re.S):
        depth = 0
        start = 0
        for index, char in enumerate(body):
            if char == "(":
                depth += 1
            elif char == ")":
                depth = max(depth - 1, 0)
            elif char == "," and depth == 0:
                token = body[start:index].strip()
                if token:
                    tokens.append(token)
                start = index + 1
        token = body[start:].strip()
        if token:
            tokens.append(token)
    return tokens


def inventory_file(path: Path, root: Path, source_class: str) -> list[dict]:
    text = path.read_text()
    masked = mask_non_code(text)
    line_offsets = [0]
    for match in re.finditer("\n", masked):
        line_offsets.append(match.end())
    starts: list[tuple[int, int, str]] = []
    for line_number, offset in enumerate(line_offsets, 1):
        end = masked.find("\n", offset)
        end = len(masked) if end < 0 else end
        line = masked[offset:end]
        stripped = line.lstrip()
        match = re.match(r"([A-Za-z][A-Za-z0-9_']*)\b", stripped)
        if match and match.group(1) in OUTER_KEYWORDS:
            starts.append((offset, line_number, match.group(1)))
    records: list[dict] = []
    for index, (start, start_line, keyword) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(text)
        sentence = text[start:end].rstrip()
        if not sentence:
            continue
        end_line = start_line + sentence.count("\n")
        normalized = " ".join(sentence.split())
        attrs = attributes(sentence)
        records.append(
            {
                "source_class": source_class,
                "file": path.relative_to(root).as_posix(),
                "keyword": keyword,
                "start_line": start_line,
                "end_line": end_line,
                "attributes": attrs,
                "is_function": any(
                    token == "function" or token.startswith("function(")
                    for token in attrs
                ),
                "is_total": "total" in attrs,
                "is_functional": "functional" in attrs,
                "is_opaque": any(
                    token == "no-evaluators" or token.startswith("symbol")
                    for token in attrs
                ),
                "is_priority": any(token.startswith("priority(") for token in attrs),
                "is_simplification": "simplification" in attrs,
                "is_concrete": "concrete" in attrs,
                "is_owise": "owise" in attrs,
                "normalized_sha256": hashlib.sha256(normalized.encode()).hexdigest(),
                "text": sentence,
            }
        )
    return records


def main() -> None:
    workspace = Path("/tmp/audit-work/137-compare-one")
    supplied_root = workspace / "reference-semantics"
    files = sorted(supplied_root.rglob("*.k"))
    records: list[dict] = []
    for path in files:
        records.extend(inventory_file(path, workspace, "supplied-semantics"))
    for name, source_class in (
        ("verification.k", "proof-local"),
        ("spec.k", "target-spec"),
    ):
        records.extend(inventory_file(workspace / name, workspace, source_class))

    counts = Counter(
        (record["source_class"], record["keyword"]) for record in records
    )
    attr_counts = Counter()
    for record in records:
        for key in (
            "is_function",
            "is_total",
            "is_functional",
            "is_opaque",
            "is_priority",
            "is_simplification",
            "is_concrete",
            "is_owise",
        ):
            if record[key]:
                attr_counts[(record["source_class"], key)] += 1
    by_file = defaultdict(Counter)
    for record in records:
        by_file[record["file"]][record["keyword"]] += 1

    document = {
        "schema_version": 1,
        "files": [path.relative_to(workspace).as_posix() for path in files]
        + ["verification.k", "spec.k"],
        "counts": {
            f"{source}:{keyword}": count
            for (source, keyword), count in sorted(counts.items())
        },
        "attribute_counts": {
            f"{source}:{attribute}": count
            for (source, attribute), count in sorted(attr_counts.items())
        },
        "by_file": {
            filename: dict(sorted(counter.items()))
            for filename, counter in sorted(by_file.items())
        },
        "records": records,
    }
    encoded = json.dumps(
        document, indent=2, sort_keys=True, ensure_ascii=False
    ) + "\n"
    output = Path("/audit-output/evidence/05-rule-inventory.json")
    output.write_text(encoded)
    print(f"FILES: {len(document['files'])}")
    print(f"SENTENCES: {len(records)}")
    print(f"COUNTS: {dict(sorted(document['counts'].items()))}")
    print(
        f"ATTRIBUTE_COUNTS: {dict(sorted(document['attribute_counts'].items()))}"
    )
    print(f"INVENTORY_SHA256: {hashlib.sha256(encoded.encode()).hexdigest()}")
    print(f"OUTPUT: {output}")


if __name__ == "__main__":
    main()
