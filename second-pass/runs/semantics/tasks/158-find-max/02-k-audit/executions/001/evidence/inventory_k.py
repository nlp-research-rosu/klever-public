#!/usr/bin/env python3
"""Build a source-linked inventory of K declarations used by the audit."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
OUT = Path("/audit-output/evidence")
SOURCE_FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

start_re = re.compile(r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?)\b")
module_re = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")


def attributes(text: str) -> list[str]:
    found: list[str] = []
    checks = [
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("symbol", r"\bsymbol\s*(?:\(|[,\]])"),
        ("no-evaluators", r"\bno-evaluators\b"),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification\b"),
        ("owise", r"\bowise\b"),
        ("strict", r"\bstrict\s*(?:\(|[,\]])"),
        ("seqstrict", r"\bseqstrict\s*(?:\(|[,\]])"),
    ]
    for label, pattern in checks:
        if re.search(pattern, text):
            found.append(label)
    return found


records: list[dict[str, object]] = []
modules: list[dict[str, object]] = []

for path in SOURCE_FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    current_module = None
    module_by_line: list[str | None] = []
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        module_match = module_re.match(line)
        if module_match:
            current_module = module_match.group(1)
            modules.append(
                {
                    "file": str(path.relative_to(ROOT)),
                    "line": index + 1,
                    "module": current_module,
                }
            )
        module_by_line.append(current_module)
        declaration_match = start_re.match(line)
        if declaration_match:
            starts.append((index, declaration_match.group(1)))
        if line.strip() == "endmodule":
            current_module = None

    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        # Avoid absorbing endmodule into the declaration text.
        while end > start + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        text = "\n".join(lines[start:end]).rstrip()
        records.append(
            {
                "id": len(records) + 1,
                "file": str(path.relative_to(ROOT)),
                "module": module_by_line[start],
                "kind": "context" if kind.startswith("context") else kind,
                "start_line": start + 1,
                "end_line": end,
                "attributes": attributes(text),
                "text": text,
            }
        )

OUT.joinpath("k-rule-inventory.json").write_text(
    json.dumps({"modules": modules, "declarations": records}, indent=2) + "\n",
    encoding="utf-8",
)

kind_counts: dict[str, int] = {}
attribute_counts: dict[str, int] = {}
file_counts: dict[str, int] = {}
for record in records:
    kind = str(record["kind"])
    kind_counts[kind] = kind_counts.get(kind, 0) + 1
    file_name = str(record["file"])
    file_counts[file_name] = file_counts.get(file_name, 0) + 1
    for attribute in record["attributes"]:
        label = str(attribute)
        attribute_counts[label] = attribute_counts.get(label, 0) + 1

markdown: list[str] = [
    "# K declaration and rule inventory",
    "",
    "Generated directly from the clean scratch source copy. Each entry includes",
    "the complete declaration/rule text through the next top-level declaration.",
    "",
    "## Counts",
    "",
    f"- Modules: {len(modules)}",
    f"- Declarations: {len(records)}",
    f"- By kind: {json.dumps(kind_counts, sort_keys=True)}",
    f"- By attribute: {json.dumps(attribute_counts, sort_keys=True)}",
    "",
    "## Per-file counts",
    "",
]
for file_name, count in sorted(file_counts.items()):
    markdown.append(f"- `{file_name}`: {count}")

markdown.extend(["", "## Complete inventory", ""])
for record in records:
    attrs = ", ".join(record["attributes"]) if record["attributes"] else "none"
    first_line = str(record["text"]).splitlines()[0].strip()
    markdown.extend(
        [
            (
                f"### {record['id']}. `{record['file']}:{record['start_line']}` "
                f"— {record['kind']} ({attrs})"
            ),
            "",
            f"First line: `{first_line.replace('`', chr(39))}`",
            "",
            "```k",
            str(record["text"]),
            "```",
            "",
        ]
    )

OUT.joinpath("k-rule-inventory.md").write_text(
    "\n".join(markdown), encoding="utf-8"
)

print(
    json.dumps(
        {
            "modules": len(modules),
            "declarations": len(records),
            "kind_counts": kind_counts,
            "attribute_counts": attribute_counts,
            "file_counts": file_counts,
        },
        indent=2,
        sort_keys=True,
    )
)
