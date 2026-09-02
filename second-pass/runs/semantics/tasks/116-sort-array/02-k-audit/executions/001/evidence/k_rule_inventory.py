#!/usr/bin/env python3
"""Emit a lossless, line-addressed inventory of candidate K declarations."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/candidate/reference-semantics"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
OUT_DIR = Path("/audit-output/evidence")
START = re.compile(
    r"^\s*(requires|module|imports|endmodule|configuration|syntax|rule|claim|context|alias)\b"
)
MODULE = re.compile(r"^\s*module\s+(\S+)")
ATTR = re.compile(r"\[([^\]]+)\]")
FLAGS = (
    "function",
    "total",
    "functional",
    "simplification",
    "anywhere",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "no-evaluators",
    "symbol",
)


def source_files() -> list[Path]:
    paths: list[Path] = []
    for root in ROOTS:
        if root.is_dir():
            paths.extend(sorted(root.rglob("*.k")))
        else:
            paths.append(root)
    return paths


def disposition(path: Path, kind: str) -> str:
    if "reference-semantics" in path.parts:
        return "fixed-supplied-semantics"
    if path.name == "verification.k":
        return "candidate-proof-extension"
    if path.name == "spec.k" and kind == "claim":
        return "candidate-positive-claim"
    return "candidate-spec-structure"


def inventory_file(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts = [(index, START.match(line)) for index, line in enumerate(lines)]
    starts = [(index, match) for index, match in starts if match]
    entries: list[dict[str, object]] = []
    current_module = ""
    for position, (index, match) in enumerate(starts):
        assert match is not None
        kind = match.group(1)
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:next_index]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        block = "\n".join(block_lines)
        module_match = MODULE.match(lines[index])
        if module_match:
            current_module = module_match.group(1)
        code_block = "\n".join(
            line for line in block_lines if not line.lstrip().startswith("//")
        )
        attrs = "; ".join(ATTR.findall(code_block))
        flags = []
        for flag in FLAGS:
            if flag == "symbol":
                present = "symbol(" in attrs
            elif flag == "priority":
                present = "priority(" in attrs
            elif flag == "macro":
                present = re.search(r"(?<![-\w])macro(?![-\w])", attrs) is not None
            else:
                present = re.search(rf"\b{re.escape(flag)}\b", attrs) is not None
            if present:
                flags.append(flag)
        entries.append(
            {
                "source": str(path),
                "module": current_module,
                "start_line": index + 1,
                "end_line": index + max(1, len(block_lines)),
                "kind": kind,
                "attributes": attrs,
                "flags": ",".join(flags),
                "disposition": disposition(path, kind),
                "text": block,
            }
        )
        if kind == "endmodule":
            current_module = ""
    return entries


def main() -> int:
    entries: list[dict[str, object]] = []
    for path in source_files():
        entries.extend(inventory_file(path))

    inventory_path = OUT_DIR / "k-inventory.tsv"
    fieldnames = [
        "id",
        "source",
        "module",
        "start_line",
        "end_line",
        "kind",
        "attributes",
        "flags",
        "disposition",
        "text",
    ]
    with inventory_path.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for number, entry in enumerate(entries, 1):
            writer.writerow({"id": f"K{number:04d}", **entry})

    special = [entry for entry in entries if entry["flags"]]
    special_path = OUT_DIR / "k-special-declarations.tsv"
    with special_path.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for number, entry in enumerate(special, 1):
            writer.writerow({"id": f"S{number:04d}", **entry})

    by_kind = Counter(str(entry["kind"]) for entry in entries)
    by_file = Counter(str(entry["source"]) for entry in entries)
    by_disposition = Counter(str(entry["disposition"]) for entry in entries)
    flag_counts = Counter(
        flag
        for entry in entries
        for flag in str(entry["flags"]).split(",")
        if flag
    )
    summary = {
        "source_files": len(source_files()),
        "total_entries": len(entries),
        "by_kind": dict(sorted(by_kind.items())),
        "by_file": dict(sorted(by_file.items())),
        "by_disposition": dict(sorted(by_disposition.items())),
        "flag_counts": dict(sorted(flag_counts.items())),
        "special_entry_count": len(special),
        "inventory": str(inventory_path),
        "special_inventory": str(special_path),
    }
    (OUT_DIR / "k-inventory-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
