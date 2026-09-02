#!/usr/bin/env python3
"""Create an exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
SEMANTICS = SCRATCH / "reference-semantics"
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else None

source_files = [SEMANTICS / "semantics.k"]
source_files.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
source_files.append(SCRATCH / "verification.k")

start_pattern = re.compile(
    r"^(?:requires |module |endmodule\b|  (?:imports |configuration\b|syntax |context |rule\b|claim\b))"
)
kind_pattern = re.compile(
    r"^(?:requires|module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
attribute_pattern = re.compile(r"\[([^\]]+)\]")
recognized_attribute = re.compile(
    r"^(?:"
    r"function|functional|total|no-evaluators|macro|macro-rec|concrete|"
    r"simplification|owise|strict(?:\([^)]*\))?|seqstrict\([^)]*\)|"
    r"priority\([^)]*\)|symbol\([^)]*\)|hook\([^)]*\)"
    r")$"
)


def split_attributes(group: str) -> list[str]:
    values: list[str] = []
    start = 0
    depth = 0
    for index, character in enumerate(group):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            values.append(group[start:index].strip())
            start = index + 1
    values.append(group[start:].strip())
    return values

entries: list[dict[str, object]] = []

for path in source_files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if start_pattern.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        # Drop trailing comments/blanks that belong between declarations.
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        first = block_lines[0].strip()
        match = kind_pattern.match(first)
        if not match:
            raise RuntimeError(f"unclassified entry: {path}:{start + 1}: {first}")
        kind = match.group(0)
        block = "\n".join(block_lines)
        attributes = sorted(
            {
                item.strip()
                for group in attribute_pattern.findall(block)
                for item in split_attributes(group)
                if recognized_attribute.match(item.strip())
            }
        )
        entries.append(
            {
                "path": path.relative_to(SCRATCH).as_posix(),
                "line": start + 1,
                "end_line": start + len(block_lines),
                "kind": kind,
                "attributes": attributes,
                "block": block,
            }
        )

counts = collections.Counter(str(entry["kind"]) for entry in entries)
attribute_counts = collections.Counter(
    attribute
    for entry in entries
    for attribute in entry["attributes"]  # type: ignore[union-attr]
)

out: list[str] = []
out.append("K SOURCE INVENTORY")
out.append(f"source_file_count={len(source_files)}")
out.append(f"entry_count={len(entries)}")
out.append("kind_counts=" + repr(dict(sorted(counts.items()))))
out.append("attribute_counts=" + repr(dict(sorted(attribute_counts.items()))))
out.append("")

for entry_id, entry in enumerate(entries, start=1):
    out.append(
        f"ENTRY {entry_id:04d} "
        f"{entry['path']}:{entry['line']}-{entry['end_line']} "
        f"kind={entry['kind']} attributes={entry['attributes']}"
    )
    out.extend("  " + line for line in str(entry["block"]).splitlines())
    out.append("")

rendered = "\n".join(out) + "\n"
if OUTPUT is None:
    sys.stdout.write(rendered)
else:
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote={OUTPUT}")
    print(f"entry_count={len(entries)}")
    print("kind_counts=" + repr(dict(sorted(counts.items()))))
    print("attribute_counts=" + repr(dict(sorted(attribute_counts.items()))))
