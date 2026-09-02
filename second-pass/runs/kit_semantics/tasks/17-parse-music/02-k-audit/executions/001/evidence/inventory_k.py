#!/usr/bin/env python3
"""Create a stable, exhaustive declaration/rule inventory for the audit."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
OUTPUT = Path("/audit-output/evidence/rule_inventory.txt")
SUMMARY = Path("/audit-output/evidence/rule_inventory_summary.json")
START = re.compile(
    r"^(?:requires|module|endmodule)\b|^  "
    r"(?P<kind>imports|syntax|configuration|context|rule|claim|priority|lexical)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_files() -> list[Path]:
    return [
        ROOT / "reference-semantics/semantics.k",
        *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
        ROOT / "verification.k",
        ROOT / "spec.k",
    ]


def kind_of(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("requires"):
        return "requires"
    if stripped.startswith("module") and not stripped.startswith("endmodule"):
        return "module"
    if stripped.startswith("endmodule"):
        return "endmodule"
    match = START.match(line)
    if match and match.group("kind"):
        return match.group("kind")
    raise AssertionError(line)


def entries(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for ordinal, start in enumerate(starts):
        end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        block = "\n".join(block_lines)
        code_only = "\n".join(line.split("//", 1)[0] for line in block_lines)
        yield {
            "line": start + 1,
            "kind": kind_of(lines[start]),
            "block": block,
            "attributes": [
                attribute
                for attribute in ATTRIBUTES
                if re.search(rf"\b{re.escape(attribute)}\b", code_only)
            ],
        }


def main() -> None:
    files = source_files()
    all_entries = []
    serials = Counter()
    file_summaries = {}
    rendered = [
        "EXHAUSTIVE K SOURCE INVENTORY",
        f"root={ROOT}",
        "",
    ]
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        file_entries = list(entries(path))
        counts = Counter(entry["kind"] for entry in file_entries)
        attribute_counts = Counter(
            attribute
            for entry in file_entries
            for attribute in entry["attributes"]
        )
        file_summaries[relative] = {
            "sha256": digest(path),
            "lines": len(path.read_text().splitlines()),
            "entry_counts": dict(sorted(counts.items())),
            "attribute_entry_counts": dict(sorted(attribute_counts.items())),
        }
        rendered.extend(
            [
                f"===== FILE {relative} =====",
                f"sha256={digest(path)} lines={file_summaries[relative]['lines']}",
                "",
            ]
        )
        for entry in file_entries:
            serials[entry["kind"]] += 1
            entry_id = f"{entry['kind'].upper()}-{serials[entry['kind']]:04d}"
            entry["id"] = entry_id
            entry["file"] = relative
            all_entries.append(entry)
            rendered.append(
                f"--- {entry_id} {relative}:{entry['line']} "
                f"attributes={','.join(entry['attributes']) or '-'} ---"
            )
            for offset, line in enumerate(entry["block"].splitlines()):
                rendered.append(f"{entry['line'] + offset:5d} | {line}")
            rendered.append("")

    global_counts = Counter(entry["kind"] for entry in all_entries)
    global_attribute_counts = Counter(
        attribute for entry in all_entries for attribute in entry["attributes"]
    )
    summary = {
        "root": str(ROOT),
        "files": file_summaries,
        "global_entry_counts": dict(sorted(global_counts.items())),
        "global_attribute_entry_counts": dict(
            sorted(global_attribute_counts.items())
        ),
        "inventory_sha256": None,
    }
    OUTPUT.write_text("\n".join(rendered) + "\n")
    summary["inventory_sha256"] = digest(OUTPUT)
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(f"inventory={OUTPUT}")
    print(f"summary={SUMMARY}")
    print(f"files={len(files)}")
    print(f"entry_counts={dict(sorted(global_counts.items()))}")
    print(f"attribute_entry_counts={dict(sorted(global_attribute_counts.items()))}")
    print(f"inventory_sha256={summary['inventory_sha256']}")


if __name__ == "__main__":
    main()
