#!/usr/bin/env python3
"""Create a line-addressable declaration inventory for all audited K sources."""

from __future__ import annotations

import argparse
import collections
import hashlib
import re
from pathlib import Path


START = re.compile(
    r"^(?:(requires)\b|\s*(module|endmodule|imports|configuration|syntax|context|rule|claim)\b)"
)


def classify(keyword: str, text: str) -> str:
    if keyword != "syntax" and keyword != "rule":
        return keyword
    tags: list[str] = []
    if keyword == "syntax":
        for tag in (
            "function",
            "total",
            "functional",
            "macro-rec",
            "macro",
            "symbol",
            "no-evaluators",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"(?<![A-Za-z-]){re.escape(tag)}(?![A-Za-z-])", text):
                tags.append(tag)
    else:
        for tag in ("simplification", "priority", "concrete", "owise"):
            if re.search(rf"(?<![A-Za-z-]){tag}(?![A-Za-z-])", text):
                tags.append(tag)
        if not tags:
            tags.append("ordinary")
    return f"{keyword}[{','.join(tags)}]"


def declaration_records(path: Path, display_root: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for offset, (start, keyword) in enumerate(starts):
        end = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        block_lines = []
        for line in lines[start:end]:
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            if "//" in stripped:
                stripped = stripped.split("//", 1)[0].rstrip()
            if stripped:
                block_lines.append(stripped)
        flat = " ".join(block_lines)
        flat = re.sub(r"\s+", " ", flat)
        yield {
            "file": str(path.relative_to(display_root)),
            "line": start + 1,
            "kind": classify(keyword, flat),
            "text": flat,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--inventory-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    paths = sorted((source_root / "reference-semantics").rglob("*.k"))
    paths.extend([source_root / "verification.k", source_root / "spec.k"])
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(f"missing K sources: {missing}")

    records = []
    file_hashes = {}
    for path in paths:
        records.extend(declaration_records(path, source_root))
        file_hashes[str(path.relative_to(source_root))] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

    header = "file\tline\tkind\tdeclaration\n"
    rows = [
        f"{r['file']}\t{r['line']}\t{r['kind']}\t{r['text']}\n" for r in records
    ]
    args.inventory_out.write_text(header + "".join(rows))

    kinds = collections.Counter(r["kind"] for r in records)
    per_file = collections.Counter(r["file"] for r in records)
    summary_lines = [
        f"source_root={source_root}",
        f"k_source_files={len(paths)}",
        f"inventory_records={len(records)}",
        "kind_counts:",
    ]
    summary_lines.extend(f"  {kind}={count}" for kind, count in sorted(kinds.items()))
    summary_lines.append("file_record_counts_and_sha256:")
    summary_lines.extend(
        f"  {name}\trecords={per_file[name]}\tsha256={file_hashes[name]}"
        for name in sorted(file_hashes)
    )
    args.summary_out.write_text("\n".join(summary_lines) + "\n")
    print("\n".join(summary_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
