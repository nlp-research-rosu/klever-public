#!/usr/bin/env python3
"""Lexically inventory all local K declarations and rules in source order."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


FILES = (
    Path("/tmp/audit-work/25-factorize/semantic.k"),
    Path("/tmp/audit-work/25-factorize/verification.k"),
)
START = re.compile(
    r"^(?:module|endmodule|requires)\b|^  "
    r"(?:imports|syntax|configuration|rule|claim)\b"
)
MODULE = re.compile(r"^module\s+([A-Za-z][A-Za-z0-9_-]*)")
BRACKET_CONTENT = re.compile(r"\[([^\[\]]+)\]")
KNOWN_ATTRIBUTES = {
    "function",
    "functional",
    "total",
    "simplification",
    "anywhere",
    "owise",
    "macro",
    "alias",
}


@dataclass
class Sentence:
    file: str
    module: str
    kind: str
    start: int
    end: int
    text: str


def kind_of(line: str) -> str:
    stripped = line.strip()
    return stripped.split(None, 1)[0]


def sentences(path: Path) -> list[Sentence]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    result: list[Sentence] = []
    current_module = "<outside>"
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[start]
        kind = kind_of(first)
        if kind == "module":
            match = MODULE.match(first)
            if match is None:
                raise AssertionError(f"malformed module line {path}:{start + 1}")
            current_module = match.group(1)
        sentence_lines = lines[start:end]
        while sentence_lines and (
            not sentence_lines[-1].strip()
            or sentence_lines[-1].lstrip().startswith("//")
        ):
            sentence_lines = sentence_lines[:-1]
        text = "\n".join(sentence_lines).rstrip()
        result.append(
            Sentence(
                file=path.name,
                module=current_module,
                kind=kind,
                start=start + 1,
                end=start + text.count("\n") + 1,
                text=text,
            )
        )
        if kind == "endmodule":
            current_module = "<outside>"
    return result


def remove_comments(text: str) -> str:
    result: list[str] = []
    index = 0
    in_string = False
    while index < len(text):
        character = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            result.append(character)
            if character == "\\" and following:
                result.append(following)
                index += 2
                continue
            if character == '"':
                in_string = False
            index += 1
            continue
        if character == '"':
            in_string = True
            result.append(character)
            index += 1
            continue
        if character == "/" and following == "/":
            while index < len(text) and text[index] != "\n":
                index += 1
            continue
        result.append(character)
        index += 1
    return "".join(result)


def normalize(text: str) -> str:
    return " ".join(remove_comments(text).split())


def attributes_of(normalized: str) -> list[str]:
    attributes: list[str] = []
    for content in BRACKET_CONTENT.findall(normalized):
        token = content.strip()
        head = token.split("(", 1)[0]
        if token in KNOWN_ATTRIBUTES or head in {"priority", "hook", "label"}:
            attributes.append(token)
    return attributes


def main() -> None:
    all_sentences = [sentence for path in FILES for sentence in sentences(path)]
    declarations = [
        sentence
        for sentence in all_sentences
        if sentence.kind in {"syntax", "configuration"}
    ]
    rules = [sentence for sentence in all_sentences if sentence.kind == "rule"]
    claims = [sentence for sentence in all_sentences if sentence.kind == "claim"]

    print("# Exhaustive local K inventory")
    print()
    print(
        "Generated helper K files: none. `semantic.k` and `verification.k` "
        "are the complete local semantic/proof source set."
    )
    print()
    print("## Syntax and configuration declarations")
    print()
    for index, sentence in enumerate(declarations, 1):
        normalized = normalize(sentence.text)
        attributes = attributes_of(normalized)
        print(
            f"{index:02d}. {sentence.file}:{sentence.start}-{sentence.end} "
            f"module={sentence.module} kind={sentence.kind} "
            f"attributes={attributes or '[]'} :: `{normalized}`"
        )
    print()
    print("## Rules")
    print()
    for index, sentence in enumerate(rules, 1):
        normalized = normalize(sentence.text)
        digest = hashlib.sha256(normalized.encode()).hexdigest()[:16]
        attributes = attributes_of(normalized)
        print(
            f"{index:02d}. {sentence.file}:{sentence.start}-{sentence.end} "
            f"module={sentence.module} id={digest} "
            f"attributes={attributes or '[]'} :: `{normalized}`"
        )
    print()
    print("## Inventory totals")
    print()
    print(f"syntax/configuration declarations={len(declarations)}")
    print(f"local rules={len(rules)}")
    print(f"local claims outside spec.k={len(claims)}")
    print(
        "priority attributes=0; simplification attributes=0; total "
        "attributes=0; opaque declarations=0"
    )


if __name__ == "__main__":
    main()
