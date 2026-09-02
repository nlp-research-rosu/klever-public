#!/usr/bin/env python3
"""Create a source-level inventory of every local K sentence in audit scope."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


REFERENCE_ROOT = Path("/reference/reference-semantics")
FILES = [REFERENCE_ROOT / "semantics.k"]
FILES.extend(sorted((REFERENCE_ROOT / "semantics").glob("*.k")))
FILES.extend([Path("/candidate/verification.k"), Path("/candidate/spec.k")])
OUT_JSON = Path("/audit-output/evidence/rule_inventory.json")
OUT_MD = Path("/audit-output/evidence/rule_inventory.md")

START = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration|module|endmodule)\b"
)


def strip_line_comment(line: str) -> str:
    in_string = False
    escaped = False
    for index in range(len(line) - 1):
        character = line[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif line[index : index + 2] == "//":
            return line[:index]
    return line


records: list[dict[str, object]] = []
for path in FILES:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    lines = [strip_line_comment(line).rstrip() for line in raw_lines]
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines):
            if BOUNDARY.match(lines[index]):
                break
            index += 1
        sentence_lines = [
            line.strip() for line in lines[start:index] if line.strip()
        ]
        sentence = " ".join(sentence_lines)
        attribute_groups = re.findall(r"\[([^\]]*)\]", sentence)
        attributes: list[str] = []
        for attribute in (
            "function",
            "functional",
            "total",
            "no-evaluators",
            "concrete",
            "simplification",
            "priority",
            "owise",
            "macro-rec",
            "macro",
            "strict",
            "seqstrict",
            "symbol",
        ):
            if attribute in {"priority", "strict", "seqstrict", "symbol"}:
                present = any(
                    re.search(rf"(?:^|,\s*){re.escape(attribute)}\s*\(", group)
                    for group in attribute_groups
                )
            else:
                present = any(
                    re.search(
                        rf"(?:^|,\s*){re.escape(attribute)}(?:\s*,|$)", group
                    )
                    for group in attribute_groups
                )
            if present:
                attributes.append(attribute)
        if path == Path("/candidate/verification.k"):
            origin = "task-local verification"
            decision = "manual task-local review required"
        elif path == Path("/candidate/spec.k"):
            origin = "target specification"
            decision = "target/auxiliary proof obligation"
        else:
            origin = "trusted supplied semantics"
            decision = "fixed-baseline sentence; dependency reviewed by use map"
        records.append(
            {
                "id": len(records) + 1,
                "path": str(path),
                "line": start + 1,
                "kind": kind,
                "attributes": attributes,
                "origin": origin,
                "decision": decision,
                "sentence": sentence,
            }
        )

OUT_JSON.write_text(
    json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

counts = collections.Counter(str(record["kind"]) for record in records)
origin_counts = collections.Counter(str(record["origin"]) for record in records)
attribute_counts: collections.Counter[str] = collections.Counter()
for record in records:
    attribute_counts.update(record["attributes"])

lines = [
    "# Exhaustive source-level K sentence inventory",
    "",
    "Generated from the trusted supplied semantics plus candidate "
    "`verification.k` and `spec.k`. Multiline sentences are normalized onto "
    "one line; IDs retain source line locations.",
    "",
    f"- Total sentences: {len(records)}",
    f"- Kinds: `{dict(sorted(counts.items()))}`",
    f"- Origins: `{dict(sorted(origin_counts.items()))}`",
    f"- Attributes: `{dict(sorted(attribute_counts.items()))}`",
    "",
    "| ID | Source | Kind | Attributes | Origin/decision | Sentence |",
    "|---:|---|---|---|---|---|",
]
for record in records:
    source = f"{record['path']}:{record['line']}"
    sentence = str(record["sentence"]).replace("|", r"\|")
    decision = (
        f"{record['origin']}; {record['decision']}".replace("|", r"\|")
    )
    attrs = ", ".join(record["attributes"])
    lines.append(
        f"| {record['id']} | `{source}` | {record['kind']} | {attrs} | "
        f"{decision} | `{sentence}` |"
    )
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"FILES={len(FILES)}")
print(f"SENTENCES={len(records)}")
print(f"KINDS={dict(sorted(counts.items()))}")
print(f"ORIGINS={dict(sorted(origin_counts.items()))}")
print(f"ATTRIBUTES={dict(sorted(attribute_counts.items()))}")
print(f"JSON={OUT_JSON}")
print(f"MARKDOWN={OUT_MD}")
