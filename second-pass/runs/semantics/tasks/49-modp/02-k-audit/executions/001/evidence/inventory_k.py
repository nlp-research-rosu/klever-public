#!/usr/bin/env python3
"""Create a complete, source-indexed inventory of local K statements."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START_RE = re.compile(r"^  (configuration|syntax|context|rule|claim)\b")
STOP_RE = re.compile(r"^(?:module|endmodule|requires)\b|^  (?:module|endmodule|imports)\b")


def normalized(lines: list[str]) -> str:
    return " ".join(part.strip() for part in lines if part.strip())


def flags(kind: str, text: str) -> list[str]:
    found: list[str] = []
    for attribute in (
        "function",
        "functional",
        "total",
        "simplification",
        "concrete",
        "owise",
        "macro",
        "hook",
        "symbol",
        "no-evaluators",
    ):
        if re.search(rf"\b{re.escape(attribute)}\b", text):
            found.append(attribute)
    if "priority(" in text:
        found.append("priority")
    if kind == "rule":
        found.append("operational" if "<k>" in text or "<" + "generatedTop>" in text else "equational/pure")
    return found


def extract(path: Path) -> list[tuple[int, int, str, str, list[str]]]:
    source = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(source):
        match = START_RE.match(line)
        if match:
            starts.append((index, match.group(1)))

    records: list[tuple[int, int, str, str, list[str]]] = []
    for position, (start, kind) in enumerate(starts):
        limit = starts[position + 1][0] if position + 1 < len(starts) else len(source)
        end = start + 1
        while end < limit and not STOP_RE.match(source[end]):
            end += 1
        block = source[start:end]
        while len(block) > 1 and (
            not block[-1].strip() or block[-1].lstrip().startswith("//")
        ):
            block.pop()
            end -= 1
        text = normalized(block)
        records.append((start + 1, end, kind, text, flags(kind, text)))
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    sources = sorted((arguments.root / "reference-semantics").rglob("*.k"))
    sources.extend([arguments.root / "verification.k", arguments.root / "spec.k"])

    all_records: dict[Path, list[tuple[int, int, str, str, list[str]]]] = {}
    counts: Counter[str] = Counter()
    flag_counts: Counter[str] = Counter()
    for path in sources:
        records = extract(path)
        all_records[path] = records
        for _start, _end, kind, _text, record_flags in records:
            counts[kind] += 1
            flag_counts.update(record_flags)

    lines = [
        "# Exhaustive local K declaration and rule inventory",
        "",
        "Generated from the clean scratch source copy. Each entry contains the exact",
        "source line range and a whitespace-normalized rendering of the complete",
        "top-level statement.",
        "",
        "## Counts",
        "",
        f"- Source files: {len(sources)}",
    ]
    for kind in ("configuration", "syntax", "context", "rule", "claim"):
        lines.append(f"- `{kind}` statements: {counts[kind]}")
    for flag in (
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "concrete",
        "owise",
        "macro",
        "hook",
        "operational",
        "equational/pure",
    ):
        lines.append(f"- Entries flagged `{flag}`: {flag_counts[flag]}")

    lines.extend(
        [
            "",
            "## Per-file statement counts",
            "",
            "| File | configuration | syntax | context | rule | claim |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for path, records in all_records.items():
        relative = path.relative_to(arguments.root)
        file_counts = Counter(record[2] for record in records)
        lines.append(
            f"| `{relative}` | {file_counts['configuration']} | "
            f"{file_counts['syntax']} | {file_counts['context']} | "
            f"{file_counts['rule']} | {file_counts['claim']} |"
        )

    for path, records in all_records.items():
        relative = path.relative_to(arguments.root)
        lines.extend(["", f"## `{relative}`", ""])
        if not records:
            lines.append("_No local configuration, syntax, context, rule, or claim statements._")
            continue
        for start, end, kind, text, record_flags in records:
            location = str(start) if start == end else f"{start}-{end}"
            flag_text = ", ".join(record_flags) if record_flags else "none"
            lines.append(
                f"- `{kind}` lines {location}; flags: `{flag_text}` — `{text.replace('`', '´')}`"
            )

    arguments.output.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"source_files={len(sources)}")
    print("statement_counts=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)))
    print("flag_counts=" + ",".join(f"{key}:{flag_counts[key]}" for key in sorted(flag_counts)))
    print(f"output={arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
