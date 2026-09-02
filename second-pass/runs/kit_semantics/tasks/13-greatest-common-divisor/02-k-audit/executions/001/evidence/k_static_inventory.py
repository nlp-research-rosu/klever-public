#!/usr/bin/env python3
"""Lexical exhaustive inventory of K outer sentences for this audit."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
SOURCES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
KEYWORDS = {
    "syntax",
    "rule",
    "configuration",
    "context",
    "claim",
    "alias",
    "macro",
}
KNOWN_ATTRIBUTES = {
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "strict",
    "seqstrict",
    "priority",
    "symbol",
    "no-evaluators",
    "assoc",
    "comm",
    "unit",
    "idem",
    "constructor",
    "token",
    "bracket",
    "left",
    "right",
}


def mask_noncode(text: str) -> str:
    output = list(text)
    state = "code"
    depth = 0
    index = 0
    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if char == "\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block-comment":
            if char == "/" and following == "*":
                output[index] = output[index + 1] = " "
                depth += 1
                index += 2
                continue
            if char == "*" and following == "/":
                output[index] = output[index + 1] = " "
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
                continue
            if char != "\n":
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
            else:
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
            depth = 1
            index += 2
            continue
        if char == '"':
            state = "string"
        index += 1
    return "".join(output)


def strip_comments(text: str) -> str:
    output: list[str] = []
    state = "code"
    depth = 0
    index = 0
    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if char == "\n":
                output.append(char)
                state = "code"
            index += 1
            continue
        if state == "block-comment":
            if char == "/" and following == "*":
                depth += 1
                index += 2
                continue
            if char == "*" and following == "/":
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
                continue
            if char == "\n":
                output.append(char)
            index += 1
            continue
        if state == "string":
            output.append(char)
            if char == "\\" and following:
                output.append(following)
                index += 2
                continue
            if char == '"':
                state = "code"
            index += 1
            continue
        if char == "/" and following == "/":
            state = "line-comment"
            index += 2
            continue
        if char == "/" and following == "*":
            state = "block-comment"
            depth = 1
            index += 2
            continue
        output.append(char)
        if char == '"':
            state = "string"
        index += 1
    return "".join(output)


def attributes(text: str) -> list[str]:
    found: set[str] = set()
    for group in re.findall(r"\[([^\[\]]*)\]", text, re.S):
        for attribute in KNOWN_ATTRIBUTES:
            if re.search(rf"\b{re.escape(attribute)}(?:\b|\()", group):
                found.add(attribute)
    return sorted(found)


def role(source: Path, keyword: str, attrs: list[str]) -> str:
    if keyword == "claim":
        return "reachability-claim"
    if keyword == "configuration":
        return "configuration"
    if keyword == "context":
        return "evaluation-context"
    if keyword in {"alias", "macro"} or "macro" in attrs:
        return "macro-or-alias"
    if keyword == "syntax":
        roles = ["syntax-declaration"]
        for tag in ("function", "total", "functional", "symbol", "no-evaluators"):
            if tag in attrs:
                roles.append(tag)
        return "+".join(roles)
    if keyword == "rule":
        roles = []
        if source.name == "verification.k":
            roles.append("proof-local")
        else:
            roles.append("fixed-semantic")
        roles.append("simplification-rule" if "simplification" in attrs else "ordinary-rule")
        for tag in ("priority", "owise", "concrete"):
            if tag in attrs:
                roles.append(tag)
        return "+".join(roles)
    return keyword


def source_inventory(path: Path) -> list[dict[str, object]]:
    text = path.read_text()
    masked = mask_noncode(text)
    lines = text.splitlines(keepends=True)
    masked_lines = masked.splitlines(keepends=True)
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(masked_lines):
        match = re.match(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\b", line)
        if match and match.group(1) in KEYWORDS:
            starts.append((index, match.group(1)))
    documents: list[dict[str, object]] = []
    for number, (start, keyword) in enumerate(starts):
        end = starts[number + 1][0] if number + 1 < len(starts) else len(lines)
        while end > start and re.match(r"^\s*(?:endmodule)?\s*$", lines[end - 1]):
            end -= 1
        sentence = "".join(lines[start:end]).rstrip()
        code_sentence = strip_comments(sentence)
        normalized = " ".join(code_sentence.split())
        attrs = attributes(code_sentence)
        relative = path.relative_to(ROOT).as_posix()
        documents.append(
            {
                "id": hashlib.sha256(
                    f"{relative}:{start + 1}:{normalized}".encode()
                ).hexdigest()[:16],
                "source": relative,
                "start_line": start + 1,
                "end_line": max(start + 1, end),
                "keyword": keyword,
                "attributes": attrs,
                "role": role(path, keyword, attrs),
                "normalized_text": normalized,
            }
        )
    return documents


def main() -> None:
    documents = [entry for source in SOURCES for entry in source_inventory(source)]
    payload = {
        "schema_version": 1,
        "sources": [source.relative_to(ROOT).as_posix() for source in SOURCES],
        "entries": documents,
    }
    Path("/audit-output/evidence/k-rule-inventory.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )

    by_keyword = collections.Counter(str(item["keyword"]) for item in documents)
    by_role = collections.Counter(str(item["role"]) for item in documents)
    by_source = collections.Counter(str(item["source"]) for item in documents)
    digest = hashlib.sha256(
        json.dumps(documents, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    markdown = [
        "# Exhaustive K declaration and rule inventory",
        "",
        f"Inventory SHA-256: `{digest}`",
        "",
        f"Total outer declarations/rules/claims: {len(documents)}",
        "",
        "Keyword counts: "
        + ", ".join(f"{key}={value}" for key, value in sorted(by_keyword.items())),
        "",
        "Role counts: "
        + ", ".join(f"{key}={value}" for key, value in sorted(by_role.items())),
        "",
        "## Per-source counts",
        "",
        "| Source | Count |",
        "|---|---:|",
    ]
    markdown.extend(
        f"| `{source}` | {count} |" for source, count in sorted(by_source.items())
    )
    markdown.extend(
        [
            "",
            "## Every inventoried sentence",
            "",
            "| ID | Source:lines | Kind / attributes / role | Normalized text |",
            "|---|---|---|---|",
        ]
    )
    for item in documents:
        attrs = ",".join(item["attributes"]) or "none"
        text = str(item["normalized_text"]).replace("|", "\\|")
        markdown.append(
            f"| `{item['id']}` | `{item['source']}:{item['start_line']}-"
            f"{item['end_line']}` | {item['keyword']}; {attrs}; "
            f"{item['role']} | `{text}` |"
        )
    Path("/audit-output/evidence/k-rule-inventory.md").write_text(
        "\n".join(markdown) + "\n"
    )

    print(f"inventory_sha256={digest}")
    print(f"total_entries={len(documents)}")
    print(f"keyword_counts={dict(sorted(by_keyword.items()))}")
    print(f"role_counts={dict(sorted(by_role.items()))}")
    print("per_source_counts:")
    for source, count in sorted(by_source.items()):
        print(f"{count:4d} {source}")


if __name__ == "__main__":
    main()
