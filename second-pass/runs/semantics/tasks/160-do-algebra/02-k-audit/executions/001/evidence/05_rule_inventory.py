#!/usr/bin/env python3
"""Create an exhaustive, line-addressed inventory of K declarations and rules."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path("/tmp/audit-work/rebuild")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(?:(?P<root_kind>requires|module|endmodule)|  (?P<module_kind>imports|syntax|configuration|context|rule|claim|alias))\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")


def declarations(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, re.Match[str]]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match))

    records: list[dict[str, Any]] = []
    module = None
    for pos, (index, match) in enumerate(starts):
        kind = match.group("root_kind") or match.group("module_kind")
        line = lines[index]
        if kind == "module":
            module = line.strip().split(maxsplit=1)[1]

        # A declaration ends immediately before the next declaration start.
        next_index = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block_lines = lines[index:next_index]
        while block_lines and (not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")):
            block_lines.pop()
        block = "\n".join(block_lines)
        attributes = []
        for attr_group in ATTR.findall(block):
            attributes.extend(piece.strip() for piece in attr_group.split(","))

        if kind == "rule":
            if any(piece.startswith("macro") for piece in attributes):
                rule_class = "macro rule"
            elif any(piece.startswith("simplification") for piece in attributes):
                rule_class = "simplification rule"
            else:
                rule_class = "ordinary semantic rule"
        elif kind == "claim":
            rule_class = "reachability claim"
        elif kind == "syntax":
            rule_class = "syntax declaration"
        else:
            rule_class = kind

        records.append(
            {
                "file": str(path.relative_to(ROOT)),
                "line": index + 1,
                "module": module,
                "kind": kind,
                "class": rule_class,
                "attributes": attributes,
                "function": any(piece == "function" or piece.startswith("function(") for piece in attributes),
                "total": any(piece == "total" or piece.startswith("total(") for piece in attributes),
                "functional": any(piece == "functional" or piece.startswith("functional(") for piece in attributes),
                "opaque": any(piece == "no-evaluators" for piece in attributes),
                "priority": [piece for piece in attributes if piece.startswith("priority")],
                "simplification": any(piece.startswith("simplification") for piece in attributes),
                "text": block,
            }
        )
        if kind == "endmodule":
            module = None
    return records


def main() -> int:
    all_records = [record for source in SOURCES for record in declarations(source)]
    counts_by_file: dict[str, Counter[str]] = defaultdict(Counter)
    for record in all_records:
        counts_by_file[record["file"]][record["class"]] += 1

    summary = {
        "source_count": len(SOURCES),
        "record_count": len(all_records),
        "rule_count": sum(record["kind"] == "rule" for record in all_records),
        "claim_count": sum(record["kind"] == "claim" for record in all_records),
        "syntax_count": sum(record["kind"] == "syntax" for record in all_records),
        "function_declaration_count": sum(record["function"] for record in all_records),
        "total_declaration_count": sum(record["total"] for record in all_records),
        "functional_declaration_count": sum(record["functional"] for record in all_records),
        "opaque_declaration_count": sum(record["opaque"] for record in all_records),
        "priority_rule_count": sum(bool(record["priority"]) and record["kind"] == "rule" for record in all_records),
        "simplification_rule_count": sum(record["simplification"] and record["kind"] == "rule" for record in all_records),
        "counts_by_file": {key: dict(value) for key, value in sorted(counts_by_file.items())},
    }

    output = {"summary": summary, "records": all_records}
    json_path = Path("/audit-output/evidence/05_rule_inventory.json")
    json_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")

    text_path = Path("/audit-output/evidence/05_rule_inventory.txt")
    lines = [json.dumps(summary, indent=2, sort_keys=True), "", "DECLARATIONS"]
    for record in all_records:
        flags = []
        for name in ("function", "total", "functional", "opaque", "simplification"):
            if record[name]:
                flags.append(name)
        flags.extend(record["priority"])
        lines.append(
            f'\n[{record["file"]}:{record["line"]}] {record["class"]}'
            + (f' ({", ".join(flags)})' if flags else "")
        )
        lines.append(record["text"])
    text_path.write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
