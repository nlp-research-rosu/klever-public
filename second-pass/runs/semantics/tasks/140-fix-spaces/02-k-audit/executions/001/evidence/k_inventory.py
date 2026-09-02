#!/usr/bin/env python3
"""Emit a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/140-fix-spaces")
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.md")

START = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"module|endmodule|imports|configuration|syntax|rule|claim|context|alias"
    r")\b"
)
TOP_REQUIRES = re.compile(r'^requires\s+"')
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "opaque",
    "priority",
    "simplification",
    "macro",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
)


def selected_files() -> list[Path]:
    semantics_root = ROOT / "reference-semantics"
    files = [semantics_root / "semantics.k"]
    files.extend(sorted((semantics_root / "semantics").glob("*.k")))
    files.extend([ROOT / "verification.k", ROOT / "spec.k"])
    return files


def declarations(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind")))
        elif TOP_REQUIRES.match(line):
            starts.append((index, "requires"))

    records: list[dict[str, object]] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        while end > start + 1 and not lines[end - 1].strip():
            end -= 1
        snippet = "\n".join(lines[start:end])
        attributes = [attribute for attribute in ATTRIBUTES if re.search(rf"\b{attribute}\b", snippet)]
        records.append(
            {
                "kind": kind,
                "start": start + 1,
                "end": end,
                "attributes": attributes,
                "snippet": snippet,
            }
        )
    return records


def main() -> None:
    all_records: list[tuple[Path, dict[str, object]]] = []
    per_file: dict[Path, Counter[str]] = {}
    attribute_counts: Counter[str] = Counter()

    for path in selected_files():
        records = declarations(path)
        counter: Counter[str] = Counter(str(record["kind"]) for record in records)
        per_file[path] = counter
        for record in records:
            all_records.append((path, record))
            attribute_counts.update(str(item) for item in record["attributes"])

    with OUTPUT.open("w", encoding="utf-8") as output:
        output.write("# Exhaustive K declaration and rule inventory\n\n")
        output.write(
            "Generated from the fresh scratch copy. Each `syntax`, `configuration`, "
            "`rule`, and `claim` block is reproduced with its source span; module, "
            "import, and require records establish dependency scope.\n\n"
        )
        output.write("## Counts\n\n")
        output.write("| File | Syntax | Configuration | Rule | Claim | Other records |\n")
        output.write("|---|---:|---:|---:|---:|---:|\n")
        for path in selected_files():
            counter = per_file[path]
            other = sum(counter.values()) - sum(
                counter[name] for name in ("syntax", "configuration", "rule", "claim")
            )
            output.write(
                f"| `{path.relative_to(ROOT)}` | {counter['syntax']} | "
                f"{counter['configuration']} | {counter['rule']} | "
                f"{counter['claim']} | {other} |\n"
            )
        output.write("\nAttribute-bearing declaration counts: ")
        output.write(
            ", ".join(f"`{name}`={attribute_counts[name]}" for name in ATTRIBUTES)
        )
        output.write(".\n\n")

        current_path: Path | None = None
        for path, record in all_records:
            if path != current_path:
                output.write(f"## `{path.relative_to(ROOT)}`\n\n")
                current_path = path
            attrs = record["attributes"]
            attribute_text = ", ".join(str(item) for item in attrs) if attrs else "none"
            output.write(
                f"### {record['kind']} lines {record['start']}-{record['end']} "
                f"(attributes: {attribute_text})\n\n"
            )
            output.write("```k\n")
            output.write(str(record["snippet"]))
            output.write("\n```\n\n")

    print(f"output={OUTPUT}")
    print(f"files={len(selected_files())}")
    print(f"records={len(all_records)}")
    totals: Counter[str] = Counter(str(record["kind"]) for _, record in all_records)
    for kind in sorted(totals):
        print(f"{kind}={totals[kind]}")
    for name in ATTRIBUTES:
        print(f"attribute_{name}={attribute_counts[name]}")


if __name__ == "__main__":
    main()
