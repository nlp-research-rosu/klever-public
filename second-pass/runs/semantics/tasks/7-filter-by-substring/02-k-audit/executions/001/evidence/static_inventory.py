#!/usr/bin/env python3
"""Create a source-line-complete inventory of local K declarations.

This is deliberately a lexical inventory rather than a trust decision.  It
captures every top-level syntax/rule/claim/context/configuration declaration
from the supplied source tree and the candidate proof sources, including each
declaration's complete source block and relevant K attributes.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path


START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?)\b"
)
ENDMODULE = re.compile(r"^\s*endmodule\b")
ATTRIBUTE_NAMES = (
    "function",
    "total",
    "functional",
    "macro",
    "simplification",
    "concrete",
    "owise",
    "no-evaluators",
    "token",
    "strict",
    "seqstrict",
    "assoc",
    "comm",
    "idem",
)


def attributes(block: str) -> list[str]:
    found = [
        attribute
        for attribute in ATTRIBUTE_NAMES
        if re.search(rf"\b{re.escape(attribute)}\b", block)
    ]
    found.extend(re.findall(r"\bpriority\s*\(\s*[^)]+\)", block))
    found.extend(re.findall(r"\bsymbol\s*\(\s*[^)]+\)", block))
    found.extend(re.findall(r"\bhook\s*\(\s*[^)]+\)", block))
    return sorted(set(found))


def classify(kind: str, attrs: list[str]) -> list[str]:
    classes = [kind.replace(" ", "-")]
    if kind == "syntax":
        if "function" in attrs or "functional" in attrs:
            classes.append("function-declaration")
        if "total" in attrs:
            classes.append("total-declaration")
        if any(attribute.startswith("symbol(") for attribute in attrs):
            classes.append("symbol-declaration")
        if "no-evaluators" in attrs:
            classes.append("proof-opaque-symbol-declaration")
        if "macro" in attrs:
            classes.append("macro-syntax")
    if kind == "rule":
        classes.append(
            "simplification-rule"
            if "simplification" in attrs
            else "ordinary-rule"
        )
        if any(attribute.startswith("priority(") for attribute in attrs):
            classes.append("priority-rule")
        if "concrete" in attrs:
            classes.append("concrete-rule")
        if "owise" in attrs:
            classes.append("owise-rule")
    return classes


def collect(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    records: list[dict[str, object]] = []
    for position, (start, kind) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        for candidate in range(start + 1, next_start):
            if ENDMODULE.match(lines[candidate]):
                end = candidate
                break
        while end > start + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        block = "\n".join(lines[start:end]).rstrip()
        attrs = attributes(block)
        records.append(
            {
                "file": str(path),
                "line": start + 1,
                "end_line": end,
                "kind": kind,
                "attributes": attrs,
                "classes": classify(kind, attrs),
                "block": block,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--markdown-out", required=True, type=Path)
    parser.add_argument("--json-out", required=True, type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    paths = [root / "reference-semantics" / "semantics.k"]
    paths.extend(sorted((root / "reference-semantics" / "semantics").glob("*.k")))
    paths.extend([root / "verification.k", root / "spec.k"])
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(f"missing inventory inputs: {missing}")

    records: list[dict[str, object]] = []
    for path in paths:
        records.extend(collect(path))
    for index, record in enumerate(records, 1):
        record["id"] = f"D{index:04d}"
        record["file"] = str(Path(str(record["file"])).relative_to(root))

    class_counts: collections.Counter[str] = collections.Counter()
    kind_counts: collections.Counter[str] = collections.Counter()
    file_counts: collections.Counter[str] = collections.Counter()
    for record in records:
        kind_counts[str(record["kind"])] += 1
        file_counts[str(record["file"])] += 1
        class_counts.update(str(value) for value in record["classes"])

    summary = {
        "record_count": len(records),
        "kind_counts": dict(sorted(kind_counts.items())),
        "class_counts": dict(sorted(class_counts.items())),
        "file_counts": dict(sorted(file_counts.items())),
    }
    args.json_out.write_text(
        json.dumps({"summary": summary, "records": records}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )

    markdown: list[str] = [
        "# Exhaustive K declaration inventory",
        "",
        "This lexical inventory covers the supplied semantics, every supplied helper",
        "K file, `verification.k`, and `spec.k`. Source blocks are copied from the",
        "scratch tree; trust and soundness decisions are in `REVIEW.md`.",
        "",
        "```json",
        json.dumps(summary, indent=2, sort_keys=True),
        "```",
        "",
    ]
    current_file = ""
    for record in records:
        file_name = str(record["file"])
        if file_name != current_file:
            current_file = file_name
            markdown.extend([f"## `{file_name}`", ""])
        attrs = ", ".join(record["attributes"]) or "none"
        classes = ", ".join(record["classes"])
        markdown.extend(
            [
                f"### {record['id']} — lines {record['line']}–{record['end_line']}",
                "",
                f"Kind/classes: `{record['kind']}`; {classes}. Attributes: {attrs}.",
                "",
                "```k",
                str(record["block"]),
                "```",
                "",
            ]
        )
    args.markdown_out.write_text("\n".join(markdown), encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
