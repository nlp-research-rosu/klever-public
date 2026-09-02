#!/usr/bin/env python3
"""Lexically inventory K sentences for the audit's exhaustive static review."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
OUTPUT_JSON = Path("/audit-output/evidence/stage5/rule-inventory.json")
OUTPUT_MD = Path("/audit-output/evidence/stage5/rule-inventory.md")

START = re.compile(
    r"^(?:requires\b|\s*(?:module|endmodule|imports|configuration|"
    r"context(?:\s+alias)?|syntax|rule|claim)\b)"
)


def classify(text: str) -> tuple[str, list[str]]:
    first = text.lstrip().split(None, 1)[0]
    tags: list[str] = []
    if first == "syntax":
        kind = "syntax"
        for tag in (
            "function",
            "total",
            "functional",
            "macro",
            "hook",
            "token",
            "symbol",
            "bracket",
        ):
            if re.search(rf"\b{tag}\b", text):
                tags.append(tag)
    elif first == "rule":
        kind = "rule"
        tags.append("simplification" if "simplification" in text else "ordinary")
        if "priority(" in text:
            tags.append("priority")
        if "owise" in text:
            tags.append("owise")
        if "anywhere" in text:
            tags.append("anywhere")
    elif first == "claim":
        kind = "claim"
        if "trusted" in text:
            tags.append("trusted")
    else:
        kind = first
    return kind, tags


def sentences(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: list[dict] = []
    active_start: int | None = None
    active_lines: list[str] = []

    def finish() -> None:
        nonlocal active_start, active_lines
        if active_start is None:
            return
        text = "\n".join(active_lines).rstrip()
        kind, tags = classify(text)
        result.append(
            {
                "file": str(path.relative_to(ROOT)),
                "line": active_start,
                "kind": kind,
                "tags": tags,
                "text": text,
            }
        )
        active_start = None
        active_lines = []

    for number, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("//") or not stripped:
            if active_start is not None:
                active_lines.append(line)
            continue
        if START.match(line):
            finish()
            active_start = number
            active_lines = [line]
        elif active_start is not None:
            active_lines.append(line)
    finish()
    return result


def main() -> None:
    paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    records: list[dict] = []
    for path in paths:
        records.extend(sentences(path))

    counts = Counter(record["kind"] for record in records)
    rule_tags = Counter(
        tag
        for record in records
        if record["kind"] == "rule"
        for tag in record["tags"]
    )
    syntax_tags = Counter(
        tag
        for record in records
        if record["kind"] == "syntax"
        for tag in record["tags"]
    )
    payload = {
        "source_root": str(ROOT),
        "files": [str(path.relative_to(ROOT)) for path in paths],
        "counts": dict(sorted(counts.items())),
        "rule_tags": dict(sorted(rule_tags.items())),
        "syntax_tags": dict(sorted(syntax_tags.items())),
        "records": records,
    }
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    rows = [
        "# Exhaustive lexical K inventory",
        "",
        f"Source root: `{ROOT}`",
        "",
        f"Files: {len(paths)}; records: {len(records)}",
        "",
        f"Sentence counts: `{dict(sorted(counts.items()))}`",
        "",
        f"Rule tags: `{dict(sorted(rule_tags.items()))}`",
        "",
        f"Syntax tags: `{dict(sorted(syntax_tags.items()))}`",
        "",
        "| # | File:line | Kind | Tags | Full normalized sentence |",
        "|---:|---|---|---|---|",
    ]
    for index, record in enumerate(records, start=1):
        normalized = " ".join(record["text"].split())
        normalized = normalized.replace("|", "\\|")
        tags = ", ".join(record["tags"])
        rows.append(
            f"| {index} | `{record['file']}:{record['line']}` | "
            f"{record['kind']} | {tags} | `{normalized}` |"
        )
    OUTPUT_MD.write_text("\n".join(rows) + "\n", encoding="utf-8")

    print(f"files={len(paths)}")
    print(f"records={len(records)}")
    print(f"counts={dict(sorted(counts.items()))}")
    print(f"rule_tags={dict(sorted(rule_tags.items()))}")
    print(f"syntax_tags={dict(sorted(syntax_tags.items()))}")
    print(OUTPUT_JSON)
    print(OUTPUT_MD)


if __name__ == "__main__":
    main()
