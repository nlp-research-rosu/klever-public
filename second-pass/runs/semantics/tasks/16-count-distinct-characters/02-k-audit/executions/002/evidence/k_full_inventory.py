#!/usr/bin/env python3
"""Create a complete lexical inventory of local K sentences and attributes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


OUTER = re.compile(
    r"^(?P<indent>[ \t]*)(?P<keyword>"
    r"requires|module|endmodule|imports|syntax|configuration|"
    r"context|rule|claim|alias"
    r")\b"
)
ATTR = re.compile(r"\[([^\[\]]*)\]", re.S)
KNOWN_ATTRIBUTES = {
    "anywhere",
    "assoc",
    "bracket",
    "comm",
    "concrete",
    "constructor",
    "format",
    "function",
    "functional",
    "hook",
    "label",
    "left",
    "macro",
    "no-evaluators",
    "non-assoc",
    "owise",
    "priority",
    "right",
    "seqstrict",
    "simplification",
    "strict",
    "symbol",
    "token",
    "total",
    "unit",
}


def mask_comments(text: str) -> str:
    output = list(text)
    state = "code"
    depth = 0
    index = 0
    while index < len(text):
        current = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line":
            if current in "\r\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block":
            if current == "/" and following == "*":
                output[index] = output[index + 1] = " "
                depth += 1
                index += 2
                continue
            if current == "*" and following == "/":
                output[index] = output[index + 1] = " "
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
                continue
            if current not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if current == "\\" and following:
                index += 2
                continue
            if current == '"':
                state = "code"
            index += 1
            continue
        if current == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line"
            index += 2
            continue
        if current == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block"
            depth = 1
            index += 2
            continue
        if current == '"':
            state = "string"
        index += 1
    return "".join(output)


def attributes(sentence: str) -> list[str]:
    values: list[str] = []
    for match in ATTR.finditer(mask_comments(sentence)):
        content = match.group(1)
        tokens: list[str] = []
        start = 0
        depth = 0
        for index, character in enumerate(content):
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
            elif character == "," and depth == 0:
                tokens.append(content[start:index].strip())
                start = index + 1
        tokens.append(content[start:].strip())
        tokens = [token for token in tokens if token]
        if tokens and all(
            token.split("(", 1)[0].strip() in KNOWN_ATTRIBUTES
            for token in tokens
        ):
            values.extend(tokens)
    return values


def sentence_records(path: Path, display_path: str) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    masked = mask_comments(text)
    physical = text.splitlines(keepends=True)
    masked_lines = masked.splitlines(keepends=True)
    starts: list[tuple[int, str, int]] = []
    module_depth = 0
    for line_index, line in enumerate(masked_lines):
        match = OUTER.match(line)
        if match is None:
            continue
        keyword = match.group("keyword")
        indent = len(match.group("indent").replace("\t", "  "))
        if keyword == "module" and indent == 0:
            module_depth += 1
            starts.append((line_index, keyword, indent))
        elif keyword == "endmodule" and indent == 0:
            starts.append((line_index, keyword, indent))
            module_depth -= 1
        elif module_depth == 0 and indent == 0 and keyword == "requires":
            starts.append((line_index, keyword, indent))
        elif module_depth > 0 and indent == 2 and keyword in {
            "imports",
            "syntax",
            "configuration",
            "context",
            "rule",
            "claim",
            "alias",
        }:
            starts.append((line_index, keyword, indent))
    records = []
    for index, (line_index, keyword, indent) in enumerate(starts):
        next_line = starts[index + 1][0] if index + 1 < len(starts) else len(physical)
        segment = "".join(physical[line_index:next_line]).rstrip()
        if keyword == "endmodule":
            segment = physical[line_index].rstrip()
            next_line = line_index + 1
        elif keyword == "module":
            segment = physical[line_index].rstrip()
            next_line = line_index + 1
        elif keyword == "requires":
            segment = physical[line_index].rstrip()
            next_line = line_index + 1
        record_attributes = attributes(segment)
        records.append(
            {
                "id": f"{display_path}:{line_index + 1}",
                "file": display_path,
                "kind": keyword,
                "start_line": line_index + 1,
                "end_line": next_line,
                "indent": indent,
                "attributes": record_attributes,
                "is_function": any(
                    item in {"function", "functional"}
                    or item.startswith("function(")
                    for item in record_attributes
                ),
                "is_total": "total" in record_attributes,
                "is_opaque": "no-evaluators" in record_attributes,
                "is_priority": any(
                    item.startswith("priority") for item in record_attributes
                ),
                "is_simplification": "simplification" in record_attributes,
                "is_macro": "macro" in record_attributes,
                "normalized_sha256": hashlib.sha256(
                    " ".join(segment.split()).encode()
                ).hexdigest(),
                "text": segment,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    all_records: list[dict[str, object]] = []
    files = []
    for relative in args.files:
        path = args.root / relative
        data = path.read_bytes()
        records = sentence_records(path, relative)
        all_records.extend(records)
        files.append(
            {
                "file": relative,
                "sha256": hashlib.sha256(data).hexdigest(),
                "records": len(records),
            }
        )

    counts: dict[str, int] = {}
    flags = {
        "function_declarations": 0,
        "total_declarations": 0,
        "opaque_declarations": 0,
        "priority_rules": 0,
        "simplification_rules": 0,
        "macro_declarations": 0,
    }
    for record in all_records:
        kind = str(record["kind"])
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "syntax" and record["is_function"]:
            flags["function_declarations"] += 1
        if kind == "syntax" and record["is_total"]:
            flags["total_declarations"] += 1
        if kind == "syntax" and record["is_opaque"]:
            flags["opaque_declarations"] += 1
        if kind == "rule" and record["is_priority"]:
            flags["priority_rules"] += 1
        if kind == "rule" and record["is_simplification"]:
            flags["simplification_rules"] += 1
        if kind == "syntax" and record["is_macro"]:
            flags["macro_declarations"] += 1

    document = {
        "schema_version": 1,
        "root": str(args.root),
        "files": files,
        "counts": counts,
        "flags": flags,
        "records": all_records,
    }
    args.output.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"counts": counts, "flags": flags}, sort_keys=True))
    print(f"FILES: {len(files)}")
    print(f"RECORDS: {len(all_records)}")
    print("FULL_K_INVENTORY: WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
