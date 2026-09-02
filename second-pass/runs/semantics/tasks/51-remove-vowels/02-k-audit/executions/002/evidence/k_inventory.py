#!/usr/bin/env python3
"""Create a source-complete inventory of K declarations for the audit."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/reconstruction/reference-semantics/semantics.k"),
    *sorted(
        Path("/tmp/audit-work/reconstruction/reference-semantics/semantics").glob(
            "*.k"
        )
    ),
    Path("/tmp/audit-work/reconstruction/verification.k"),
    Path("/tmp/audit-work/reconstruction/spec.k"),
]
OUT = Path("/audit-output/evidence/stage5-k-inventory.json")
KEYWORDS = ("configuration", "syntax", "rule", "claim", "context", "alias")
START = re.compile(r"^  (" + "|".join(KEYWORDS) + r")\b")
MODULE = re.compile(r"^module\s+([A-Za-z][A-Za-z0-9_-]*)\b")
ENDMODULE = re.compile(r"^endmodule\b")


ATTR_WORDS = {
    "assoc",
    "bracket",
    "comm",
    "concrete",
    "element",
    "format",
    "function",
    "functional",
    "hook",
    "klabel",
    "left",
    "macro",
    "macro-rec",
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


def mask_non_code(text: str) -> str:
    output = list(text)
    index = 0
    state = "code"
    depth = 0
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
            if char not in "\r\n":
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


def attributes(text: str) -> list[str]:
    masked = mask_non_code(text)
    result: list[str] = []
    for match in re.finditer(r"\[([^\[\]]+)\]", masked):
        candidate = match.group(1).strip()
        words = set(re.findall(r"[A-Za-z][A-Za-z0-9_-]*", candidate))
        if words & ATTR_WORDS:
            result.append(text[match.start(1) : match.end(1)].strip())
    return result


entries: list[dict[str, object]] = []
per_file: collections.Counter[str] = collections.Counter()

for path in ROOTS:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)

    current_module: str | None = None
    starts: list[tuple[int, int, str, str]] = []
    for index, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        module_match = MODULE.match(stripped)
        if module_match:
            current_module = module_match.group(1)
            continue
        if ENDMODULE.match(stripped):
            starts.append((index, offsets[index], "endmodule", current_module or ""))
            current_module = None
            continue
        sentence_match = START.match(stripped)
        if sentence_match and current_module is not None:
            starts.append(
                (index, offsets[index], sentence_match.group(1), current_module)
            )

    declaration_starts = [item for item in starts if item[2] != "endmodule"]
    boundaries = sorted((start, keyword) for _, start, keyword, _ in starts)
    for ordinal, (line_index, start, keyword, module_name) in enumerate(
        declaration_starts, 1
    ):
        later = [position for position, _ in boundaries if position > start]
        end = min(later) if later else len(text)
        source = text[start:end].rstrip()
        end_line = line_index + source.count("\n") + 1
        attrs = attributes(source)
        attr_text = ",".join(attrs)
        flags = {
            "function": bool(re.search(r"(^|,)\s*function\s*(,|$)", attr_text)),
            "total": bool(re.search(r"(^|,)\s*total\s*(,|$)", attr_text)),
            "functional": bool(
                re.search(r"(^|,)\s*functional\s*(,|$)", attr_text)
            ),
            "macro": bool(re.search(r"(^|,)\s*macro\s*(,|$)", attr_text)),
            "simplification": "simplification" in attr_text,
            "priority": "priority(" in attr_text,
            "concrete": bool(re.search(r"(^|,)\s*concrete\s*(,|$)", attr_text)),
            "owise": bool(re.search(r"(^|,)\s*owise\s*(,|$)", attr_text)),
            "opaque": "opaque" in attr_text or "no-evaluators" in attr_text,
            "symbol": "symbol(" in attr_text,
        }
        if keyword == "rule":
            category = "simplification-rule" if flags["simplification"] else "rule"
        elif keyword == "syntax" and flags["macro"]:
            category = "macro-syntax"
        elif keyword == "syntax" and flags["opaque"]:
            category = "opaque-symbol-syntax"
        elif keyword == "syntax" and flags["function"]:
            category = "function-syntax"
        else:
            category = keyword
        relative = (
            "verification.k"
            if path.name == "verification.k"
            else "spec.k"
            if path.name == "spec.k"
            else path.relative_to(
                Path("/tmp/audit-work/reconstruction")
            ).as_posix()
        )
        digest = hashlib.sha256(source.encode()).hexdigest()
        entry = {
            "id": f"{relative}:{module_name}:{line_index + 1}",
            "file": relative,
            "module": module_name,
            "start_line": line_index + 1,
            "end_line": end_line,
            "keyword": keyword,
            "category": category,
            "attributes": attrs,
            "flags": flags,
            "source_sha256": digest,
            "source": source,
        }
        entries.append(entry)
        per_file[relative] += 1

assert len(entries) == 949, f"expected 949 source declarations, got {len(entries)}"
assert sum(entry["keyword"] == "claim" for entry in entries) == 4
assert sum(entry["keyword"] == "configuration" for entry in entries) == 1

counts = collections.Counter(str(entry["keyword"]) for entry in entries)
categories = collections.Counter(str(entry["category"]) for entry in entries)
flag_counts = {
    flag: sum(bool(entry["flags"][flag]) for entry in entries)
    for flag in next(iter(entries))["flags"]
}
document = {
    "schema_version": 1,
    "roots": [str(path) for path in ROOTS],
    "counts": dict(sorted(counts.items())),
    "categories": dict(sorted(categories.items())),
    "flag_counts": flag_counts,
    "per_file": dict(sorted(per_file.items())),
    "entries": entries,
}
encoded = json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
OUT.write_text(encoded, encoding="utf-8")
print(f"output={OUT}")
print(f"output_sha256={hashlib.sha256(encoded.encode()).hexdigest()}")
print(f"declarations={len(entries)} counts={dict(sorted(counts.items()))}")
print(f"categories={dict(sorted(categories.items()))}")
print(f"flag_counts={flag_counts}")
for filename, count in sorted(per_file.items()):
    print(f"file={filename} declarations={count}")
